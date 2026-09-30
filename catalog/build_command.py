from pathlib import Path
from typing import final

from catalog.command import Command
from catalog.release import Release


@final
class BuildCommand(Command):
    def __init__(self, release: Release, output: Path) -> None:
        self._release = release
        self._output = output

    def run(self) -> None:
        self._output.write_text(self._release.text(), encoding="utf-8")
