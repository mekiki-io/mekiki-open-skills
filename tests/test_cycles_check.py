from hamcrest import assert_that, contains_exactly, empty

from catalog.cycles_check import CyclesCheck
from tests.fakes import FakeCatalog, FakeCategory


def test_refuses_two_skills_needing_each_other() -> None:
    assert_that(
        CyclesCheck(
            FakeCatalog(
                [
                    FakeCategory(
                        "python",
                        {
                            "skills": {
                                "a": {"prerequisites": ["b"]},
                                "b": {"prerequisites": ["a"]},
                            }
                        },
                    )
                ]
            )
        ).problems(),
        contains_exactly("python.yaml: a: prerequisites form a cycle (a -> b -> a)"),
        "a prerequisites loop has no valid order and must be refused",
    )


def test_refuses_loop_reached_through_chain() -> None:
    assert_that(
        CyclesCheck(
            FakeCatalog(
                [
                    FakeCategory(
                        "k8s",
                        {
                            "skills": {
                                "pod-🚀": {"prerequisites": ["svc"]},
                                "svc": {"prerequisites": ["ingress"]},
                                "ingress": {"prerequisites": ["hpa"]},
                                "hpa": {"prerequisites": ["svc"]},
                            }
                        },
                    )
                ]
            )
        ).problems(),
        contains_exactly(
            "k8s.yaml: svc: prerequisites form a cycle (svc -> ingress -> hpa -> svc)"
        ),
        "the cycle must be reported without the chain that leads to it",
    )


def test_accepts_diamond_of_prerequisites() -> None:
    assert_that(
        CyclesCheck(
            FakeCatalog(
                [
                    FakeCategory(
                        "sql",
                        {
                            "skills": {
                                "window-functions": {
                                    "prerequisites": ["group-by", "order-by"]
                                },
                                "group-by": {"prerequisites": ["select"]},
                                "order-by": {"prerequisites": ["select"]},
                                "select": {},
                            }
                        },
                    )
                ]
            )
        ).problems(),
        empty(),
        "two paths to one skill are not a cycle",
    )


def test_accepts_loop_of_related_skills() -> None:
    assert_that(
        CyclesCheck(
            FakeCatalog(
                [
                    FakeCategory(
                        "git",
                        {
                            "skills": {
                                "rebase": {"related": ["merge"]},
                                "merge": {"related": ["rebase"]},
                            }
                        },
                    )
                ]
            )
        ).problems(),
        empty(),
        "related is symmetric and may loop",
    )


def test_refuses_cycles_of_every_file() -> None:
    assert_that(
        CyclesCheck(
            FakeCatalog(
                [
                    FakeCategory(
                        "x",
                        {
                            "skills": {
                                "y1": {"prerequisites": ["y2"]},
                                "y2": {"prerequisites": ["y1"]},
                            }
                        },
                    ),
                    FakeCategory(
                        "z",
                        {
                            "skills": {
                                "q": {"prerequisites": ["w"]},
                                "w": {"prerequisites": ["q"]},
                            }
                        },
                    ),
                ]
            )
        ).problems(),
        contains_exactly(
            "x.yaml: y1: prerequisites form a cycle (y1 -> y2 -> y1)",
            "z.yaml: q: prerequisites form a cycle (q -> w -> q)",
        ),
        "each file must be checked for cycles",
    )
