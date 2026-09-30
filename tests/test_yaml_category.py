from pathlib import Path

import pytest
from hamcrest import assert_that, equal_to

from catalog.yaml_category import YamlCategory


def test_takes_id_from_file_name(tmp_path: Path) -> None:
    assert_that(
        YamlCategory(tmp_path / "soft-skills.yaml").id(),
        equal_to("soft-skills"),
        "id must be the file name without extension",
    )


def test_reads_unicode_document(tmp_path: Path) -> None:
    path = tmp_path / "python.yaml"
    path.write_text("name: Пайтон 🐍\nskills: {}\n", encoding="utf-8")
    assert_that(
        YamlCategory(path).document(),
        equal_to({"name": "Пайтон 🐍", "skills": {}}),
        "document must keep unicode text as written",
    )


def test_refuses_broken_yaml_naming_the_file(tmp_path: Path) -> None:
    path = tmp_path / "ruby.yaml"
    path.write_text("name: [Ruby\n", encoding="utf-8")
    with pytest.raises(Exception, match=r"ruby\.yaml"):
        YamlCategory(path).document()
