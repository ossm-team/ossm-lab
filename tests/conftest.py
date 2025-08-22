import types
import sys
import importlib
import pytest

from ossm_lab.core import registry as reg_mod


@pytest.fixture(autouse=True)
def _clean_registry_state():
    # snapshot
    by_name = dict(reg_mod.registry._by_name)
    aliases = dict(reg_mod.registry._aliases)
    loaded = reg_mod.registry._loaded_entry_points
    try:
        # clean
        reg_mod.registry._by_name.clear()
        reg_mod.registry._aliases.clear()
        reg_mod.registry._loaded_entry_points = False
        yield
    finally:
        # restore
        reg_mod.registry._by_name.clear()
        reg_mod.registry._by_name.update(by_name)
        reg_mod.registry._aliases.clear()
        reg_mod.registry._aliases.update(aliases)
        reg_mod.registry._loaded_entry_points = loaded


@pytest.fixture
def make_dummy_module(monkeypatch):
    """Create a temporary importable module with a given name and attributes."""
    created = []

    def _make(mod_name: str, **attrs):
        mod = types.ModuleType(mod_name)
        for k, v in attrs.items():
            setattr(mod, k, v)
        monkeypatch.setitem(sys.modules, mod_name, mod)
        created.append(mod_name)
        return mod
    return _make


@pytest.fixture
def reload_registry_module():
    """Force re-import of the registry module if a test needs a clean import state."""
    def _reload():
        return importlib.reload(reg_mod)
    return _reload
