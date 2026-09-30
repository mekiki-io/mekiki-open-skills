import pytest
from hamcrest import assert_that, contains_exactly, empty, has_length

from catalog.schema_check import SchemaCheck
from tests.fakes import FakeCatalog, FakeCategory


def test_accepts_complete_category() -> None:
    assert_that(
        SchemaCheck(
            FakeCatalog(
                [
                    FakeCategory(
                        "python",
                        {
                            "name": "Python",
                            "description": "Core language, runtime and ecosystem.",
                            "skills": {
                                "gil": {
                                    "name": "GIL",
                                    "level": "senior",
                                    "aliases": ["Global Interpreter Lock"],
                                    "prerequisites": ["threads"],
                                    "related": ["asyncio"],
                                }
                            },
                        },
                    )
                ]
            )
        ).problems(),
        empty(),
        "a category with every field filled must pass",
    )


def test_refuses_unknown_level() -> None:
    assert_that(
        SchemaCheck(
            FakeCatalog(
                [
                    FakeCategory(
                        "java",
                        {
                            "name": "Java",
                            "description": "JVM.",
                            "skills": {"jit": {"name": "JIT", "level": "Senior"}},
                        },
                    )
                ]
            )
        ).problems(),
        contains_exactly(
            "java.yaml: skills/jit/level: "
            "'Senior' is not one of ['junior', 'middle', 'senior']"
        ),
        "levels are case sensitive and limited to three values",
    )


def test_refuses_skill_without_name() -> None:
    assert_that(
        SchemaCheck(
            FakeCatalog(
                [
                    FakeCategory(
                        "php",
                        {
                            "name": "PHP",
                            "description": "Web.",
                            "skills": {"fpm": {"level": "middle"}},
                        },
                    )
                ]
            )
        ).problems(),
        contains_exactly("php.yaml: skills/fpm: 'name' is a required property"),
        "every skill needs a name",
    )


def test_refuses_misspelled_field() -> None:
    assert_that(
        SchemaCheck(
            FakeCatalog(
                [
                    FakeCategory(
                        "lua",
                        {
                            "name": "Lua",
                            "description": "Embedded.",
                            "skills": {
                                "tables": {
                                    "name": "Tables",
                                    "level": "junior",
                                    "alias": ["t"],
                                }
                            },
                        },
                    )
                ]
            )
        ).problems(),
        has_length(1),
        "unknown fields are typos and must be refused",
    )


@pytest.mark.parametrize(
    "key", ["Async_IO", "-lead", "trail-", "a--b", "ünïcode", "", "a b"]
)
def test_refuses_skill_key_that_is_not_slug(key: str) -> None:
    assert_that(
        SchemaCheck(
            FakeCatalog(
                [
                    FakeCategory(
                        "perl",
                        {
                            "name": "Perl",
                            "description": "Text.",
                            "skills": {key: {"name": "X", "level": "junior"}},
                        },
                    )
                ]
            )
        ).problems(),
        has_length(1),
        f"key {key!r} must be lowercase words joined by single '-'",
    )


def test_refuses_repeated_alias() -> None:
    assert_that(
        SchemaCheck(
            FakeCatalog(
                [
                    FakeCategory(
                        "erlang",
                        {
                            "name": "Erlang",
                            "description": "BEAM.",
                            "skills": {
                                "otp": {
                                    "name": "OTP",
                                    "level": "senior",
                                    "aliases": ["otp", "otp"],
                                }
                            },
                        },
                    )
                ]
            )
        ).problems(),
        has_length(1),
        "aliases must be unique",
    )


def test_refuses_category_without_skills() -> None:
    assert_that(
        SchemaCheck(
            FakeCatalog(
                [
                    FakeCategory(
                        "cobol", {"name": "COBOL", "description": "Old.", "skills": {}}
                    )
                ]
            )
        ).problems(),
        has_length(1),
        "a category must have at least one skill",
    )


def test_refuses_empty_file() -> None:
    assert_that(
        SchemaCheck(FakeCatalog([FakeCategory("fortran", None)])).problems(),
        contains_exactly("fortran.yaml: root: None is not of type 'object'"),
        "an empty file is not a category",
    )


def test_refuses_file_name_that_is_not_slug() -> None:
    assert_that(
        SchemaCheck(
            FakeCatalog(
                [
                    FakeCategory(
                        "Soft_Skills",
                        {
                            "name": "Soft",
                            "description": "S.",
                            "skills": {"talk": {"name": "Talk", "level": "junior"}},
                        },
                    )
                ]
            )
        ).problems(),
        contains_exactly(
            "Soft_Skills.yaml: file name must be lowercase words joined by '-'"
        ),
        "file name is the category id and must be a slug",
    )
