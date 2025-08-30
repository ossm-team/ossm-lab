import abc
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from ossm_lab.core.result import BaseResult


class Protocol(abc.ABC):
    """ Analysis protocol that can be applied to a model. """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}

    def __call__(self, model):
        """ Apply the protocol to a model and return a result. """
        return self.run(model)

    def run(self, model) -> BaseResult:
        raise NotImplementedError