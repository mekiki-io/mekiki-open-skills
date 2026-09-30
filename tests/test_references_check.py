from hamcrest import assert_that, contains_exactly, empty

from catalog.references_check import ReferencesCheck
from tests.fakes import FakeCatalog, FakeCategory


def test_accepts_references_to_skills_of_same_file() -> None:
    assert_that(
        ReferencesCheck(
            FakeCatalog(
                [
                    FakeCategory(
                        "devops",
                        {
                            "skills": {
                                "docker": {"related": ["helm"]},
                                "helm": {
                                    "prerequisites": ["docker"],
                                    "related": ["docker"],
                                },
                            }
                        },
                    )
                ]
            )
        ).problems(),
        empty(),
        "references between skills of one file must pass",
    )


def test_refuses_unknown_prerequisite() -> None:
    assert_that(
        ReferencesCheck(
            FakeCatalog(
                [
                    FakeCategory(
                        "ruby", {"skills": {"rack": {"prerequisites": ["http-2"]}}}
                    )
                ]
            )
        ).problems(),
        contains_exactly(
            "ruby.yaml: rack: prerequisites item 'http-2' is not a skill in this file"
        ),
        "prerequisites must point to existing skills",
    )


def test_refuses_reference_to_skill_of_other_file() -> None:
    assert_that(
        ReferencesCheck(
            FakeCatalog(
                [
                    FakeCategory("sql", {"skills": {"joins": {}}}),
                    FakeCategory(
                        "orm", {"skills": {"n-plus-1": {"related": ["joins"]}}}
                    ),
                ]
            )
        ).problems(),
        contains_exactly(
            "orm.yaml: n-plus-1: related item 'joins' is not a skill in this file"
        ),
        "references across files are not supported",
    )


def test_refuses_reference_to_itself() -> None:
    assert_that(
        ReferencesCheck(
            FakeCatalog(
                [
                    FakeCategory(
                        "leadership", {"skills": {"1-on-1": {"related": ["1-on-1"]}}}
                    )
                ]
            )
        ).problems(),
        contains_exactly(
            "leadership.yaml: 1-on-1: related item '1-on-1' is the skill itself"
        ),
        "a skill can not be related to itself",
    )
