""" Sample script to demonstrate the usage of the API. """

import ossm_lab
from ossm_lab.core.base import Visualization
from ossm_lab.core.result import BaseResult
from ossm_lab.core.protocol import Protocol

from ossm_lab.core.registry import list_protocols, get, load_entry_points

load_entry_points()           # discovers any third‑party plugins
print([m.name for m in list_protocols()])
proto = get("representation.rsa")            # alias resolution -> representation.rsa