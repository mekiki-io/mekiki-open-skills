from pathlib import Path

from hamcrest import assert_that, equal_to

from catalog.build_command import BuildCommand
from tests.fakes import FakeRelease


def test_writes_release_into_file(tmp_path: Path) -> None:
    BuildCommand(
        FakeRelease('{"skills": "✓ ünïcode"}\n'), tmp_path / "skills.json"
    ).run()
    assert_that(
        (tmp_path / "skills.json").read_text(encoding="utf-8"),
        equal_to('{"skills": "✓ ünïcode"}\n'),
        "file must contain the release text in UTF-8",
    )
