import pytest

from likeasnail.enumRegister import R8ID
from likeasnail.opcodes import OXFE


@pytest.mark.cpCmds
class TestCPX():

    def testOXFEZero(self, getMemoryController):

        getMemoryController.setMemValue(0x0000, 0x60)
        getMemoryController.setR8(R8ID.A, 0x60)

        OXFE(getMemoryController)

        assert getMemoryController.getZero() == 1

    def testOXFESubstract(self, getMemoryController):

        getMemoryController.setMemValue(0x0000, 0x60)
        getMemoryController.setR8(R8ID.A, 0x60)

        OXFE(getMemoryController)

        assert getMemoryController.getSubstract() == 1

    def testOXFECarry(self, getMemoryController):

        getMemoryController.setMemValue(0x0000, 0xFF)
        getMemoryController.setR8(R8ID.A, 0x60)

        OXFE(getMemoryController)

        assert getMemoryController.getCarry() == 1
