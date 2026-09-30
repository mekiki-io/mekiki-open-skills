from typing import final

from catalog.catalog import Catalog
from catalog.category import Category
from catalog.check import Check


@final
class CheckedCatalog(Catalog):
    def __init__(self, origin: Catalog, check: Check) -> None:
        self._origin = origin
        self._check = check

    def categories(self) -> list[Category]:
        problems = self._check.problems()
        if problems:
            raise Exception("\n".join(problems))
        return self._origin.categories()
