# ossm_lab/protocols/__init__.py
# Import built-ins so they self-register at import time.
# Keep these imports lightweight; factories do heavy imports lazily.
from . import representation  # noqa: F401

__all__ = ["representation"]
