import pytest

from likeasnail.enumRegister import R8ID
from likeasnail.opcodes import OX2F


@pytest.mark.cpl
class TestCPL():

    def testOX2FSubstract(self, getMemoryController):

        OX2F(getMemoryController)
        assert getMemoryController.getSubstract() == 1

    def testOX2FHalfCarry(self, getMemoryController):

        OX2F(getMemoryController)
        assert getMemoryController.getHalfCarry() == 1

    def testOX2FZero(self, getMemoryController):

        OX2F(getMemoryController)
        assert getMemoryController.getZero() == 0

    def testOX2FCarry(self, getMemoryController):

        OX2F(getMemoryController)
        assert getMemoryController.getCarry() == 0

    def testOX2FResult(self, getMemoryController):
        testValue = [0xF0, 0xFF, 0xFF]
        assertValue = [0x0F, 0x00, 0x00]

        for i in range(0, len(testValue)):
            getMemoryController.setR8(R8ID.A, testValue[i])
            OX2F(getMemoryController)
            assert getMemoryController.getR8(R8ID.A) == assertValue[i]
