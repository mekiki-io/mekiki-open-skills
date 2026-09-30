from typing import final

from catalog.check import Check


@final
class StagedChecks(Check):
    def __init__(self, checks: list[Check]) -> None:
        self._checks = checks

    def problems(self) -> list[str]:
        return next(
            (
                problems
                for problems in (check.problems() for check in self._checks)
                if problems
            ),
            [],
        )
