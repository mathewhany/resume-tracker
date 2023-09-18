from io import StringIO
from .metrics import JSONMetricsManager


def test_json_metric_collector():
    file = StringIO()
    metrics = JSONMetricsManager(file)

    metrics.record_visit("resume", "source1")
    metrics.record_visit("resume", "source2")
    assert file.getvalue() == r'{"resume": {"source1": 1, "source2": 1}}'
    assert metrics.get_count("resume") == {"source1": 1, "source2": 1}
    assert metrics.get_count("another") == {}
    assert metrics.get_all_counts() == {"resume": {"source1": 1, "source2": 1}}

    metrics.record_visit("resume", "source1")
    assert file.getvalue() == r'{"resume": {"source1": 2, "source2": 1}}'
    assert metrics.get_count("resume") == {"source1": 2, "source2": 1}
    assert metrics.get_count("another") == {}
    assert metrics.get_all_counts() == {"resume": {"source1": 2, "source2": 1}}

    metrics.record_visit("resume", "source2")
    assert file.getvalue() == r'{"resume": {"source1": 2, "source2": 2}}'
    assert metrics.get_count("resume") == {"source1": 2, "source2": 2}
    assert metrics.get_count("another") == {}
    assert metrics.get_all_counts() == {"resume": {"source1": 2, "source2": 2}}

    metrics.record_visit("another", "source1")
    assert (
        file.getvalue()
        == r'{"resume": {"source1": 2, "source2": 2}, "another": {"source1": 1}}'
    )
    assert metrics.get_count("resume") == {"source1": 2, "source2": 2}
    assert metrics.get_count("another") == {"source1": 1}
    assert metrics.get_all_counts() == {
        "resume": {"source1": 2, "source2": 2},
        "another": {"source1": 1},
    }
