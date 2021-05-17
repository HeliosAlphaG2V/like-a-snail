import pytest

from likeasnail.enumRegister import R8ID
from likeasnail.opCodesRotate import rrX, OX0F, OX07, OX1F


@pytest.mark.rotateCmds
class TestRotate():

    def testRRX(self, getMemoryController):
        testValue = [0xFF, 0x0F, 0xF0]
        carryValue = [1, 1, 0]
        assertValue = [0x7F, 0x07, 0x78]

        for i in range(0, len(testValue)):
            getMemoryController.setR8(R8ID.A, testValue[i])
            rrX(getMemoryController, R8ID.A)

            assert getMemoryController.getR8(R8ID.A) == assertValue[i]
            assert getMemoryController.getZero() == 0
            assert getMemoryController.getSubstract() == 0
            assert getMemoryController.getHalfCarry() == 0
            assert getMemoryController.getCarry() == carryValue[i]

    def testOX0F(self, getMemoryController):
        testValue = [0xFF, 0x0F, 0xF0]
        carryValue = [1, 1, 0]
        assertValue = [0x7F, 0x87, 0xF8]

        for i in range(0, len(testValue)):
            getMemoryController.setR8(R8ID.A, testValue[i])
            OX0F(getMemoryController)

            assert getMemoryController.getR8(R8ID.A) == assertValue[i]
            assert getMemoryController.getZero() == 0
            assert getMemoryController.getSubstract() == 0
            assert getMemoryController.getHalfCarry() == 0
            assert getMemoryController.getCarry() == carryValue[i]

            print('Step: ' + str(i) + ' done.')

    def testOX07Result(self, getMemoryController):

        getMemoryController.setR8(R8ID.A, 0x0F)
        OX07(getMemoryController)

        assert getMemoryController.getR8(R8ID.A) == 0x1E

    def testOX07Carry(self, getMemoryController):

        getMemoryController.setCarry()
        getMemoryController.setR8(R8ID.A, 0x0F)
        OX07(getMemoryController)

        assert getMemoryController.getR8(R8ID.A) == 0x1F

    def testOX1F(self, getMemoryController):

        getMemoryController.setR8(R8ID.A, 0x0F)
        OX1F(getMemoryController)

        assert getMemoryController.getR8(R8ID.A) == 0x7

    def testOX1FCarry(self, getMemoryController):
        getMemoryController.setR8(R8ID.A, 0x0F)
        OX1F(getMemoryController)

        assert getMemoryController.getCarry() == 1
