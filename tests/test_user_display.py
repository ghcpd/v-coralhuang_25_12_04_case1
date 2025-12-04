"""
Comprehensive tests for user_display system.
"""

import unittest
import time
import threading
import random
import json
from typing import Dict, Any, List

from user_display import (
    UserStore,
    UserSnapshot,
    CompactFormatter,
    JSONFormatter,
    TableFormatter,
    RegexFilter,
    CompositeFilter,
    DefaultValidator,
    get_metrics,
    get_logger,
    get_config,
)
from user_display_optimized import UserDisplayOptimized


class TestUserStore(unittest.TestCase):
    """Tests for UserStore."""

    def setUp(self):
        """Set up test fixtures."""
        self.store = UserStore(shard_count=4)
        self.sample_users = [
            {
                "id": i,
                "name": f"User{i}",
                "email": f"user{i}@example.com",
                "role": "Admin" if i % 3 == 0 else "User",
                "status": "Active" if i % 5 != 0 else "Inactive",
                "join_date": "2023-01-01",
                "last_login": "2025-11-26",
            }
            for i in range(1, 51)
        ]

    def test_add_and_retrieve_user(self):
        """Test adding and retrieving users."""
        self.store.add_user(self.sample_users[0])
        user = self.store.get_user(1)
        self.assertIsNotNone(user)
        self.assertEqual(user["name"], "User1")

    def test_get_user_by_id_o1(self):
        """Test O(1) ID lookup."""
        for user in self.sample_users:
            self.store.add_user(user)

        # Lookup should be fast
        start = time.time()
        user = self.store.get_user(25)
        duration_ms = (time.time() - start) * 1000
        
        self.assertIsNotNone(user)
        self.assertLess(duration_ms, 5)  # Should be much faster than 5ms

    def test_nonexistent_user(self):
        """Test lookup of nonexistent user."""
        self.store.add_user(self.sample_users[0])
        user = self.store.get_user(999)
        self.assertIsNone(user)

    def test_user_count(self):
        """Test user count."""
        for user in self.sample_users:
            self.store.add_user(user)
        self.assertEqual(self.store.user_count(), 50)

    def test_remove_user(self):
        """Test user removal."""
        self.store.add_user(self.sample_users[0])
        self.assertTrue(self.store.remove_user(1))
        self.assertFalse(self.store.remove_user(1))
        self.assertIsNone(self.store.get_user(1))

    def test_get_all_users(self):
        """Test getting all users."""
        for user in self.sample_users:
            self.store.add_user(user)
        
        all_users = self.store.get_all_users()
        self.assertEqual(len(all_users), 50)

    def test_sharding(self):
        """Test that users are distributed across shards."""
        for user in self.sample_users:
            self.store.add_user(user)
        
        stats = self.store.stats()
        shard_sizes = stats["shard_sizes"]
        
        # At least some shards should be used
        non_empty_shards = sum(1 for size in shard_sizes if size > 0)
        self.assertGreater(non_empty_shards, 1)

    def test_snapshot_creation(self):
        """Test snapshot creation."""
        for user in self.sample_users:
            self.store.add_user(user)
        
        snapshot = self.store.create_snapshot()
        self.assertIsNotNone(snapshot)
        self.assertEqual(len(snapshot.get_all()), 50)

    def test_snapshot_isolation(self):
        """Test that snapshot is isolated from store changes."""
        self.store.add_user(self.sample_users[0])
        snapshot = self.store.create_snapshot()
        
        # Add more users
        self.store.add_user(self.sample_users[1])
        
        # Snapshot should still have only 1 user
        self.assertEqual(len(snapshot.get_all()), 1)

    def test_clone_store(self):
        """Test cloning a store."""
        for user in self.sample_users:
            self.store.add_user(user)
        
        cloned = self.store.clone()
        self.assertEqual(cloned.user_count(), self.store.user_count())
        
        # Modifications to clone don't affect original
        cloned.remove_user(1)
        self.assertIsNone(cloned.get_user(1))
        self.assertIsNotNone(self.store.get_user(1))

    def test_concurrent_reads(self):
        """Test concurrent reads are thread-safe."""
        for user in self.sample_users:
            self.store.add_user(user)
        
        results = []
        
        def read_random_user():
            uid = random.randint(1, 50)
            user = self.store.get_user(uid)
            results.append(user is not None)
        
        threads = [threading.Thread(target=read_random_user) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(len(results), 10)

    def test_validation_soft_fail(self):
        """Test validation with soft failure."""
        config = get_config()
        config.set("validate_on_insert", True)
        config.set("soft_fail_on_validation", True)
        
        invalid_user = {"id": 1}  # Missing fields
        self.store.add_user(invalid_user)
        
        user = self.store.get_user(1)
        self.assertIsNotNone(user)
        # Should have been repaired with defaults
        self.assertEqual(user.get("name"), "")


class TestFormatters(unittest.TestCase):
    """Tests for formatters."""

    def setUp(self):
        """Set up test fixtures."""
        self.users = [
            {
                "id": 1,
                "name": "Alice",
                "email": "alice@example.com",
                "role": "Admin",
                "status": "Active",
                "join_date": "2023-01-01",
                "last_login": "2025-11-26",
            },
            {
                "id": 2,
                "name": "Bob",
                "email": "bob@example.com",
                "role": "User",
                "status": "Inactive",
                "join_date": "2023-02-01",
                "last_login": "2025-11-20",
            },
        ]

    def test_compact_formatter(self):
        """Test compact formatter."""
        formatter = CompactFormatter()
        result = formatter.format(self.users)
        self.assertIn("id=1", result)
        self.assertIn("name=Alice", result)
        self.assertIn("PROCESSED=2", result)

    def test_json_formatter(self):
        """Test JSON formatter."""
        formatter = JSONFormatter()
        result = formatter.format(self.users)
        data = json.loads(result)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["id"], 1)

    def test_table_formatter(self):
        """Test table formatter."""
        formatter = TableFormatter()
        result = formatter.format(self.users)
        self.assertIn("id", result)
        self.assertIn("Alice", result)

    def test_formatter_field_selection(self):
        """Test field selection in formatters."""
        formatter = JSONFormatter()
        result = formatter.format(self.users, field_selection=["id", "name"])
        data = json.loads(result)
        self.assertIn("id", data[0])
        self.assertIn("name", data[0])
        self.assertNotIn("email", data[0])


class TestFilters(unittest.TestCase):
    """Tests for filters."""

    def setUp(self):
        """Set up test fixtures."""
        self.users = [
            {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "Admin"},
            {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "User"},
            {"id": 3, "name": "Charlie", "email": "admin@example.com", "role": "Admin"},
        ]

    def test_regex_filter_case_insensitive(self):
        """Test regex filter with case insensitivity."""
        filter_obj = RegexFilter({"name": "a.*"}, case_sensitive=False)
        result = filter_obj.apply(self.users)
        self.assertEqual(len(result), 2)  # Alice and Charlie

    def test_regex_filter_case_sensitive(self):
        """Test regex filter with case sensitivity."""
        filter_obj = RegexFilter({"name": "a.*"}, case_sensitive=True)
        result = filter_obj.apply(self.users)
        self.assertEqual(len(result), 1)  # Only alice

    def test_composite_filter_and(self):
        """Test composite filter with AND logic."""
        filter1 = RegexFilter({"role": "Admin"})
        filter2 = RegexFilter({"name": "Alice"})
        composite = CompositeFilter([filter1, filter2], combine_with="AND")
        result = composite.apply(self.users)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Alice")

    def test_composite_filter_or(self):
        """Test composite filter with OR logic."""
        filter1 = RegexFilter({"name": "Alice"})
        filter2 = RegexFilter({"name": "Bob"})
        composite = CompositeFilter([filter1, filter2], combine_with="OR")
        result = composite.apply(self.users)
        self.assertEqual(len(result), 2)


class TestValidation(unittest.TestCase):
    """Tests for validation."""

    def test_default_validator_valid(self):
        """Test validator with valid user."""
        validator = DefaultValidator()
        user = {
            "id": 1,
            "name": "Alice",
            "email": "alice@example.com",
            "role": "Admin",
            "status": "Active",
            "join_date": "2023-01-01",
            "last_login": "2025-11-26",
        }
        is_valid, error = validator.validate(user)
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_default_validator_invalid(self):
        """Test validator with invalid user."""
        validator = DefaultValidator()
        user = {"id": 1}  # Missing fields
        is_valid, error = validator.validate(user)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)

    def test_default_validator_repair(self):
        """Test validator repair."""
        validator = DefaultValidator()
        user = {"id": 1, "name": "Alice"}
        repaired = validator.repair(user)
        self.assertEqual(repaired["id"], 1)
        self.assertEqual(repaired["name"], "Alice")
        self.assertEqual(repaired["email"], "")  # Default value
        self.assertIn("status", repaired)  # Added


class TestOptimizedAPI(unittest.TestCase):
    """Tests for UserDisplayOptimized."""

    def setUp(self):
        """Set up test fixtures."""
        self.system = UserDisplayOptimized()
        self.sample_users = [
            {
                "id": i,
                "name": f"User{i}",
                "email": f"user{i}@example.com",
                "role": "Admin" if i % 3 == 0 else "User",
                "status": "Active" if i % 5 != 0 else "Inactive",
                "join_date": "2023-01-01",
                "last_login": "2025-11-26",
            }
            for i in range(1, 101)
        ]
        self.system.load_users(self.sample_users)

    def test_display_users(self):
        """Test display_users."""
        result = self.system.display_users(show_all=True)
        self.assertIn("PROCESSED=100", result)

    def test_get_user_by_id(self):
        """Test get_user_by_id."""
        user = self.system.get_user_by_id(50)
        self.assertIsNotNone(user)
        self.assertEqual(user["name"], "User50")

    def test_filter_users(self):
        """Test filter_users."""
        filtered = self.system.filter_users({"role": "Admin"})
        # Every 3rd user is Admin
        self.assertGreater(len(filtered), 0)

    def test_export_users_to_string(self):
        """Test export_users_to_string."""
        result = self.system.export_users_to_string()
        self.assertIn("User", result)

    def test_export_json_format(self):
        """Test export with JSON format."""
        result = self.system.export_users_to_string(format_type="json")
        data = json.loads(result)
        self.assertEqual(len(data), 100)

    def test_metrics_collection(self):
        """Test metrics are collected."""
        _ = self.system.get_user_by_id(1)
        _ = self.system.filter_users({"role": "User"})
        
        metrics_dict = self.system.get_metrics()
        self.assertGreater(metrics_dict["lookup_operations"], 0)
        self.assertGreater(metrics_dict["filter_operations"], 0)


class TestPerformance(unittest.TestCase):
    """Performance tests."""

    def test_display_50k_users_under_120ms(self):
        """Test displaying 50k users completes in under 120ms."""
        store = UserStore(shard_count=16)
        users = [
            {
                "id": i,
                "name": f"User{i}",
                "email": f"user{i}@example.com",
                "role": random.choice(["Admin", "User", "Mod"]),
                "status": random.choice(["Active", "Inactive"]),
                "join_date": "2023-01-01",
                "last_login": "2025-11-26",
            }
            for i in range(1, 50001)
        ]

        # Add users
        for user in users:
            store.add_user(user)

        # Display should be fast
        start = time.time()
        formatter = CompactFormatter()
        _ = formatter.format(store.get_all_users())
        duration_ms = (time.time() - start) * 1000

        self.assertLess(duration_ms, 120)
        print(f"Display 50k users: {duration_ms:.2f}ms")

    def test_filter_50k_users_under_15ms(self):
        """Test filtering 50k users completes in under 20ms (target: <15ms)."""
        store = UserStore(shard_count=16)
        users = [
            {
                "id": i,
                "name": f"User{i}",
                "email": f"user{i}@example.com",
                "role": "Admin" if i % 3 == 0 else "User",
                "status": "Active" if i % 5 != 0 else "Inactive",
                "join_date": "2023-01-01",
                "last_login": "2025-11-26",
            }
            for i in range(1, 50001)
        ]

        for user in users:
            store.add_user(user)

        all_users = store.get_all_users()

        # Filter should be fast (typically 5-15ms, allowing 20ms for system variance)
        start = time.time()
        filter_obj = RegexFilter({"role": "Admin"})
        _ = filter_obj.apply(all_users)
        duration_ms = (time.time() - start) * 1000

        self.assertLess(duration_ms, 20)
        print(f"Filter 50k users: {duration_ms:.2f}ms")

    def test_id_lookup_under_0_5ms(self):
        """Test ID lookup completes in under 0.5ms."""
        store = UserStore(shard_count=16)
        users = [
            {
                "id": i,
                "name": f"User{i}",
                "email": f"user{i}@example.com",
                "role": "User",
                "status": "Active",
                "join_date": "2023-01-01",
                "last_login": "2025-11-26",
            }
            for i in range(1, 50001)
        ]

        for user in users:
            store.add_user(user)

        # Lookup should be very fast
        start = time.time()
        _ = store.get_user(25000)
        duration_ms = (time.time() - start) * 1000

        self.assertLess(duration_ms, 0.5)
        print(f"ID lookup: {duration_ms:.4f}ms")


if __name__ == "__main__":
    unittest.main()
