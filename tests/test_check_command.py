import pytest

from catalog.check_command import CheckCommand
from catalog.checked_catalog import CheckedCatalog
from tests.fakes import FakeCatalog, FakeCheck


def test_refuses_catalog_with_problems() -> None:
    with pytest.raises(Exception, match=r"c\.yaml: pointers"):
        CheckCommand(
            CheckedCatalog(FakeCatalog([]), FakeCheck(["c.yaml: pointers"]))
        ).run()
