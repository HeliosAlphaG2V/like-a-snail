import pytest

from likeasnail.enumRegister import R8ID
from likeasnail.opcodes import cbOX37


@pytest.mark.swapCmds
class TestXOR():

    def testCBOX37(self, getMemoryController):

        getMemoryController.setR8(R8ID.A, 0x3C)
        cbOX37(getMemoryController)

        assert getMemoryController.getR8(R8ID.A) == 0xC3
