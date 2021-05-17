import pytest

from likeasnail.enumRegister import R8ID
from likeasnail.opcodes import OX3E


@pytest.mark.ldCmds
class TestLDAX():

    def testOX3EResult(self, getMemoryController):

        getMemoryController.setMemValue(0x0000, 0x60)

        OX3E(getMemoryController)

        assert getMemoryController.getR8(R8ID.A) == 0x60
