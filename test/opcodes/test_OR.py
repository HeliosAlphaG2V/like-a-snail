import pytest

from likeasnail.enumRegister import R8ID
from likeasnail.opCodesOR import OXB6


@pytest.mark.orCmds
class TestXOR():

    def testOXB6(self, getMemoryController):
        getMemoryController.setR8(R8ID.A, 0xF0)
        getMemoryController.setR8(R8ID.H, 0x3C)
        getMemoryController.setR8(R8ID.L, 0x00)
        getMemoryController.setMemValue(0x3C00, 0x0F)
        OXB6(getMemoryController)
        assert getMemoryController.getR8(R8ID.A) == 0xFF
