import pytest

from likeasnail.enumRegister import R8ID
from likeasnail.memoryController import MemCntr


@pytest.helpers.register
def allOtherRegisterZero(memCntr, R1=99, R2=99):
    for i in range(0, 8):
        if memCntr.getR8(i) != 0 and i != R1 and i != R2:
            print('Register ' + str(i) + ' failed, value: ' + str(memCntr.getR8(i)))
            return False

    return True


@pytest.fixture
def memCntr():
    return MemCntr(rom='', boot='', skip=True)


@pytest.fixture
def getMemoryController(memCntr):
    yield memCntr
    memCntr.setR8(R8ID.A, 0)
    memCntr.setR8(R8ID.F, 0)

    memCntr.setR8(R8ID.B, 0)
    memCntr.setR8(R8ID.C, 0)

    memCntr.setR8(R8ID.D, 0)
    memCntr.setR8(R8ID.E, 0)

    memCntr.setR8(R8ID.H, 0)
    memCntr.setR8(R8ID.L, 0)
