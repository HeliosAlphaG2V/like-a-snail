import pytest

from likeasnail.enumRegister import R8ID
from likeasnail.opcodes import OX58, OX59, OX5A, OX5B, OX5C, OX5D, OX5E, OX5F


@pytest.mark.ldCmds
class TestLDBX():

    def testOX58(self, getMemoryController):
        getMemoryController.setR8(R8ID.B, 95)
        OX58(getMemoryController)

        assert getMemoryController.getR8(R8ID.E) == 95
        assert getMemoryController.getR8(R8ID.B) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.E, R8ID.B) == True

    def testOX59(self, getMemoryController):
        getMemoryController.setR8(R8ID.C, 95)
        OX59(getMemoryController)

        assert getMemoryController.getR8(R8ID.E) == 95
        assert getMemoryController.getR8(R8ID.C) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.E, R8ID.C) == True

    def testOX5A(self, getMemoryController):
        getMemoryController.setR8(R8ID.D, 95)
        OX5A(getMemoryController)

        assert getMemoryController.getR8(R8ID.E) == 95
        assert getMemoryController.getR8(R8ID.D) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.E, R8ID.D) == True

    def testOX5B(self, getMemoryController):
        getMemoryController.setR8(R8ID.E, 95)
        OX5B(getMemoryController)

        assert getMemoryController.getR8(R8ID.E) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.E, R8ID.E) == True

    def testOX5C(self, getMemoryController):
        getMemoryController.setR8(R8ID.H, 95)
        OX5C(getMemoryController)

        assert getMemoryController.getR8(R8ID.E) == 95
        assert getMemoryController.getR8(R8ID.H) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.E, R8ID.H) == True

    def testOX5D(self, getMemoryController):
        getMemoryController.setR8(R8ID.L, 95)
        OX5D(getMemoryController)

        assert getMemoryController.getR8(R8ID.E) == 95
        assert getMemoryController.getR8(R8ID.L) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.E, R8ID.L) == True

    def testOX5E(self, getMemoryController):
        getMemoryController.setR8(R8ID.H, 95)
        getMemoryController.setR8(R8ID.L, 95)
        getMemoryController.setMemValue(getMemoryController.getAsR16(95, 95), 127)
        OX5E(getMemoryController)

        assert getMemoryController.getR8(R8ID.A) == 0
        assert getMemoryController.getR8(R8ID.F) == 0
        assert getMemoryController.getR8(R8ID.B) == 0
        assert getMemoryController.getR8(R8ID.C) == 0
        assert getMemoryController.getR8(R8ID.D) == 0
        assert getMemoryController.getR8(R8ID.E) == 127
        assert getMemoryController.getR8(R8ID.H) == 95
        assert getMemoryController.getR8(R8ID.L) == 95

    def testOX5F(self, getMemoryController):
        getMemoryController.setR8(R8ID.A, 95)
        OX5F(getMemoryController)

        assert getMemoryController.getR8(R8ID.E) == 95
        assert getMemoryController.getR8(R8ID.A) == 95
        assert pytest.helpers.allOtherRegisterZero(getMemoryController, R8ID.E, R8ID.A) == True
