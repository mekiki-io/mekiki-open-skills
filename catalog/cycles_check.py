from typing import Any, final

from catalog.catalog import Catalog
from catalog.check import Check


@final
class CyclesCheck(Check):
    def __init__(self, catalog: Catalog) -> None:
        self._catalog = catalog

    def problems(self) -> list[str]:
        return [
            f"{category.id()}.yaml: {cycle[0]}: prerequisites form a cycle "
            f"({' -> '.join([*cycle, cycle[0]])})"
            for category in self._catalog.categories()
            for cycle in self._cycles(category.document()["skills"])
        ]

    def _cycles(self, skills: dict[str, Any]) -> list[list[str]]:
        done: set[str] = set()
        cycles: list[list[str]] = []
        for key in skills:
            self._walk(skills, key, [], done, cycles)
        return cycles

    def _walk(
        self,
        skills: dict[str, Any],
        key: str,
        path: list[str],
        done: set[str],
        cycles: list[list[str]],
    ) -> None:
        if key in path:
            cycles.append(path[path.index(key) :])
        elif key not in done:
            for target in skills[key].get("prerequisites", []):
                self._walk(skills, target, [*path, key], done, cycles)
            done.add(key)
