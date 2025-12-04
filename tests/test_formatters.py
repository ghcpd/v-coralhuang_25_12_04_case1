from user_display.formatters.compact import CompactFormatter
from user_display.formatters.json_fmt import JSONFormatter
from user_display.formatters.table import TableFormatter


def test_compact_formatter(sample_users):
    f = CompactFormatter()
    out = f.format(sample_users[:5])
    assert "ID" not in out  # uses lower-case keys
    assert "User1" in out


def test_json_formatter(sample_users):
    f = JSONFormatter()
    out = f.format(sample_users[:3])
    assert out.startswith("{") and out.endswith("}")
    assert '"count": 3' in out


def test_table_formatter(sample_users):
    f = TableFormatter()
    out = f.format(sample_users[:3])
    assert "id" in out.splitlines()[0]
    assert "User1" in out
