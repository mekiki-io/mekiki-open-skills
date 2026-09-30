from typing import final

from catalog.catalog import Catalog
from catalog.category import Category
from catalog.check import Check


@final
class ReferencesCheck(Check):
    def __init__(self, catalog: Catalog) -> None:
        self._catalog = catalog

    def problems(self) -> list[str]:
        return [
            problem
            for category in self._catalog.categories()
            for problem in self._category(category)
        ]

    def _category(self, category: Category) -> list[str]:
        skills = category.document()["skills"]
        problems: list[str] = []
        for key, skill in skills.items():
            for field in ("prerequisites", "related"):
                place = f"{category.id()}.yaml: {key}: {field} item"
                targets = skill.get(field, [])
                problems += [
                    f"{place} '{t}' is the skill itself" for t in targets if t == key
                ]
                problems += [
                    f"{place} '{t}' is not a skill in this file"
                    for t in targets
                    if t not in skills
                ]
        return problems
