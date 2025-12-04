from collections import Counter

_c = Counter()

def incr(key, n=1):
    _c[key] += n

def get_metrics():
    return dict(_c)
