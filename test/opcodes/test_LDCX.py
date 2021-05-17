import pytest

from likeasnail.enumRegister import R8ID
from likeasnail.opcodes import OX48, OX49, OX4A, OX4B, OX4C, OX4D, OX4E, OX4F


@pytest.mark.ldCmds
class TestLDBX():

    def testOX48(self, getMemoryController):
        getMemoryController.setR8(R8ID.B, 95)
        OX48(getMemoryController)

        assert getMemoryController.getR8(R8ID.C) == 95
        assert getMemoryController.getR8(R8ID.B) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.C, R8ID.B) == True

    def testOX49(self, getMemoryController):
        getMemoryController.setR8(R8ID.C, 95)
        OX49(getMemoryController)

        assert getMemoryController.getR8(R8ID.C) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.C, R8ID.C) == True

    def testOX4A(self, getMemoryController):
        getMemoryController.setR8(R8ID.D, 95)
        OX4A(getMemoryController)

        assert getMemoryController.getR8(R8ID.C) == 95
        assert getMemoryController.getR8(R8ID.D) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.C, R8ID.D) == True

    def testOX4B(self, getMemoryController):
        getMemoryController.setR8(R8ID.E, 95)
        OX4B(getMemoryController)

        assert getMemoryController.getR8(R8ID.C) == 95
        assert getMemoryController.getR8(R8ID.E) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.C, R8ID.E) == True

    def testOX4C(self, getMemoryController):
        getMemoryController.setR8(R8ID.H, 95)
        OX4C(getMemoryController)

        assert getMemoryController.getR8(R8ID.C) == 95
        assert getMemoryController.getR8(R8ID.H) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.C, R8ID.H) == True

    def testOX4D(self, getMemoryController):
        getMemoryController.setR8(R8ID.L, 95)
        OX4D(getMemoryController)

        assert getMemoryController.getR8(R8ID.C) == 95
        assert getMemoryController.getR8(R8ID.L) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.C, R8ID.L) == True

    def testOX4E(self, getMemoryController):
        getMemoryController.setR8(R8ID.H, 95)
        getMemoryController.setR8(R8ID.L, 95)
        getMemoryController.setMemValue(getMemoryController.getAsR16(95, 95), 127)
        OX4E(getMemoryController)

        assert getMemoryController.getR8(R8ID.A) == 0
        assert getMemoryController.getR8(R8ID.F) == 0
        assert getMemoryController.getR8(R8ID.B) == 0
        assert getMemoryController.getR8(R8ID.C) == 127
        assert getMemoryController.getR8(R8ID.D) == 0
        assert getMemoryController.getR8(R8ID.E) == 0
        assert getMemoryController.getR8(R8ID.H) == 95
        assert getMemoryController.getR8(R8ID.L) == 95

    def testOX4F(self, getMemoryController):
        getMemoryController.setR8(R8ID.A, 95)
        OX4F(getMemoryController)

        assert getMemoryController.getR8(R8ID.C) == 95
        assert getMemoryController.getR8(R8ID.A) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.C, R8ID.A) == True
