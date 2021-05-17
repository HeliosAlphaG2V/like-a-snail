import pytest

from likeasnail.enumRegister import R8ID
from likeasnail.opCodesDEC import decX, OX05, OX3B


@pytest.mark.decCmds
class TestDEC():

    def testDecXZero(self, getMemoryController):
        assert getMemoryController.getZero() == 0
        assert getMemoryController.getSubstract() == 0
        assert getMemoryController.getHalfCarry() == 0
        assert getMemoryController.getCarry() == 0

        result = decX(getMemoryController, 1)

        assert result == 0
        assert getMemoryController.getZero() == 1
        assert getMemoryController.getSubstract() == 1
        assert getMemoryController.getHalfCarry() == 0
        assert getMemoryController.getCarry() == 0

    def testDecX(self, getMemoryController):
        assert getMemoryController.getZero() == 0
        assert getMemoryController.getSubstract() == 0
        assert getMemoryController.getHalfCarry() == 0
        assert getMemoryController.getCarry() == 0

        result = decX(getMemoryController, 20)

        assert result == 19
        assert getMemoryController.getZero() == 0
        assert getMemoryController.getSubstract() == 1
        assert getMemoryController.getHalfCarry() == 0
        assert getMemoryController.getCarry() == 0

    def testDecXHalfCarry(self, getMemoryController):
        assert getMemoryController.getZero() == 0
        assert getMemoryController.getSubstract() == 0
        assert getMemoryController.getHalfCarry() == 0
        assert getMemoryController.getCarry() == 0

        result = decX(getMemoryController, 96)

        assert result == 95
        assert getMemoryController.getZero() == 0
        assert getMemoryController.getSubstract() == 1
        assert getMemoryController.getHalfCarry() == 1
        assert getMemoryController.getCarry() == 0

    def testDecXUnderflow(self, getMemoryController):
        assert getMemoryController.getZero() == 0
        assert getMemoryController.getSubstract() == 0
        assert getMemoryController.getHalfCarry() == 0
        assert getMemoryController.getCarry() == 0

        result = decX(getMemoryController, 0)

        assert result == 0xFF
        assert getMemoryController.getZero() == 0
        assert getMemoryController.getSubstract() == 1
        assert getMemoryController.getHalfCarry() == 0
        assert getMemoryController.getCarry() == 0

    def testOX05Result(self, getMemoryController):

        getMemoryController.setR8(R8ID.B, 0xFF)

        OX05(getMemoryController)

        assert getMemoryController.getR8(R8ID.B) == 0xFE

    def testOX3BSPMax(self, getMemoryController):
        getMemoryController.setSP(0x0000)
        OX3B(getMemoryController)
        assert getMemoryController.getSP() == 0xFFFF
