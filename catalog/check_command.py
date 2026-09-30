from typing import final

from catalog.catalog import Catalog
from catalog.command import Command


@final
class CheckCommand(Command):
    def __init__(self, catalog: Catalog) -> None:
        self._catalog = catalog

    def run(self) -> None:
        self._catalog.categories()
