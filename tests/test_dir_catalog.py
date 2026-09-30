from pathlib import Path

import pytest
from hamcrest import assert_that, contains_exactly, has_length

from catalog.dir_catalog import DirCatalog


def test_orders_categories_by_file_name(tmp_path: Path) -> None:
    (tmp_path / "zeta.yaml").write_text("", encoding="utf-8")
    (tmp_path / "alpha.yaml").write_text("", encoding="utf-8")
    (tmp_path / "m-2.yaml").write_text("", encoding="utf-8")
    assert_that(
        [category.id() for category in DirCatalog(tmp_path).categories()],
        contains_exactly("alpha", "m-2", "zeta"),
        "categories must be ordered by id to give a stable release",
    )


def test_ignores_files_that_are_not_yaml(tmp_path: Path) -> None:
    (tmp_path / "notes.md").write_text("# notes", encoding="utf-8")
    (tmp_path / "old.yml").write_text("name: Old", encoding="utf-8")
    (tmp_path / "haskell.yaml").write_text("name: Haskell", encoding="utf-8")
    assert_that(
        DirCatalog(tmp_path).categories(),
        has_length(1),
        "only *.yaml files are categories",
    )


def test_refuses_missing_directory(tmp_path: Path) -> None:
    with pytest.raises(Exception, match="nowhere"):
        DirCatalog(tmp_path / "nowhere").categories()
