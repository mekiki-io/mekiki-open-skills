from pathlib import Path

import pytest
from hamcrest import assert_that, equal_to

from catalog.strict_category import StrictCategory
from tests.fakes import FakeCategory


def test_gives_document_of_origin_when_keys_are_unique(tmp_path: Path) -> None:
    path = tmp_path / "go.yaml"
    path.write_text(
        "name: Go\nskills:\n  goroutines:\n    name: Goroutines\n", encoding="utf-8"
    )
    assert_that(
        StrictCategory(FakeCategory("go", {"🦫": ["chan"]}), path).document(),
        equal_to({"🦫": ["chan"]}),
        "document must come from the origin category",
    )


def test_gives_id_of_origin(tmp_path: Path) -> None:
    assert_that(
        StrictCategory(FakeCategory("c-sharp", {}), tmp_path / "other.yaml").id(),
        equal_to("c-sharp"),
        "id must come from the origin category",
    )


def test_refuses_duplicate_skill_key(tmp_path: Path) -> None:
    path = tmp_path / "rust.yaml"
    path.write_text(
        "skills:\n  borrow:\n    name: A\n  borrow:\n    name: B\n", encoding="utf-8"
    )
    with pytest.raises(Exception, match=r"rust\.yaml: duplicate key 'borrow'"):
        StrictCategory(FakeCategory("rust", {}), path).document()


def test_refuses_duplicate_key_nested_in_list(tmp_path: Path) -> None:
    path = tmp_path / "zig.yaml"
    path.write_text("aliases:\n  - {x: 1, x: 2}\n", encoding="utf-8")
    with pytest.raises(Exception, match="duplicate key 'x'"):
        StrictCategory(FakeCategory("zig", {}), path).document()


def test_refuses_key_that_yaml_reads_as_boolean(tmp_path: Path) -> None:
    path = tmp_path / "elixir.yaml"
    path.write_text("skills:\n  on:\n    name: On\n", encoding="utf-8")
    with pytest.raises(
        Exception, match=r"elixir\.yaml: line 2: key 'on' is not a string"
    ):
        StrictCategory(FakeCategory("elixir", {}), path).document()


def test_refuses_broken_yaml_naming_the_file(tmp_path: Path) -> None:
    path = tmp_path / "kotlin.yaml"
    path.write_text("skills: {coroutines\n", encoding="utf-8")
    with pytest.raises(Exception, match=r"kotlin\.yaml"):
        StrictCategory(FakeCategory("kotlin", {}), path).document()
