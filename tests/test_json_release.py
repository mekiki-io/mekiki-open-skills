import json

from hamcrest import assert_that, equal_to
from hypothesis import given
from hypothesis import strategies as st

from catalog.json_release import JsonRelease
from catalog.version import Version
from tests.fakes import FakeCatalog, FakeCategory


def test_builds_catalog_document() -> None:
    assert_that(
        json.loads(
            JsonRelease(
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
                                        "related": ["multiprocessing"],
                                    },
                                    "multiprocessing": {
                                        "name": "Multiprocessing",
                                        "level": "senior",
                                    },
                                },
                            },
                        )
                    ]
                ),
                Version("1.4.0"),
            ).text()
        ),
        equal_to(
            {
                "version": "1.4.0",
                "categories": [
                    {
                        "id": "python",
                        "name": "Python",
                        "description": "Core language, runtime and ecosystem.",
                        "skills": [
                            {
                                "id": "gil",
                                "name": "GIL",
                                "level": "senior",
                                "aliases": ["Global Interpreter Lock"],
                                "prerequisites": [],
                                "related": ["multiprocessing"],
                            },
                            {
                                "id": "multiprocessing",
                                "name": "Multiprocessing",
                                "level": "senior",
                                "aliases": [],
                                "prerequisites": [],
                                "related": [],
                            },
                        ],
                    }
                ],
            }
        ),
        "release must follow the skills.json format with every list present",
    )


def test_writes_unicode_without_escaping() -> None:
    assert_that(
        JsonRelease(
            FakeCatalog(
                [
                    FakeCategory(
                        "ux",
                        {
                            "name": "Дизайн",
                            "description": "日本語",
                            "skills": {"a": {"name": "✓", "level": "junior"}},
                        },
                    )
                ]
            ),
            Version("0.0.1"),
        ).text(),
        equal_to(
            '{\n  "version": "0.0.1",\n  "categories": [\n    {\n      "id": "ux",\n'
            '      "name": "Дизайн",\n      "description": "日本語",\n'
            '      "skills": [\n'
            '        {\n          "id": "a",\n          "name": "✓",\n'
            '          "level": "junior",\n          "aliases": [],\n'
            '          "prerequisites": [],\n          "related": []\n        }\n'
            "      ]\n    }\n  ]\n}\n"
        ),
        "release must be readable UTF-8 with a trailing newline",
    )


@given(st.text(min_size=1))
def test_keeps_any_category_name(name: str) -> None:
    assert_that(
        json.loads(
            JsonRelease(
                FakeCatalog(
                    [
                        FakeCategory(
                            "any",
                            {
                                "name": name,
                                "description": "D",
                                "skills": {"k": {"name": "K", "level": "middle"}},
                            },
                        )
                    ]
                ),
                Version("3.2.1"),
            ).text()
        )["categories"][0]["name"],
        equal_to(name),
        "any text must survive the JSON round trip",
    )
