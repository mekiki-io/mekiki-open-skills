import pytest
from hamcrest import assert_that, has_length

from catalog.checked_catalog import CheckedCatalog
from tests.fakes import FakeCatalog, FakeCategory, FakeCheck


def test_refuses_catalog_with_problems() -> None:
    with pytest.raises(Exception, match=r"scala\.yaml: first\nscala\.yaml: second"):
        CheckedCatalog(
            FakeCatalog([FakeCategory("scala", {})]),
            FakeCheck(["scala.yaml: first", "scala.yaml: second"]),
        ).categories()


def test_gives_categories_of_origin_without_problems() -> None:
    assert_that(
        CheckedCatalog(
            FakeCatalog([FakeCategory("swift", {}), FakeCategory("dart", {})]),
            FakeCheck([]),
        ).categories(),
        has_length(2),
        "a clean catalog must pass its categories through",
    )
