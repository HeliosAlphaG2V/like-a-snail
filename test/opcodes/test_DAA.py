import pytest

from likeasnail.enumRegister import R8ID
from likeasnail.opCodesSpecial import OX27


@pytest.mark.daa
class TestDAA():

    def testDAA(self, getMemoryController):
        getMemoryController.setR8(R8ID.A, 0x99)

        OX27(getMemoryController)

        assert getMemoryController.getSubstract() == 0
        assert getMemoryController.getHalfCarry() == 0
        assert getMemoryController.getCarry() == 0
        assert getMemoryController.getZero() == 0
        assert getMemoryController.getR8(R8ID.A) == 0x99

        getMemoryController.setR8(R8ID.A, 0xA9)

        OX27(getMemoryController)

        assert getMemoryController.getSubstract() == 0
        assert getMemoryController.getHalfCarry() == 0
        assert getMemoryController.getCarry() == 1
        assert getMemoryController.getZero() == 0
        assert getMemoryController.getR8(R8ID.A) == 0x9
