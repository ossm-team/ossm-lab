from . import protocols
from .core.registry import registry, load_entry_points, get, list_protocols

# Load third‑party plugins once; ignore failures gracefully.
try:
    load_entry_points()
except Exception:
    pass

__all__ = ["registry", "load_entry_points"]
