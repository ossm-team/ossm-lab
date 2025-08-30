from ossm_lab.core.protocol import Protocol
from ossm_lab.core.registry import list_protocols, get
from ossm_lab.core.decorators import register_protocol


def test_register_protocol_decorator_registers_class():
    @register_protocol(
        name="representation.decorated",
        version="0.2.0",
        family="representation",
        aliases=["deco"],
    )
    class Dummy(Protocol):

        def __init__(self, config=None):
            self.config = config or {}

    names = [m.name for m in list_protocols()]
    assert "representation.decorated" in names

    inst = get("deco", config={"a": 1})
    assert isinstance(inst, Dummy)
    assert inst.config["a"] == 1
