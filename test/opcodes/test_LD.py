import pytest

from likeasnail.enumRegister import R8ID
from likeasnail.opcodes import OXE0, OXF0, OX06, OX60, OX7F, OX48, OX40, OX4F, OX0E, OX7E, OX3A, OX52, OX44, OX7C, OX4E, OX4C, OX36, OX08, OX22, OX2A, OX31, OX32, OXF9


@pytest.mark.ldCmds
class TestLD():

    def testOXE0Result(self, getMemoryController):

        getMemoryController.setMemValue(0x0000, 0x60)
        getMemoryController.setR8(R8ID.A, 0xAF)

        OXE0(getMemoryController)

        assert getMemoryController.getMemValue(0xFF00 + 0x60) == 0xAF

    def testOXE0JoyPadDeny(self, getMemoryController):

        getMemoryController.setMemValue(0x0000, 0x00)
        getMemoryController.setR8(R8ID.A, 0xAF)

        OXE0(getMemoryController)

        assert getMemoryController.getMemValue(0xFF00 + 0x00) == 0x00

    # TODO: 0xEF is faked input
    def testOXE0JoyPadAllow(self, getMemoryController):

        getMemoryController.setMemValue(0x0000, 0x00)
        getMemoryController.setR8(R8ID.A, 0x20)

        OXE0(getMemoryController)

        assert getMemoryController.getMemValue(0xFF00 + 0x00) == 0xEF

    def testOXF0Result(self, getMemoryController):

        getMemoryController.setMemValue(0x0000, 0x60)
        getMemoryController.setMemValue(0xFF60, 0xFA)

        OXF0(getMemoryController)

        assert getMemoryController.getR8(R8ID.A) == 0xFA

    def testOX06Result(self, getMemoryController):

        getMemoryController.setMemValue(0x0000, 0x60)
        OX06(getMemoryController)

        assert getMemoryController.getR8(R8ID.B) == 0x60

    def testOX60Result(self, getMemoryController):

        getMemoryController.setR8(R8ID.B, 0xF5)
        OX60(getMemoryController)

        assert getMemoryController.getR8(R8ID.H) == 0xF5

    def testOX7FResult(self, getMemoryController):

        getMemoryController.setR8(R8ID.A, 0xF5)
        OX7F(getMemoryController)

        assert getMemoryController.getR8(R8ID.A) == 0xF5

    def testOX48Result(self, getMemoryController):

        getMemoryController.setR8(R8ID.B, 0xF5)
        OX48(getMemoryController)

        assert getMemoryController.getR8(R8ID.C) == 0xF5

    def testOX40Result(self, getMemoryController):

        getMemoryController.setR8(R8ID.B, 0xF5)
        OX40(getMemoryController)

        assert getMemoryController.getR8(R8ID.B) == 0xF5

    def testOX0EResult(self, getMemoryController):

        getMemoryController.setMemValue(0x0000, 0xF5)
        OX0E(getMemoryController)

        assert getMemoryController.getR8(R8ID.C) == 0xF5

    def testOX4FResult(self, getMemoryController):

        getMemoryController.setR8(R8ID.A, 0xF5)
        OX4F(getMemoryController)

        assert getMemoryController.getR8(R8ID.C) == 0xF5

    def testOX52Result(self, getMemoryController):

        getMemoryController.setR8(R8ID.D, 0xF5)
        OX52(getMemoryController)

        assert getMemoryController.getR8(R8ID.D) == 0xF5

    def testOX44Result(self, getMemoryController):

        getMemoryController.setR8(R8ID.H, 0xF5)
        OX44(getMemoryController)

        assert getMemoryController.getR8(R8ID.B) == 0xF5

    def testOX7CResult(self, getMemoryController):

        getMemoryController.setR8(R8ID.H, 0xF5)
        OX7C(getMemoryController)

        assert getMemoryController.getR8(R8ID.A) == 0xF5

    def testOX4CResult(self, getMemoryController):

        getMemoryController.setR8(R8ID.H, 0xF5)
        OX4C(getMemoryController)

        assert getMemoryController.getR8(R8ID.C) == 0xF5

    def testOX7EResult(self, getMemoryController):

        getMemoryController.setMemValue(0xF050, 0xF5)
        getMemoryController.setR8(R8ID.H, 0xF0)
        getMemoryController.setR8(R8ID.L, 0x50)
        OX7E(getMemoryController)

        assert getMemoryController.getR8(R8ID.A) == 0xF5

    def testOX3AResult(self, getMemoryController):

        getMemoryController.setMemValue(0xF050, 0xF5)
        getMemoryController.setR8(R8ID.H, 0xF0)
        getMemoryController.setR8(R8ID.L, 0x50)
        OX3A(getMemoryController)

        assert getMemoryController.getR8(R8ID.A) == 0xF5

    def testOX3AResultHL(self, getMemoryController):

        getMemoryController.setMemValue(0xF050, 0xF5)
        getMemoryController.setR8(R8ID.H, 0xF0)
        getMemoryController.setR8(R8ID.L, 0x50)
        OX3A(getMemoryController)

        assert getMemoryController.getR8(R8ID.H) == 0xF0
        assert getMemoryController.getR8(R8ID.L) == 0x4F

    def testOX3AResultHLOverflow(self, getMemoryController):

        getMemoryController.setMemValue(0x0000, 0xF5)
        getMemoryController.setR8(R8ID.H, 0x00)
        getMemoryController.setR8(R8ID.L, 0x00)
        OX3A(getMemoryController)

        assert getMemoryController.getR16FromR8(R8ID.H) == 0xFFFF

    def testOX4EResult(self, getMemoryController):

        getMemoryController.setMemValue(0x0000, 0xF5)
        getMemoryController.setR8(R8ID.H, 0x00)
        getMemoryController.setR8(R8ID.L, 0x00)
        OX4E(getMemoryController)

        assert getMemoryController.getR8(R8ID.C) == 0xF5

    def testOX36Result(self, getMemoryController):

        getMemoryController.setMemValue(0x0000, 0xF5)
        getMemoryController.setR8(R8ID.H, 0x50)
        getMemoryController.setR8(R8ID.L, 0x05)
        OX36(getMemoryController)

        assert getMemoryController.getMemValue(0x5005) == 0xF5

    def testOX08Result(self, getMemoryController):

        getMemoryController.setSP(0xFFFE)
        getMemoryController.setMemValue(0x0000, 0x00)
        getMemoryController.setMemValue(0x0001, 0xE5)
        OX08(getMemoryController)

        assert getMemoryController.getMemValue(0xE500) == 0xFE
        assert getMemoryController.getMemValue(0xE501) == 0xFF

    def testOX22Result(self, getMemoryController):

        getMemoryController.setR8(R8ID.A, 0xF5)
        getMemoryController.setR8(R8ID.H, 0x50)
        getMemoryController.setR8(R8ID.L, 0x05)
        OX22(getMemoryController)

        assert getMemoryController.getMemValue(0x5005) == 0xF5

    def testOX22HL(self, getMemoryController):

        getMemoryController.setR8(R8ID.A, 0xF5)
        getMemoryController.setR8(R8ID.H, 0x50)
        getMemoryController.setR8(R8ID.L, 0x05)
        OX22(getMemoryController)

        assert getMemoryController.getR16FromR8(R8ID.H) == 0x5006

    def testOX2AResult(self, getMemoryController):
        getMemoryController.setMemValue(0x5005, 0xF5)
        getMemoryController.setR8(R8ID.H, 0x50)
        getMemoryController.setR8(R8ID.L, 0x05)
        OX2A(getMemoryController)

        assert getMemoryController.getR8(R8ID.A) == 0xF5

    def testOX2AHL(self, getMemoryController):
        getMemoryController.setMemValue(0x5005, 0xF5)
        getMemoryController.setR8(R8ID.H, 0x50)
        getMemoryController.setR8(R8ID.L, 0x05)
        OX2A(getMemoryController)

        assert getMemoryController.getR16FromR8(R8ID.H) == 0x5006

    # def testOXF8(self, getMemoryController):
    #     getMemoryController.setMemValue(0x0000, 0x80)
    #     getMemoryController.setR8(R8ID.H, 0x50)
    #     getMemoryController.setR8(R8ID.L, 0x05)
    #     OXF8(getMemoryController)
    #
    #     assert getMemoryController.getR16FromR8(R8ID.H) == 0x4F85

    def testOX31(self, getMemoryController):
        getMemoryController.setMemValue(0x0000, 0x50)
        getMemoryController.setMemValue(0x0001, 0x05)
        OX31(getMemoryController)

        assert getMemoryController.getSP() == 0x0550

    def testOX32Result(self, getMemoryController):
        getMemoryController.setR8(R8ID.A, 0xF5)
        getMemoryController.setR8(R8ID.H, 0x50)
        getMemoryController.setR8(R8ID.L, 0x05)
        OX32(getMemoryController)

        assert getMemoryController.getMemValue(0x5005) == 0xF5

    def testOX32HL(self, getMemoryController):
        getMemoryController.setR8(R8ID.A, 0xF5)
        getMemoryController.setR8(R8ID.H, 0x50)
        getMemoryController.setR8(R8ID.L, 0x05)
        OX32(getMemoryController)

        assert getMemoryController.getR16FromR8(R8ID.H) == 0x5004

    def testOXF9(self, getMemoryController):
        getMemoryController.setR8(R8ID.H, 0x0)
        getMemoryController.setR8(R8ID.L, 0x0)
        OXF9(getMemoryController)

        assert getMemoryController.getSP() == 0x0

    def testOXF91(self, getMemoryController):
        getMemoryController.setR8(R8ID.H, 0xFF)
        getMemoryController.setR8(R8ID.L, 0xFF)
        OXF9(getMemoryController)

        assert getMemoryController.getSP() == 0xFFFF
