import re
from typing import final


@final
class Version:
    def __init__(self, tag: str) -> None:
        self._tag = tag

    def __str__(self) -> str:
        version = self._tag.removeprefix("v")
        if not re.fullmatch(
            r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", version
        ):
            raise Exception(f"Tag '{self._tag}' is not a version like 1.4.0")
        return version
