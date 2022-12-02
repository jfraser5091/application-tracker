
from typing import Any, Dict, NamedTuple


class CurrentApplication(NamedTuple):
    todo: Dict[str, Any]
    error: int
