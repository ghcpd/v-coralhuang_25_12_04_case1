from collections import Counter

_metrics = Counter()

def incr(name, n=1):
    _metrics[name] += n

def get_metrics():
    return dict(_metrics)

def reset_metrics():
    _metrics.clear()
