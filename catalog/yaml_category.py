from pathlib import Path
from typing import Any, final

import yaml

from catalog.category import Category


@final
class YamlCategory(Category):
    def __init__(self, path: Path) -> None:
        self._path = path

    def id(self) -> str:
        return self._path.stem

    def document(self) -> Any:
        try:
            return yaml.safe_load(self._path.read_text(encoding="utf-8"))
        except yaml.YAMLError as error:
            raise Exception(f"{self._path.name}: {error}") from error
