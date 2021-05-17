import pytest

from likeasnail.enumRegister import R8ID
from likeasnail.opCodesADD import addX, addXR16, OX80, OXE8, OXF8


@pytest.mark.addCmds
class TestADD():

    def testADDX(self, getMemoryController):
        assert getMemoryController.getZero() == 0
        assert getMemoryController.getSubstract() == 0
        assert getMemoryController.getHalfCarry() == 0
        assert getMemoryController.getCarry() == 0

        addX(getMemoryController, 1)

        assert getMemoryController.getR8(R8ID.A) == 1
        assert getMemoryController.getZero() == 0
        assert getMemoryController.getSubstract() == 0
        assert getMemoryController.getHalfCarry() == 0
        assert getMemoryController.getCarry() == 0

    def testADDXOverflow(self, getMemoryController):
        assert getMemoryController.getZero() == 0
        assert getMemoryController.getSubstract() == 0
        assert getMemoryController.getHalfCarry() == 0
        assert getMemoryController.getCarry() == 0

        getMemoryController.setR8(R8ID.A, 255)
        addX(getMemoryController, 1)

        assert getMemoryController.getR8(R8ID.A) == 0
        assert getMemoryController.getZero() == 1
        assert getMemoryController.getSubstract() == 0
        assert getMemoryController.getHalfCarry() == 1
        assert getMemoryController.getCarry() == 1

    def testADDXHalfCarry(self, getMemoryController):
        assert getMemoryController.getZero() == 0
        assert getMemoryController.getSubstract() == 0
        assert getMemoryController.getHalfCarry() == 0
        assert getMemoryController.getCarry() == 0

        getMemoryController.setR8(R8ID.A, 0xFF)
        addX(getMemoryController, 0xFF)

        assert getMemoryController.getR8(R8ID.A) == 0xFE
        assert getMemoryController.getZero() == 0
        assert getMemoryController.getSubstract() == 0
        assert getMemoryController.getHalfCarry() == 1
        assert getMemoryController.getCarry() == 1

    def testOX80Result(self, getMemoryController):

        getMemoryController.setR8(R8ID.A, 0x0F)
        getMemoryController.setR8(R8ID.B, 0x0F)
        OX80(getMemoryController)

        assert getMemoryController.getR8(R8ID.A) == 0x1E

    def testADDX16Result(self, getMemoryController):
        addXR16(getMemoryController, 0xFFFF, 0xFFFF, R8ID.B)
        assert getMemoryController.getR16FromR8(R8ID.B) == 0xFFFE

    def testADDXR16Carry(self, getMemoryController):
        addXR16(getMemoryController, 0xFFFF, 0xFFFF, R8ID.B)
        assert getMemoryController.getCarry() == 1

    def testADDXR16HalfCarry(self, getMemoryController):
        addXR16(getMemoryController, 0xFFFF, 0xFFFF, R8ID.B)
        assert getMemoryController.getHalfCarry() == 1

    def testADDXR16Substract(self, getMemoryController):
        addXR16(getMemoryController, 0xFFFF, 0xFFFF, R8ID.B)
        assert getMemoryController.getSubstract() == 0

    def testOXE8(self, getMemoryController):
        getMemoryController.setMemValue(0x0, 0x90)
        OXE8(getMemoryController)
        assert getMemoryController.getSP() == 0xFF8E

    def testOXE8Reset(self, getMemoryController):
        getMemoryController.setSP(0x0)
        getMemoryController.setMemValue(0x0, 0x90)
        OXE8(getMemoryController)
        assert getMemoryController.getSP() == 0xFF8F

    def testOXF8(self, getMemoryController):
        getMemoryController.setMemValue(0x0, 0x90)
        OXF8(getMemoryController)
        assert getMemoryController.getR16FromR8(R8ID.H) == 0xFF8E
