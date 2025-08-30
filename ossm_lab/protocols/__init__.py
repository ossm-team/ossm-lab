# ossm_lab/protocols/__init__.py
# Import built-ins so they self-register at import time.
# Keep these imports lightweight; factories do heavy imports lazily.
from . import representation  # noqa: F401
from . import misc
from . import dynamics

__all__ = ["representation"]
