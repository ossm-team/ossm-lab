from typing import Any, Optional, Dict

from ...core.decorators import register_protocol

@register_protocol(
    name="representation.rsa",
    version="0.1.0",
    family="representation",
    authors="OSSM Team",
    aliases=["rsa"],
)
class RSAProtocol:

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}