from ossm_lab.core.registry import ProtocolMeta, registry, load_entry_points


def test_entry_point_loading(monkeypatch):
    # Fake entry point object
    class EP:
        def __init__(self, load_fn):
            self._load_fn = load_fn
        def load(self):
            return self._load_fn

    # Provider returns a list of metas
    def provider():
        return [ProtocolMeta(
            name="representation.from_ep",
            version="0.1.0",
            family="representation",
            entry=lambda *, config=None: {"ep": True},
        )]

    # Monkeypatch importlib.metadata.entry_points(...) to return our fake EP list
    import ossm_lab.core.registry as reg
    monkeypatch.setattr(reg, "entry_points", lambda *a, **k: [EP(provider)])

    count = load_entry_points()
    assert count == 1
    assert "representation.from_ep" in {m.name for m in registry.list()}


def test_entry_point_idempotent(monkeypatch):
    # same as above but ensure second call returns 0
    class EP:
        def __init__(self, load_fn):
            self._load_fn = load_fn
        def load(self):
            return self._load_fn

    def provider():
        return [ProtocolMeta(
            name="representation.once",
            version="0.1.0",
            family="representation",
            entry=lambda *, config=None: {"ok": 1},
        )]

    import ossm_lab.core.registry as reg
    monkeypatch.setattr(reg, "entry_points", lambda *a, **k: [EP(provider)])

    assert load_entry_points() == 1
    assert load_entry_points() == 0
