import pytest

from ossm_lab.core.registry import _load_factory
from ossm_lab.core.registry import ProtocolMeta, register, get
from ossm_lab.core.errors import InvalidMetaError


def test_dotted_entry_imports_on_get(make_dummy_module, monkeypatch):
    # Create a dummy module that tracks import side effect
    side_effect = {"imported": False}
    def factory(*, config=None):
        return {"ok": True}

    mod = make_dummy_module("dummy_pkg.rsa", build=factory)

    # Simulate a side effect on import
    def _import_hook(name, package=None):
        if name == "dummy_pkg.rsa":
            side_effect["imported"] = True
        return original_import(name, package=package)

    meta = ProtocolMeta(
        name="representation.dotted",
        version="0.1.0",
        family="representation",
        entry="dummy_pkg.rsa:build",
    )

    register(meta)

    # Ensure not imported yet (lazy)
    assert side_effect["imported"] is False

    # Patch importlib.import_module to flip the flag
    import ossm_lab.core.registry as reg
    original_import = reg.importlib.import_module
    monkeypatch.setattr(reg.importlib, "import_module", _import_hook)

    inst = get("representation.dotted")
    assert inst["ok"] is True
    assert side_effect["imported"] is True


def test_invalid_dotted_entry_raises(make_dummy_module):
    make_dummy_module("dummy_pkg.bad", no_factory=object())
    meta = ProtocolMeta(
        name="representation.bad",
        version="0.1.0",
        family="representation",
        entry="dummy_pkg.bad:missing",
    )

    # Registration is fine; failure occurs at load
    from ossm_lab.core.registry import registry
    registry.register(meta)
    with pytest.raises(InvalidMetaError):
        _load_factory(meta.entry)
