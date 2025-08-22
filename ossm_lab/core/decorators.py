from functools import wraps
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from ossm_lab.core.registry import ProtocolMeta, register, registry


def register_protocol(
    *,
    name: str,
    version: str,
    family: str,
    authors: Optional[str] = None,
    requires: Optional[List[str]] = None,
    aliases: Optional[List[str]] = None,
):
    """
    Class decorator that registers a Protocol implementation.

    The decorated class must be instantiable as `cls(config: dict | None = None)`.
    Produces a tiny factory: lambda config=None: cls(config or {}), and registers it.
    """

    def decorator(cls):
        # make a stable factory (keeps imports light; heavy deps remain in cls.__init__/run)

        @wraps(cls)
        def _factory(*, config: Optional[Dict[str, Any]] = None):
            return cls(config or {})

        meta = ProtocolMeta(
            name=name,
            version=version,
            family=family,
            authors=authors,
            entry=_factory,
            requires=list(requires or []),
            aliases=list(aliases or []),
        )

        registry.register(meta)

        return cls

    return decorator
