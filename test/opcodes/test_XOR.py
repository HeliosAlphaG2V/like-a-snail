import pytest

from likeasnail.enumRegister import R8ID
from likeasnail.opCodesXOR import xorX, OXAE


@pytest.mark.xorCmds
class TestXOR():

    def testXORX(self, getMemoryController):

        getMemoryController.setR8(R8ID.A, 0x3C)
        xorX(getMemoryController, 0xC3)

        assert getMemoryController.getR8(R8ID.A) == 0xFF

    def testXORXZero(self, getMemoryController):

        getMemoryController.setR8(R8ID.A, 0x3C)
        xorX(getMemoryController, 0x3C)

        assert getMemoryController.getZero() == 1

    def testOXAE(self, getMemoryController):

        getMemoryController.setR8(R8ID.A, 0xFF)
        getMemoryController.setR8(R8ID.H, 0xD9)
        getMemoryController.setR8(R8ID.L, 0x43)
        getMemoryController.setMemValue(0xD943, 0x2A)
        OXAE(getMemoryController)

        assert getMemoryController.getR8(R8ID.A) == 0xD5
