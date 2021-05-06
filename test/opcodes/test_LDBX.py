import pytest

from likeasnail.enumRegister import R8ID
from likeasnail.opcodes import OX40, OX41, OX42, OX43, OX44, OX45, OX46, OX47


@pytest.mark.ldCommands
class TestLDBX():

    def testOX40(self, getMemoryController):
        getMemoryController.setR8(R8ID.B, 95)
        OX40(getMemoryController)

        assert getMemoryController.getR8(R8ID.B) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.B, R8ID.B) == True

    def testOX41(self, getMemoryController):
        getMemoryController.setR8(R8ID.C, 95)
        OX41(getMemoryController)

        assert getMemoryController.getR8(R8ID.C) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.B, R8ID.C) == True

    def testOX42(self, getMemoryController):
        getMemoryController.setR8(R8ID.D, 95)
        OX42(getMemoryController)

        assert getMemoryController.getR8(R8ID.B) == 95
        assert getMemoryController.getR8(R8ID.D) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.B, R8ID.D) == True

    def testOX43(self, getMemoryController):
        getMemoryController.setR8(R8ID.E, 95)
        OX43(getMemoryController)

        assert getMemoryController.getR8(R8ID.B) == 95
        assert getMemoryController.getR8(R8ID.E) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.B, R8ID.E) == True

    def testOX44(self, getMemoryController):
        getMemoryController.setR8(R8ID.H, 95)
        OX44(getMemoryController)

        assert getMemoryController.getR8(R8ID.B) == 95
        assert getMemoryController.getR8(R8ID.H) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.B, R8ID.H) == True

    def testOX45(self, getMemoryController):
        getMemoryController.setR8(R8ID.L, 95)
        OX45(getMemoryController)

        assert getMemoryController.getR8(R8ID.B) == 95
        assert getMemoryController.getR8(R8ID.L) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.B, R8ID.L) == True

    def testOX46(self, getMemoryController):
        getMemoryController.setR8(R8ID.H, 95)
        getMemoryController.setR8(R8ID.L, 95)
        getMemoryController.setMemValue(getMemoryController.getAsR16(95, 95), 127)
        OX46(getMemoryController)

        assert getMemoryController.getR8(R8ID.A) == 0
        assert getMemoryController.getR8(R8ID.F) == 0
        assert getMemoryController.getR8(R8ID.B) == 127
        assert getMemoryController.getR8(R8ID.C) == 0
        assert getMemoryController.getR8(R8ID.D) == 0
        assert getMemoryController.getR8(R8ID.E) == 0
        assert getMemoryController.getR8(R8ID.H) == 95
        assert getMemoryController.getR8(R8ID.L) == 95

    def testOX47(self, getMemoryController):
        getMemoryController.setR8(R8ID.A, 95)
        OX47(getMemoryController)

        assert getMemoryController.getR8(R8ID.B) == 95
        assert getMemoryController.getR8(R8ID.A) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.B, R8ID.A) == True
