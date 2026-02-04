# simple plugin registry
_filters = {}
_formatters = {}
_validators = {}

def register_filter(name, factory):
    _filters[name] = factory

def get_filter(name):
    return _filters.get(name)

def register_formatter(name, factory):
    _formatters[name] = factory

def get_formatter(name):
    return _formatters.get(name)

def register_validator(name, factory):
    _validators[name] = factory

def get_validator(name):
    return _validators.get(name)
