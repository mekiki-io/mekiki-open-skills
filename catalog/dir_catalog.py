from pathlib import Path
from typing import final

from catalog.catalog import Catalog
from catalog.category import Category
from catalog.strict_category import StrictCategory
from catalog.yaml_category import YamlCategory


@final
class DirCatalog(Catalog):
    def __init__(self, directory: Path) -> None:
        self._directory = directory

    def categories(self) -> list[Category]:
        if not self._directory.is_dir():
            raise Exception(f"'{self._directory}' is not a directory with skills")
        return [
            StrictCategory(YamlCategory(path), path)
            for path in sorted(self._directory.glob("*.yaml"))
        ]
