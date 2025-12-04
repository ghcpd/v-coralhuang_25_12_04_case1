class UserDisplayError(Exception):
    pass


class ValidationError(UserDisplayError):
    pass


class PluginError(UserDisplayError):
    pass


class ConfigError(UserDisplayError):
    pass
