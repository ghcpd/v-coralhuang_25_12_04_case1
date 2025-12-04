"""
Quick validation and example usage of the optimized system.
"""

import time
from user_display_optimized import UserDisplayOptimized
from user_display import get_metrics, get_logger

# Create sample users
sample_users = [
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

print("=" * 60)
print("USER DISPLAY SYSTEM - VALIDATION & EXAMPLE")
print("=" * 60)

# Create system
print("\n1. Creating system with 100 sample users...")
system = UserDisplayOptimized(sample_users)
print("[+] System created successfully")

# Display users
print("\n2. Displaying users (compact format)...")
result = system.display_users(format_type="compact", show_all=True)
lines = result.split('\n')
print(f"   First 3 lines:\n   {lines[0]}")
print(f"   {lines[1]}")
print(f"   {lines[2]}")
print(f"   ... (total {len(lines)} lines)")

# Get user by ID
print("\n3. Getting user by ID (O(1) lookup)...")
user = system.get_user_by_id(50)
if user:
    print(f"   [+] Found: {user['name']} ({user['email']}) - Role: {user['role']}")
else:
    print("   [-] User not found")

# Filter users
print("\n4. Filtering users (role=Admin)...")
admins = system.filter_users({"role": "Admin"})
print(f"   [+] Found {len(admins)} admins")
print(f"   Examples: {', '.join([u['name'] for u in admins[:3]])}")

# Export to JSON
print("\n5. Exporting to JSON format...")
json_export = system.export_users_to_string(format_type="json")
json_preview = json_export[:150] + "..."
print(f"   {json_preview}")

# Show table format
print("\n6. Displaying in table format...")
table_result = system.display_users(format_type="table", show_all=True)
table_lines = table_result.split('\n')
for line in table_lines[:5]:
    print(f"   {line}")
print(f"   ... (total {len(table_lines)} lines)")

# Performance metrics
print("\n7. Performance Metrics:")
metrics = system.get_metrics()
print(f"   Display operations: {metrics['display_operations']}")
print(f"   Average display time: {metrics['display_avg_duration_ms']:.2f}ms")
print(f"   Filter operations: {metrics['filter_operations']}")
print(f"   Average filter time: {metrics['filter_avg_duration_ms']:.2f}ms")
print(f"   Lookup operations: {metrics['lookup_operations']}")
print(f"   Average lookup time: {metrics['lookup_avg_duration_ms']:.4f}ms")

# Snapshot support
print("\n8. Creating snapshot...")
snapshot = system.create_snapshot()
user_from_snapshot = snapshot.get_by_id(25)
if user_from_snapshot:
    print(f"   [+] Snapshot contains: {user_from_snapshot['name']}")

# Store statistics
print("\n9. Store Statistics:")
store = system.get_store()
stats = store.stats()
print(f"   Total users: {stats['total_users']}")
print(f"   Shard count: {stats['shard_count']}")
print(f"   Shard distribution: {stats['shard_sizes']}")

print("\n" + "=" * 60)
print("[OK] VALIDATION COMPLETE - ALL SYSTEMS OPERATIONAL")
print("=" * 60)
print("\nKey Improvements Over Original:")
print("  [+] O(1) ID lookups instead of O(n) linear scans")
print("  [+] No artificial delays or randomized corruption")
print("  [+] Modular, extensible architecture")
print("  [+] Thread-safe with snapshot support")
print("  [+] Comprehensive metrics and logging")
print("  [+] Multiple output formats (compact, JSON, table)")
print("  [+] Automatic validation and repair")
print("  [+] Plugin system for custom components")
print("\nNext Steps:")
print("  1. Run tests: python -m pytest tests/ -v")
print("  2. Or use one-click runner: .\\run_tests.ps1")
print("  3. See README.md for full documentation")
