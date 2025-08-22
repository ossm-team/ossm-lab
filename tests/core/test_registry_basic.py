import pytest

from ossm_lab.core.registry import (
    ProtocolMeta,
    registry,
    register,
    list_protocols,
    get,
    resolve,
)
from ossm_lab.core.errors import InvalidMetaError
from ossm_lab.core.errors import NotFoundError
from ossm_lab.core.errors import DuplicateNameError


def test_register_and_list():
    m = ProtocolMeta(
        name="representation.testproto",
        version="0.1.0",
        family="representation",
        entry=lambda *, config=None: {"ok": True, "config": config},
        aliases=["testproto"],
    )

    register(m)

    names = [x.name for x in list_protocols()]

    assert "representation.testproto" in names


def test_alias_resolution_and_get():
    m = ProtocolMeta(
        name="representation.aliasy",
        version="1.2.3",
        family="representation",
        entry=lambda *, config=None: {"name": "aliasy", "cfg": config or {}},
        aliases=["ali", "aliasy"],
    )

    register(m)

    assert resolve("ali") == "representation.aliasy"

    inst = get("ali", config={"x": 1})
    assert inst["name"] == "aliasy"
    assert inst["cfg"]["x"] == 1


def test_duplicate_registration_raises():
    m = ProtocolMeta(
        name="representation.dup",
        version="0.0.1",
        family="representation",
        entry=lambda *, config=None: object(),
    )

    register(m)

    with pytest.raises(DuplicateNameError):
        register(m)


@pytest.mark.parametrize("bad_name", ["RSA", "representation", "representation.", "rep..rsa", "representation/rsa"])
def test_validation_bad_name(bad_name):
    with pytest.raises(InvalidMetaError):
        register(ProtocolMeta(
            name=bad_name,
            version="0.1.0",
            family="representation",
            entry=lambda *, config=None: object(),
        ))



@pytest.mark.parametrize("bad_ver", ["1", "1.0", "one.two.three", "1.0.0.0"])
def test_validation_bad_semver(bad_ver):
    with pytest.raises(InvalidMetaError):
        register(ProtocolMeta(
            name="representation.v",
            version=bad_ver,
            family="representation",
            entry=lambda *, config=None: object(),
        ))


def test_not_found_on_get():
    with pytest.raises(NotFoundError):
        get("does.not.exist")
