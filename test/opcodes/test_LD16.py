import pytest

from likeasnail.enumRegister import R8ID
from likeasnail.opcodes import OX21, OX01, OX02, OX11


@pytest.mark.ldCmds
class TestLD16():

    def testOX21ResultH(self, getMemoryController):

        getMemoryController.setMemValue(0x0000, 0xF0)
        getMemoryController.setMemValue(0x0001, 0xFF)

        OX21(getMemoryController)

        assert getMemoryController.getR8(R8ID.H) == 0xFF

    def testOX21ResultL(self, getMemoryController):

        getMemoryController.setMemValue(0x0000, 0xF0)
        getMemoryController.setMemValue(0x0001, 0xFF)

        OX21(getMemoryController)

        assert getMemoryController.getR8(R8ID.L) == 0xF0

    def testOX01ResultB(self, getMemoryController):

        getMemoryController.setMemValue(0x0000, 0xF0)
        getMemoryController.setMemValue(0x0001, 0xFF)

        OX01(getMemoryController)

        assert getMemoryController.getR8(R8ID.B) == 0xFF

    def testOX01ResultC(self, getMemoryController):

        getMemoryController.setMemValue(0x0000, 0xF0)
        getMemoryController.setMemValue(0x0001, 0xFF)

        OX01(getMemoryController)

        assert getMemoryController.getR8(R8ID.C) == 0xF0

    def testOX11ResultD(self, getMemoryController):

        getMemoryController.setMemValue(0x0000, 0xF0)
        getMemoryController.setMemValue(0x0001, 0xFF)

        OX11(getMemoryController)

        assert getMemoryController.getR8(R8ID.D) == 0xFF

    def testOX11ResultE(self, getMemoryController):

        getMemoryController.setMemValue(0x0000, 0xF0)
        getMemoryController.setMemValue(0x0001, 0xFF)

        OX11(getMemoryController)

        assert getMemoryController.getR8(R8ID.E) == 0xF0

    def testOX02Result(self, getMemoryController):

        getMemoryController.setR8(R8ID.A, 0x20)
        getMemoryController.setR8(R8ID.B, 0x50)
        getMemoryController.setR8(R8ID.C, 0x0F)

        OX02(getMemoryController)

        assert getMemoryController.getMemValue(0x500F) == 0x20
