import importlib
import re
from dataclasses import dataclass, field, asdict
from typing import Any, Callable, Dict, Iterable, List, Optional

from importlib.metadata import entry_points, EntryPoints
from typing import Union

from ossm_lab.core.errors import DuplicateNameError
from ossm_lab.core.errors import InvalidMetaError
from ossm_lab.core.errors import NotFoundError
from ossm_lab.core.errors import RegistryError

NAME_RE = re.compile(r"^[a-z0-9-_]+(\.[a-z0-9-_]+)+$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+([+-].+)?$")


@dataclass(frozen=True)
class ProtocolMeta:
    """ Metadata for a Protocol factory."""

    name: str
    version: str
    family: str
    entry: Union[str, Callable[..., Any]]                       # "module.sub:factory" or a callable factory
    authors: Optional[str] = None
    license: Optional[str] = None
    requires: List[str] = field(default_factory=list)           # extras / soft deps
    aliases: List[str] = field(default_factory=list)            # alternative names

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def validate(self) -> None:
        """ Validate basic sanity of a ProtocolMeta record. """

        if not NAME_RE.match(self.name):
            raise InvalidMetaError(f"Invalid name '{self.name}'. Expected something like 'representation.rsa'.")

        if not SEMVER_RE.match(self.version):
            raise InvalidMetaError(f"Invalid semver '{self.version}' for '{self.name}'.")

        if not (callable(self.entry) or (isinstance(self.entry, str) and ":" in self.entry)):
            raise InvalidMetaError(
                f"'entry' must be a callable factory or 'module.sub:factory', got {self.entry!r}."
            )


def _load_factory(entry: Union[str, Callable]) -> Callable[..., Any]:
    """ Load the factory function from the entry point or callable. """

    if callable(entry):
        return entry

    module_path, _, attr = entry.partition(":")
    mod = importlib.import_module(module_path)

    factory = getattr(mod, attr, None)

    if not callable(factory):
        raise InvalidMetaError(f"Entry '{entry}' is not a callable factory.")

    return factory


class _Registry:
    """In-memory registry of ProtocolMeta records with lazy factory import."""

    def __init__(self) -> None:
        self._by_name: Dict[str, ProtocolMeta] = {}
        self._aliases: Dict[str, str] = {}
        self._loaded_entry_points: bool = False

    def register(self, meta: ProtocolMeta) -> None:
        print(f"Registering protocol '{meta.name}' (version {meta.version})")

        meta.validate()

        if meta.name in self._by_name:
            raise DuplicateNameError(f'Protocol name "{meta.name}" is already registered.')

        self._by_name[meta.name] = meta

        for a in meta.aliases:
            self._aliases[a] = meta.name

    def list(self) -> List[ProtocolMeta]:
        """ List all registered protocol records"""

        metas = list(self._by_name.values())
        return sorted(metas, key=lambda m: m.name)

    def resolve(self, name_or_alias: str) -> str:
        """ Resolve a protocol name or alias to its canonical name. """

        return self._aliases.get(name_or_alias, name_or_alias)

    def get(self, name: str, *, config: Optional[Dict[str, Any]] = None) -> Any:
        """Instantiate a Protocol via its factory. Lazy‑imports the factory."""

        canon = self.resolve(name)
        meta = self._by_name.get(canon)

        if not meta:
            raise NotFoundError(f"Unknown protocol '{name}'")

        factory = _load_factory(meta.entry)

        try:
            return factory(config=config) if config is not None else factory()
        except ImportError as e:
            hint = f"Required extras not available for '{meta.name}'. Missing: {meta.requires or 'unknown'}."
            raise RegistryError(f"Failed to instantiate '{meta.name}': {e}\n{hint}") from e

    def load_entry_points(self, *, group: str = "ossm_lab.protocols") -> int:
        """ Discover third‑party plugins via entry points. Idempotent. """

        if self._loaded_entry_points:
            return 0

        if entry_points is None:
            return 0

        count = 0

        try:
            eps = entry_points(group=group)
        except TypeError:  # Python <3.12 compatibility
            eps_all = entry_points()
            eps = eps_all.get(group, [])

        def _iter(ep_container: EntryPoints | Iterable[Any]) -> Iterable[Any]:
            try:
                return list(ep_container)  # Py3.12 EntryPoints is iterable
            except:
                return ep_container

        for ep in _iter(eps):
            record_provider = ep.load()
            records: List[ProtocolMeta] = record_provider()

            for m in records:
                # Allow plugins to override only themselves via higher version;
                # otherwise, require distinct names.
                self.register(m)
                count += 1

        self._loaded_entry_points = True

        return count


# Module‑level singleton
registry = _Registry()

# Convenience top‑level functions
register = registry.register
list_protocols = registry.list
get = registry.get
resolve = registry.resolve
load_entry_points = registry.load_entry_points
