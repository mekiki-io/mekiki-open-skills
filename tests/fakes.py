from typing import Any, final

from catalog.catalog import Catalog
from catalog.category import Category
from catalog.check import Check
from catalog.release import Release


@final
class FakeCategory(Category):
    def __init__(self, name: str, content: Any) -> None:
        self._name = name
        self._content = content

    def id(self) -> str:
        return self._name

    def document(self) -> Any:
        return self._content


@final
class FakeCatalog(Catalog):
    def __init__(self, items: list[Category]) -> None:
        self._items = items

    def categories(self) -> list[Category]:
        return self._items


@final
class FakeCheck(Check):
    def __init__(self, items: list[str]) -> None:
        self._items = items

    def problems(self) -> list[str]:
        return self._items


@final
class FakeRelease(Release):
    def __init__(self, content: str) -> None:
        self._content = content

    def text(self) -> str:
        return self._content
