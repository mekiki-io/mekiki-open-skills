from hamcrest import assert_that, contains_exactly, empty

from catalog.staged_checks import StagedChecks
from tests.fakes import FakeCheck


def test_stops_at_first_stage_with_problems() -> None:
    assert_that(
        StagedChecks(
            [FakeCheck(["schema broke"]), FakeCheck(["never reached"])]
        ).problems(),
        contains_exactly("schema broke"),
        "later stages rely on earlier ones and must not run after a failure",
    )


def test_runs_later_stage_after_clean_one() -> None:
    assert_that(
        StagedChecks([FakeCheck([]), FakeCheck(["late ⚠"])]).problems(),
        contains_exactly("late ⚠"),
        "a clean stage must pass control to the next one",
    )


def test_has_no_problems_without_stages() -> None:
    assert_that(
        StagedChecks([]).problems(),
        empty(),
        "no stages means nothing to complain about",
    )
