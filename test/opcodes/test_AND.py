import pytest

from likeasnail.enumRegister import R8ID
from likeasnail.opCodesAND import andX, OXA6, OXA2, OXA7, OXA1, OXE6


@pytest.mark.andCmds
class TestADD():

    def testandX(self, getMemoryController):
        getMemoryController.setR8(R8ID.A, 0xF0)
        andX(getMemoryController, 0xFF)

        assert getMemoryController.getR8(R8ID.A) == 0xF0
        assert getMemoryController.getZero() == 0
        assert getMemoryController.getSubstract() == 0
        assert getMemoryController.getHalfCarry() == 1
        assert getMemoryController.getCarry() == 0

    def testandXZero(self, getMemoryController):
        getMemoryController.setR8(R8ID.A, 0x00)
        andX(getMemoryController, 0x00)

        assert getMemoryController.getZero() == 1

    def testOXA6(self, getMemoryController):
        getMemoryController.setMemValue(0x8585, 0x01)
        getMemoryController.setR8(R8ID.H, 0x85)
        getMemoryController.setR8(R8ID.L, 0x85)
        getMemoryController.setR8(R8ID.A, 0x01)
        OXA6(getMemoryController)

        assert getMemoryController.getR8(R8ID.A) == 0x01
        assert getMemoryController.getZero() == 0
        assert getMemoryController.getSubstract() == 0
        assert getMemoryController.getHalfCarry() == 1
        assert getMemoryController.getCarry() == 0

    def testOXA2Zero(self, getMemoryController):

        getMemoryController.setR8(R8ID.A, 0x00)
        getMemoryController.setR8(R8ID.D, 0x00)
        OXA2(getMemoryController)

        assert getMemoryController.getZero() == 1

    def testOXA7Zero(self, getMemoryController):

        getMemoryController.setR8(R8ID.A, 0x00)
        OXA7(getMemoryController)

        assert getMemoryController.getZero() == 1

    def testOXA1Zero(self, getMemoryController):

        getMemoryController.setR8(R8ID.C, 0x00)
        OXA1(getMemoryController)

        assert getMemoryController.getZero() == 1

    def testOXA1Result(self, getMemoryController):

        getMemoryController.setR8(R8ID.C, 0xF0)
        getMemoryController.setR8(R8ID.A, 0x0F)
        OXA1(getMemoryController)

        assert getMemoryController.getR8(R8ID.A) == 0x00

    def testOXE6Result(self, getMemoryController):

        getMemoryController.setMemValue(0x0000, 0xF0)
        getMemoryController.setR8(R8ID.A, 0x0F)
        OXE6(getMemoryController)

        assert getMemoryController.getR8(R8ID.A) == 0x00
