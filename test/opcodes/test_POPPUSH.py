import pytest

from likeasnail.enumRegister import R8ID
from likeasnail.opCodesPushPop import OXC5, OXC1


@pytest.mark.pushPopCmds
class TestPushPop():

    def test0XC5(self, getMemoryController):
        getMemoryController.setR8(R8ID.B, 0x95)
        getMemoryController.setR8(R8ID.C, 0x12)
        getMemoryController.setSP(0xFFFE)
        OXC5(getMemoryController)
        assert getMemoryController.getAsR16(getMemoryController.pop(),
                                            getMemoryController.pop()) == 0x9512

    def test0XC1(self, getMemoryController):
        getMemoryController.setSP(0xFFFE)
        getMemoryController.push(0x12)
        getMemoryController.push(0x95)
        OXC1(getMemoryController)
        assert getMemoryController.getAsR16(getMemoryController.getR8(R8ID.B),
                                            getMemoryController.getR8(R8ID.C)) == 0x9512
