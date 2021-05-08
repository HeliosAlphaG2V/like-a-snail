#from .log import logAction
from .enumRegister import R8ID


def orrX(memCntr, x):
    a = memCntr.getR8(R8ID.A)
    aLog = a
    a = a | memCntr.getReduced(x)

    memCntr.setR8(R8ID.A, a)

    memCntr.resetSubstract()
    memCntr.resetHalfCarry()
    memCntr.resetCarry()

    if(a == 0):
        memCntr.setZero()
    else:
        memCntr.resetZero()

    # logAction(orrX.__name__, '|', aLog, x,
    #                   memCntr.getR8(R8ID.A), memCntr.getR8(R8ID.F))


def OXB0(memCntr):
    orrX(memCntr, memCntr.getR8(R8ID.B))
    return 4


def OXB1(memCntr):
    orrX(memCntr, memCntr.getR8(R8ID.C))
    return 4


def OXB2(memCntr):
    orrX(memCntr, memCntr.getR8(R8ID.D))
    return 4


def OXB3(memCntr):
    orrX(memCntr, memCntr.getR8(R8ID.E))
    return 4


def OXB4(memCntr):
    orrX(memCntr, memCntr.getR8(R8ID.H))
    return 4


def OXB5(memCntr):
    orrX(memCntr, memCntr.getR8(R8ID.L))
    return 4


def OXB6(memCntr):
    orrX(memCntr, memCntr.getR16FromR8(R8ID.H))
    return 8


def OXB7(memCntr):
    orrX(memCntr, memCntr.getR8(R8ID.A))
    return 4


def OXF6(memCntr):
    orrX(memCntr, memCntr.getNextParam())
    return 8
