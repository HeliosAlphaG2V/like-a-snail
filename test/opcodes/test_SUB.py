import pytest

from likeasnail.enumRegister import R8ID
from likeasnail.opCodesSUB import OXD6


@pytest.mark.subCmds
class TestLD():

    def testOXD6Result(self, getMemoryController):

        getMemoryController.setMemValue(0x0000, 0x88)
        getMemoryController.setR8(R8ID.A, 0x00)

        OXD6(getMemoryController)

        assert getMemoryController.getR8(R8ID.A) == 0x78

    def testOXD6Carry(self, getMemoryController):

        getMemoryController.setMemValue(0x0000, 0x88)
        getMemoryController.setR8(R8ID.A, 0x00)

        OXD6(getMemoryController)

        assert getMemoryController.getCarry() == 1

    def testOXD6HalfCarry(self, getMemoryController):

        getMemoryController.setMemValue(0x0000, 0x88)
        getMemoryController.setR8(R8ID.A, 0x00)

        OXD6(getMemoryController)

        assert getMemoryController.getHalfCarry() == 1

    def testOXD6Zero(self, getMemoryController):

        getMemoryController.setMemValue(0x0000, 0x88)
        getMemoryController.setR8(R8ID.A, 0x00)

        OXD6(getMemoryController)

        assert getMemoryController.getZero() == 0

    def testOXD6Substract(self, getMemoryController):

        getMemoryController.setMemValue(0x0000, 0x88)
        getMemoryController.setR8(R8ID.A, 0x00)

        OXD6(getMemoryController)

        assert getMemoryController.getSubstract() == 1
