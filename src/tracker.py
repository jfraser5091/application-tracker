
from pathlib import Path
from typing import Any, Dict, NamedTuple
from database import DatabaseHandler


class CurrentApplication(NamedTuple):
    application: Dict[str, Any]
    error: int


class Applier:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

