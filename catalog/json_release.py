import json
from typing import Any, final

from catalog.catalog import Catalog
from catalog.category import Category
from catalog.release import Release
from catalog.version import Version


@final
class JsonRelease(Release):
    def __init__(self, catalog: Catalog, version: Version) -> None:
        self._catalog = catalog
        self._version = version

    def text(self) -> str:
        document = {
            "version": str(self._version),
            "categories": [
                self._category(category) for category in self._catalog.categories()
            ],
        }
        return json.dumps(document, ensure_ascii=False, indent=2) + "\n"

    def _category(self, category: Category) -> dict[str, Any]:
        document = category.document()
        return {
            "id": category.id(),
            "name": document["name"],
            "description": document["description"],
            "skills": [
                self._skill(key, skill) for key, skill in document["skills"].items()
            ],
        }

    def _skill(self, key: str, skill: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": key,
            "name": skill["name"],
            "level": skill["level"],
            "aliases": skill.get("aliases", []),
            "prerequisites": skill.get("prerequisites", []),
            "related": skill.get("related", []),
        }
