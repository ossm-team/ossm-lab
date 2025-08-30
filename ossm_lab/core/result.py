import abc


class BaseResult(abc.ABC):
    """ Result of applying a protocol to a model. """

    def __init__(self, success: bool, data: dict):
        self.success = success
        self.data = data

    @abc.abstractmethod
    def __repr__(self): pass

    def __bool__(self):
        return self.success


class Result(BaseResult):
    """ Result of applying a protocol to a model. """

    def __repr__(self):
        return f"<Result success={self.success} data_keys={list(self.data.keys())}>"