import pytest

from likeasnail.enumRegister import R8ID
from likeasnail.opCodesADC import adCX


@pytest.mark.adcCmds
class TestADD():

    def testADDCX(self, getMemoryController):
        getMemoryController.setCarry()
        adCX(getMemoryController, 1)

        assert getMemoryController.getR8(R8ID.A) == 2
