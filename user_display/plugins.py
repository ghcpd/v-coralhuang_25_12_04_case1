_REG = {"formatters": {}, "filters": {}, "validators": {}}

def register(kind, name, obj):
    _REG.setdefault(kind, {})[name] = obj

def get(kind, name):
    return _REG.get(kind, {}).get(name)

def list_all():
    return {k: list(v.keys()) for k, v in _REG.items()}
