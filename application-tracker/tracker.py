
from pathlib import Path
from typing import Any, Dict, NamedTuple, List
from src.database import DatabaseHandler
from src import DB_READ_ERROR, ID_ERROR


class CurrentApplication(NamedTuple):
    application: Dict[str, Any]
    error: int


class Applier:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def add(self, title: str, description: List[str]) -> CurrentApplication:
        desc_text = " ".join(description)
        if not desc_text.endswith("."):
            desc_text += "."
        application = {
            "title": title,
            "description": desc_text
        }
        read = self._db_handler.read_applications()
        if read.error == DB_READ_ERROR:
            return CurrentApplication(application, read.error)
        read.application_list.append(application)
        write = self._db_handler.write_applications(read.application_list)
        return CurrentApplication(application, write.error)

    def remove(self, app_id: int) -> CurrentApplication:
        read = self._db_handler.read_applications()
        if read.error:
            return CurrentApplication({}, read.error)
        try:
            application = read.application_list.pop(app_id - 1)
        except IndexError:
            return CurrentApplication({}, ID_ERROR)
        write = self._db_handler.write_applications(read.application_list)
        return CurrentApplication(application, write.error)

    def get_application_list(self) -> List[Dict[str, Any]]:
        read = self._db_handler.read_applications()
        return read.application_list

