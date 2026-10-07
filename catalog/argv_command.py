from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import final

from catalog.build_command import BuildCommand
from catalog.check_command import CheckCommand
from catalog.checked_catalog import CheckedCatalog
from catalog.command import Command
from catalog.cycles_check import CyclesCheck
from catalog.dir_catalog import DirCatalog
from catalog.json_release import JsonRelease
from catalog.kept_keys_check import KeptKeysCheck
from catalog.references_check import ReferencesCheck
from catalog.schema_check import SchemaCheck
from catalog.staged_checks import StagedChecks
from catalog.version import Version


@final
class ArgvCommand(Command):
    def __init__(self, argv: list[str]) -> None:
        self._argv = argv

    def run(self) -> None:
        arguments = self._parser().parse_args(self._argv)
        arguments.command(arguments).run()

    def _parser(self) -> ArgumentParser:
        parser = ArgumentParser(prog="python -m catalog")
        commands = parser.add_subparsers(required=True)
        check = commands.add_parser("check", help="validate skills")
        check.add_argument("--source", type=Path, required=True)
        check.add_argument(
            "--previous", type=Path, required=True, help="previous release"
        )
        check.set_defaults(command=self._check)
        build = commands.add_parser(
            "build", help="validate skills and write skills.json"
        )
        build.add_argument("--source", type=Path, required=True)
        build.add_argument("--version", required=True, help="git tag, like 1.4.0")
        build.add_argument("--output", type=Path, required=True)
        build.set_defaults(command=self._build)
        return parser

    def _check(self, arguments: Namespace) -> Command:
        source = DirCatalog(arguments.source)
        return CheckCommand(
            CheckedCatalog(
                source,
                StagedChecks(
                    [
                        SchemaCheck(source),
                        ReferencesCheck(source),
                        CyclesCheck(source),
                        KeptKeysCheck(source, DirCatalog(arguments.previous)),
                    ]
                ),
            )
        )

    def _build(self, arguments: Namespace) -> Command:
        source = DirCatalog(arguments.source)
        return BuildCommand(
            JsonRelease(
                CheckedCatalog(
                    source,
                    StagedChecks(
                        [
                            SchemaCheck(source),
                            ReferencesCheck(source),
                            CyclesCheck(source),
                        ]
                    ),
                ),
                Version(arguments.version),
            ),
            arguments.output,
        )
