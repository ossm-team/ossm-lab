from ...core.result import BaseResult
from ...core.decorators import register_protocol
from ...core.protocol import Protocol
from ...core.result import Result


@register_protocol(
    name="misc.dummy",
    version="0.1.0",
    family="misc",
    authors="OSSM Team",
    aliases=["dummy", "test"],
)
class Dummy(Protocol):
    """ Dummy implementation of a protocol. """

    def run(self, model) -> BaseResult:
        analysis_result = {}

        return Result(
            success=True,
            data=analysis_result
        )



