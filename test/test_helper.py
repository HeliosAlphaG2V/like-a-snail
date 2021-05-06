import pytest


@pytest.mark.helper
class TestHelper():

    def testAllOtherRegisterZero(self, getMemoryController):
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, 99, 99) == True

        assert pytest.helpers.allOtherRegisterZero(getMemoryController, 0, 0) == True
