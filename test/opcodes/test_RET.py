import pytest

from likeasnail.enumRegister import R8ID
from likeasnail.opcodes import OXC8


class TestRET():

    def testOXC8(self, getMemoryController):
        getMemoryController.setMemValue(0xFFFD, 0x95)
        getMemoryController.setMemValue(0xFFFC, 0x95)
        getMemoryController.setSP(0xFFFC)
        getMemoryController.setZero()
        OXC8(getMemoryController)

        assert getMemoryController.getMemValue(0xFFFE) == 0
        assert getMemoryController.getMemValue(0xFFFD) == 0x95
        assert getMemoryController.getMemValue(0xFFFC) == 0x95
        assert getMemoryController.getMemValue(0xFFFB) == 0
        assert getMemoryController.getSP() == 0xFFFE
        assert getMemoryController.getPC() == 0x9595
        assert getMemoryController.getR8(R8ID.A) == 0
        assert getMemoryController.getR8(R8ID.B) == 0
        assert getMemoryController.getR8(R8ID.C) == 0
        assert getMemoryController.getR8(R8ID.D) == 0
        assert getMemoryController.getR8(R8ID.E) == 0
        assert getMemoryController.getR8(R8ID.F) == 0x80
        assert getMemoryController.getR8(R8ID.H) == 0
        assert getMemoryController.getR8(R8ID.L) == 0
