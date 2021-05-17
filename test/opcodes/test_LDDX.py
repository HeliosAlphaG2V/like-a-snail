import pytest

from likeasnail.enumRegister import R8ID
from likeasnail.opcodes import OX50, OX51, OX52, OX53, OX54, OX55, OX56, OX57


@pytest.mark.ldCmds
class TestLDDX():

    def testOX50(self, getMemoryController):
        getMemoryController.setR8(R8ID.B, 95)
        OX50(getMemoryController)

        assert getMemoryController.getR8(R8ID.D) == 95
        assert getMemoryController.getR8(R8ID.B) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.D, R8ID.B) == True

    def testOX51(self, getMemoryController):
        getMemoryController.setR8(R8ID.C, 95)
        OX51(getMemoryController)

        assert getMemoryController.getR8(R8ID.D) == 95
        assert getMemoryController.getR8(R8ID.C) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.D, R8ID.C) == True

    def testOX52(self, getMemoryController):
        getMemoryController.setR8(R8ID.D, 95)
        OX52(getMemoryController)

        assert getMemoryController.getR8(R8ID.D) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.D, R8ID.D) == True

    def testOX53(self, getMemoryController):
        getMemoryController.setR8(R8ID.E, 95)
        OX53(getMemoryController)

        assert getMemoryController.getR8(R8ID.D) == 95
        assert getMemoryController.getR8(R8ID.E) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.D, R8ID.E) == True

    def testOX54(self, getMemoryController):
        getMemoryController.setR8(R8ID.H, 95)
        OX54(getMemoryController)

        assert getMemoryController.getR8(R8ID.D) == 95
        assert getMemoryController.getR8(R8ID.H) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.D, R8ID.H) == True

    def testOX55(self, getMemoryController):
        getMemoryController.setR8(R8ID.L, 95)
        OX55(getMemoryController)

        assert getMemoryController.getR8(R8ID.D) == 95
        assert getMemoryController.getR8(R8ID.L) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.D, R8ID.L) == True

    def testOX56(self, getMemoryController):
        getMemoryController.setR8(R8ID.H, 95)
        getMemoryController.setR8(R8ID.L, 95)
        getMemoryController.setMemValue(getMemoryController.getAsR16(95, 95), 127)
        OX56(getMemoryController)

        assert getMemoryController.getR8(R8ID.A) == 0
        assert getMemoryController.getR8(R8ID.F) == 0
        assert getMemoryController.getR8(R8ID.B) == 0
        assert getMemoryController.getR8(R8ID.C) == 0
        assert getMemoryController.getR8(R8ID.D) == 127
        assert getMemoryController.getR8(R8ID.E) == 0
        assert getMemoryController.getR8(R8ID.H) == 95
        assert getMemoryController.getR8(R8ID.L) == 95

    def testOX57(self, getMemoryController):
        getMemoryController.setR8(R8ID.A, 95)
        OX57(getMemoryController)

        assert getMemoryController.getR8(R8ID.D) == 95
        assert getMemoryController.getR8(R8ID.A) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.D, R8ID.A) == True
