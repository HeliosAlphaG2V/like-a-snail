import pytest

from likeasnail.enumRegister import R8ID
from likeasnail.opCodesXOR import xorX


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
