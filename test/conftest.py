import pytest

from likeasnail.memoryController import MemCntr


@pytest.fixture(scope="class")
def obj():
    return MemCntr(rom='', boot='', skip=True)
