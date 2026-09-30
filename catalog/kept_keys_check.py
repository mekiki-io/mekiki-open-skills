from typing import final

from catalog.catalog import Catalog
from catalog.check import Check


@final
class KeptKeysCheck(Check):
    def __init__(self, catalog: Catalog, previous: Catalog) -> None:
        self._catalog = catalog
        self._previous = previous

    def problems(self) -> list[str]:
        return [
            f"{ref}: skill was removed or renamed, keys must never change"
            for ref in sorted(self._refs(self._previous) - self._refs(self._catalog))
        ]

    def _refs(self, catalog: Catalog) -> set[str]:
        return {
            f"{category.id()}.{key}"
            for category in catalog.categories()
            for key in category.document()["skills"]
        }
