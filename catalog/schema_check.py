import json
import re
from pathlib import Path
from typing import final

from jsonschema import Draft202012Validator

from catalog.catalog import Catalog
from catalog.category import Category
from catalog.check import Check


@final
class SchemaCheck(Check):
    def __init__(self, catalog: Catalog) -> None:
        self._catalog = catalog

    def problems(self) -> list[str]:
        schema = Draft202012Validator(
            json.loads(
                (Path(__file__).parent / "schema.json").read_text(encoding="utf-8")
            )
        )
        return [
            problem
            for category in self._catalog.categories()
            for problem in self._name(category) + self._content(category, schema)
        ]

    def _name(self, category: Category) -> list[str]:
        return [
            f"{category.id()}.yaml: file name must be lowercase words joined by '-'"
            for _ in [category]
            if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", category.id())
        ]

    def _content(self, category: Category, schema: Draft202012Validator) -> list[str]:
        return [
            f"{category.id()}.yaml: "
            f"{'/'.join(map(str, error.absolute_path)) or 'root'}: {error.message}"
            for error in sorted(
                schema.iter_errors(category.document()),
                key=lambda error: list(map(str, error.absolute_path)),
            )
        ]
