import pytest

from likeasnail.enumRegister import R8ID
from likeasnail.opCodesJUMP import OXFF, OXCD, OXC9, OX20, OX18, OXC3, OXE9, OXC4


@pytest.mark.jmpCmds
class TestJUMP():

    def testOXFFResult(self, getMemoryController):

        OXFF(getMemoryController)
        assert getMemoryController.getPC() == 0x0038

    def testOXFFStackLower(self, getMemoryController):

        getMemoryController.setPC(0xAFBE)
        OXFF(getMemoryController)
        assert getMemoryController.getMemValue(getMemoryController.getSP() + 1) == 0xBE

    def testOXFFStackUpper(self, getMemoryController):

        getMemoryController.setPC(0xAFBE)
        OXFF(getMemoryController)
        assert getMemoryController.getMemValue(getMemoryController.getSP()) == 0xAF

    def testOXFFStackPointer(self, getMemoryController):

        OXFF(getMemoryController)
        assert getMemoryController.getSP() == 0xFFFC

    def testOXCDSP(self, getMemoryController):
        getMemoryController.setPC(0x2000)
        getMemoryController.setMemValue(0x2000, 0x10)
        getMemoryController.setMemValue(0x2001, 0x25)
        OXCD(getMemoryController)
        assert getMemoryController.getSP() == 0xFFFC

    def testOXCDPC(self, getMemoryController):
        getMemoryController.setPC(0x2000)
        getMemoryController.setMemValue(0x2000, 0x10)
        getMemoryController.setMemValue(0x2001, 0x25)
        OXCD(getMemoryController)
        assert getMemoryController.getPC() == 0x2510

    def testOXCDSPValue(self, getMemoryController):
        getMemoryController.setPC(0x2000)
        OXCD(getMemoryController)
        assert getMemoryController.getAsR16(getMemoryController.getMemValue(getMemoryController.getSP()),
                                            getMemoryController.getMemValue(getMemoryController.getSP() + 1)) == 0x2002

    def testOXC9(self, getMemoryController):
        getMemoryController.setPC(0x2000)
        OXCD(getMemoryController)
        OXC9(getMemoryController)
        assert getMemoryController.getPC() == 0x2002

    def testOXC9SP(self, getMemoryController):
        OXCD(getMemoryController)
        OXC9(getMemoryController)
        assert getMemoryController.getSP() == 0xFFFE

    def testOX20Forward(self, getMemoryController):
        getMemoryController.setPC(0x2000)
        getMemoryController.setMemValue(0x2000, 0x10)
        OX20(getMemoryController)
        assert getMemoryController.getPC() == 0x2011

    def testOX20Backward(self, getMemoryController):
        getMemoryController.setPC(0x2000)
        getMemoryController.setMemValue(0x2000, 0x90)
        OX20(getMemoryController)

        assert getMemoryController.getPC() == 0x1F91

    def testOX18(self, getMemoryController):
        getMemoryController.setPC(0x42CB)
        getMemoryController.setMemValue(0x42CB, 0xF4)
        OX20(getMemoryController)

        assert getMemoryController.getPC() == 0x42C0

    def testOX18Forward(self, getMemoryController):
        getMemoryController.setPC(0x2000)
        getMemoryController.setMemValue(0x2000, 0x10)
        OX20(getMemoryController)

        assert getMemoryController.getPC() == 0x2011

    def testOX18Backward(self, getMemoryController):
        getMemoryController.setPC(0x2000)
        getMemoryController.setMemValue(0x2000, 0x90)
        OX20(getMemoryController)

        assert getMemoryController.getPC() == 0x1F91

    def testOXC3PC(self, getMemoryController):
        getMemoryController.setPC(0x2000)
        getMemoryController.setMemValue(0x2000, 0x50)
        getMemoryController.setMemValue(0x2001, 0x01)
        OXC3(getMemoryController)
        assert getMemoryController.getPC() == 0x0150

    def testOXE9PC(self, getMemoryController):
        getMemoryController.setR8(R8ID.H, 0x20)
        getMemoryController.setR8(R8ID.L, 0x01)
        OXE9(getMemoryController)
        assert getMemoryController.getPC() == 0x2001

    def testOXC4NoJump(self, getMemoryController):
        getMemoryController.setZero()
        OXC4(getMemoryController)
        assert getMemoryController.getSP() == 0xFFFE

    def testOXC4JumpSP(self, getMemoryController):
        getMemoryController.setMemValue(0x2000, 0x50)
        getMemoryController.setMemValue(0x2001, 0x01)
        OXC4(getMemoryController)
        assert getMemoryController.getSP() == 0xFFFC

    def testOXC4PC(self, getMemoryController):
        getMemoryController.setPC(0x2000)
        getMemoryController.setMemValue(0x2000, 0x50)
        getMemoryController.setMemValue(0x2001, 0x01)
        OXC4(getMemoryController)
        assert getMemoryController.getPC() == 0x0150
