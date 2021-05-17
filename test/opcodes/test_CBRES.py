import pytest

from likeasnail.enumRegister import R8ID
from likeasnail.opcodes import cbOXBE


@pytest.mark.cbRESCmds
class TestADD():

    def testCBOXBE(self, getMemoryController):
        getMemoryController.setR8(R8ID.H, 0x84)
        getMemoryController.setR8(R8ID.L, 0x84)
        getMemoryController.setMemValue(0x8484, 255)

        cbOXBE(getMemoryController)

        assert getMemoryController.getMemValue(0x8484) == 127
        assert getMemoryController.getR8(R8ID.H) == 0x84
        assert getMemoryController.getR8(R8ID.L) == 0x84

        getMemoryController.setMemValue(0x8484, 127)

        cbOXBE(getMemoryController)

        assert getMemoryController.getMemValue(0x8484) == 127
        assert getMemoryController.getR8(R8ID.H) == 0x84
        assert getMemoryController.getR8(R8ID.L) == 0x84
