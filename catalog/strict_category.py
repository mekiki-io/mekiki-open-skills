from pathlib import Path
from typing import Any, final

import yaml
from yaml.nodes import MappingNode, Node, SequenceNode

from catalog.category import Category


@final
class StrictCategory(Category):
    def __init__(self, origin: Category, path: Path) -> None:
        self._origin = origin
        self._path = path

    def id(self) -> str:
        return self._origin.id()

    def document(self) -> Any:
        try:
            self._verify(yaml.compose(self._path.read_text(encoding="utf-8")))
        except yaml.YAMLError as error:
            raise Exception(f"{self._path.name}: {error}") from error
        return self._origin.document()

    def _verify(self, node: Node | None) -> None:
        if isinstance(node, MappingNode):
            self._verify_keys([key for key, _ in node.value])
            for _, value in node.value:
                self._verify(value)
        if isinstance(node, SequenceNode):
            for item in node.value:
                self._verify(item)

    def _verify_keys(self, keys: list[Node]) -> None:
        for key in keys:
            if key.tag != "tag:yaml.org,2002:str":
                raise Exception(
                    f"{self._path.name}: line {key.start_mark.line + 1}: "
                    f"key '{key.value}' is not a string, quote it"
                )
        names = [key.value for key in keys]
        for name in names:
            if names.count(name) > 1:
                raise Exception(f"{self._path.name}: duplicate key '{name}'")
