import json
from pathlib import Path

import pytest
from hamcrest import assert_that, equal_to

from catalog.argv_command import ArgvCommand


def test_builds_release_of_repository_skills(tmp_path: Path) -> None:
    ArgvCommand(
        [
            "build",
            "--source",
            str(Path(__file__).parent.parent / "src"),
            "--version",
            "v9.8.7",
            "--output",
            str(tmp_path / "skills.json"),
        ]
    ).run()
    assert_that(
        json.loads((tmp_path / "skills.json").read_text(encoding="utf-8"))["version"],
        equal_to("9.8.7"),
        "skills of this repository must build into a release",
    )


def test_refuses_build_with_wrong_version(tmp_path: Path) -> None:
    with pytest.raises(Exception, match="'main' is not a version"):
        ArgvCommand(
            [
                "build",
                "--source",
                str(Path(__file__).parent.parent / "src"),
                "--version",
                "main",
                "--output",
                str(tmp_path / "never.json"),
            ]
        ).run()


def test_refuses_check_of_renamed_skill(tmp_path: Path) -> None:
    (tmp_path / "now").mkdir()
    (tmp_path / "before").mkdir()
    (tmp_path / "now" / "sql.yaml").write_text(
        "name: SQL\ndescription: Q.\nskills:\n"
        "  joins-2:\n    name: J\n    level: junior\n",
        encoding="utf-8",
    )
    (tmp_path / "before" / "sql.yaml").write_text(
        "name: SQL\ndescription: Q.\nskills:\n"
        "  joins:\n    name: J\n    level: junior\n",
        encoding="utf-8",
    )
    with pytest.raises(Exception, match=r"sql\.joins: skill was removed or renamed"):
        ArgvCommand(
            [
                "check",
                "--source",
                str(tmp_path / "now"),
                "--previous",
                str(tmp_path / "before"),
            ]
        ).run()


def test_refuses_check_of_duplicate_keys(tmp_path: Path) -> None:
    (tmp_path / "vue.yaml").write_text(
        "name: Vue\ndescription: V.\nskills:\n"
        "  refs:\n    name: R\n    level: junior\n"
        "  refs:\n    name: R2\n    level: junior\n",
        encoding="utf-8",
    )
    with pytest.raises(Exception, match=r"vue\.yaml: duplicate key 'refs'"):
        ArgvCommand(
            ["check", "--source", str(tmp_path), "--previous", str(tmp_path)]
        ).run()


def test_refuses_check_of_circular_prerequisites(tmp_path: Path) -> None:
    (tmp_path / "go.yaml").write_text(
        "name: Go\ndescription: G.\nskills:\n"
        "  chan:\n    name: C\n    level: middle\n    prerequisites: [select]\n"
        "  select:\n    name: S\n    level: middle\n    prerequisites: [chan]\n",
        encoding="utf-8",
    )
    with pytest.raises(Exception, match=r"go\.yaml: chan: prerequisites form a cycle"):
        ArgvCommand(
            ["check", "--source", str(tmp_path), "--previous", str(tmp_path)]
        ).run()
