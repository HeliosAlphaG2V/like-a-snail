import pytest

from likeasnail.enumRegister import R8ID


class TestMemCntr():

    def testInit(self, getMemoryController):
        assert pytest.helpers.allOtherRegisterZero(getMemoryController) == True

    def testSetR8RegisterF(self, getMemoryController):
        getMemoryController.setR8(R8ID.F, 0xFF)
        assert getMemoryController.getR8(R8ID.F) == 0xF0
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.F, R8ID.F) == True

        getMemoryController.setR8(R8ID.F, 0xAF)
        assert getMemoryController.getR8(R8ID.F) == 0xA0
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.F, R8ID.F) == True

        getMemoryController.setR8(R8ID.F, 0x00)
        assert getMemoryController.getR8(R8ID.F) == 0x00
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.F, R8ID.F) == True

        getMemoryController.setR8(R8ID.F, 0x10)
        assert getMemoryController.getR8(R8ID.F) == 0x10
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.F, R8ID.F) == True

    def testGetAsR16(self, getMemoryController):
        assert getMemoryController.getAsR16(0x95, 0x95) == 0x9595
        assert getMemoryController.getAsR16(0x44, 0x23) == 0x4423
