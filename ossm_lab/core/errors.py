class RegistryError(Exception):
    pass


class DuplicateNameError(RegistryError):
    pass


class NotFoundError(RegistryError):
    pass


class InvalidMetaError(RegistryError):
    pass
