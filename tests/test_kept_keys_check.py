from hamcrest import assert_that, contains_exactly, empty

from catalog.kept_keys_check import KeptKeysCheck
from tests.fakes import FakeCatalog, FakeCategory


def test_accepts_added_skills() -> None:
    assert_that(
        KeptKeysCheck(
            FakeCatalog(
                [FakeCategory("go", {"skills": {"channels": {}, "generics": {}}})]
            ),
            FakeCatalog([FakeCategory("go", {"skills": {"channels": {}}})]),
        ).problems(),
        empty(),
        "adding skills must pass",
    )


def test_accepts_first_release() -> None:
    assert_that(
        KeptKeysCheck(
            FakeCatalog([FakeCategory("css", {"skills": {"flexbox": {}}})]),
            FakeCatalog([]),
        ).problems(),
        empty(),
        "nothing can be removed when there was no release",
    )


def test_refuses_renamed_skill() -> None:
    assert_that(
        KeptKeysCheck(
            FakeCatalog([FakeCategory("python", {"skills": {"global-lock": {}}})]),
            FakeCatalog([FakeCategory("python", {"skills": {"gil": {}}})]),
        ).problems(),
        contains_exactly(
            "python.gil: skill was removed or renamed, keys must never change"
        ),
        "user templates reference skills by key, so keys must live forever",
    )


def test_refuses_removed_category() -> None:
    assert_that(
        KeptKeysCheck(
            FakeCatalog([FakeCategory("html", {"skills": {"forms": {}}})]),
            FakeCatalog(
                [
                    FakeCategory("html", {"skills": {"forms": {}}}),
                    FakeCategory("xml", {"skills": {"xslt": {}, "dtd": {}}}),
                ]
            ),
        ).problems(),
        contains_exactly(
            "xml.dtd: skill was removed or renamed, keys must never change",
            "xml.xslt: skill was removed or renamed, keys must never change",
        ),
        "removing a file removes all its skills",
    )
