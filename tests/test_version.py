import pytest
from hamcrest import assert_that, equal_to
from hypothesis import given
from hypothesis import strategies as st

from catalog.version import Version


def test_drops_leading_v() -> None:
    assert_that(
        str(Version("v10.0.7")), equal_to("10.0.7"), "tags like v1.2.3 are common"
    )


@given(st.integers(min_value=0), st.integers(min_value=0), st.integers(min_value=0))
def test_keeps_any_semantic_version(major: int, minor: int, patch: int) -> None:
    assert_that(
        str(Version(f"{major}.{minor}.{patch}")),
        equal_to(f"{major}.{minor}.{patch}"),
        "every semantic version must be accepted as is",
    )


@pytest.mark.parametrize(
    "tag",
    [
        "1.4",
        "latest",
        "1.4.0-rc1",
        "",
        "vv1.0.0",
        "01.2.3",
        "\u0661.\u0662.\u0663",
        "1.2.3\n",
        " 1.2.3",
    ],
)
def test_refuses_tag_that_is_not_semantic_version(tag: str) -> None:
    with pytest.raises(Exception, match="is not a version"):
        str(Version(tag))
