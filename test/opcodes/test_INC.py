import pytest

from likeasnail.enumRegister import R8ID
from likeasnail.opCodesINC import OX2C, OX3C, OX03, OX04, OX34, OX0C, OX33


@pytest.mark.incCmds
class TestINC():

    def testOX03(self, getMemoryController):
        getMemoryController.setR8(R8ID.B, 0xFF)
        getMemoryController.setR8(R8ID.C, 0xFF)
        OX03(getMemoryController)

        assert getMemoryController.getR16FromR8(R8ID.B) == 0x00

    def testOX2CResult(self, getMemoryController):

        getMemoryController.setR8(R8ID.L, 0xFF)

        OX2C(getMemoryController)

        assert getMemoryController.getR8(R8ID.L) == 0x00

    def testOX2CCarry(self, getMemoryController):

        getMemoryController.setR8(R8ID.L, 0xFF)

        OX2C(getMemoryController)

        assert getMemoryController.getCarry() == 0

    def testOX2CNoHalfCarry(self, getMemoryController):

        getMemoryController.setR8(R8ID.L, 0x01)

        OX2C(getMemoryController)

        assert getMemoryController.getHalfCarry() == 0

    def testOX2CHalfCarry(self, getMemoryController):

        getMemoryController.setR8(R8ID.L, 0x0F)

        OX2C(getMemoryController)

        assert getMemoryController.getHalfCarry() == 1

    def testOX2CSubstract(self, getMemoryController):

        getMemoryController.setR8(R8ID.L, 0x0F)

        OX2C(getMemoryController)

        assert getMemoryController.getSubstract() == 0

    def testOX2CSubstract(self, getMemoryController):

        getMemoryController.setR8(R8ID.L, 0xFF)

        OX2C(getMemoryController)

        assert getMemoryController.getZero() == 1

    def testOX3CResult(self, getMemoryController):

        getMemoryController.setR8(R8ID.A, 0xFF)

        OX3C(getMemoryController)

        assert getMemoryController.getR8(R8ID.A) == 0x00

    def testOX04Result(self, getMemoryController):

        getMemoryController.setR8(R8ID.B, 0xFF)

        OX04(getMemoryController)

        assert getMemoryController.getR8(R8ID.B) == 0x00

    def testOX0CResult(self, getMemoryController):

        getMemoryController.setR8(R8ID.C, 0xFF)

        OX0C(getMemoryController)

        assert getMemoryController.getR8(R8ID.C) == 0x00

    def testOX34Result(self, getMemoryController):

        getMemoryController.setMemValue(0x0000, 0xFF)

        OX34(getMemoryController)

        assert getMemoryController.getMemValue(0x0000) == 0x00

    def testOX33SPMin(self, getMemoryController):
        getMemoryController.setSP(0xFFFF)
        OX33(getMemoryController)
        assert getMemoryController.getSP() == 0x0000
