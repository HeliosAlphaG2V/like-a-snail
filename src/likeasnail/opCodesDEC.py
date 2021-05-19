#!python
#cython: language_level=3
from .enumRegister import R8ID
##from .log import logAction
minimum = 0xFF


def decX(memCntr, x):

    if((1 & x) == 0 and (2 & x) == 0 and (4 & x) == 0 and (8 & x) == 0 and x >= 16):
        memCntr._registerFlags.H = 1
    else:
        memCntr._registerFlags.H = 0

    x -= 1

    # Overflow
    if(x == -1):
        x = minimum

    memCntr._registerFlags.N = 1

    if(x == 0):
        memCntr._registerFlags.Z = 1
    else:
        memCntr._registerFlags.Z = 0

    return x
    # logAction(decX.__name__,
    #           '-',
    #           0,
    #           0x01,
    #           x,
    #           memCntr.getR8(R8ID.F)
    #           )


def decX16(memCntr, ID):

    x = memCntr.getR16FromR8(ID)
    xLog = x
    x -= 1

    # Overflow
    if(x == -1):
        x = 0xFFFF

    memCntr.setR16FromR8(ID, x)

    # logAction(decX16.__name__,
    #           '-',
    #           xLog,
    #           0x01,
    #           x,
    #           memCntr.getR8(R8ID.F)
    #           )

# R16


def OX0B(memCntr):
    decX16(memCntr, R8ID.B)
    return 8


def OX1B(memCntr):
    decX16(memCntr, R8ID.D)
    return 8


def OX2B(memCntr):
    decX16(memCntr, R8ID.H)
    return 8


def OX3B(memCntr):
    sp = memCntr.getSP() - 1

    if(sp < 0):
        sp = 0xFFFF

    memCntr.setSP(sp)
    return 8


def OX35(memCntr):
    address = memCntr.getR16FromR8(R8ID.H)
    value = decX(memCntr, memCntr.getMemValue(address))
    memCntr.setMemValue(address, value)
    return 12

# R8


def OX05(memCntr):
    memCntr._register.B = decX(memCntr, memCntr._register.B)
    return 4


def OX15(memCntr):
    memCntr._register.D = decX(memCntr, memCntr._register.D)
    return 4


def OX0D(memCntr):
    memCntr._register.C = decX(memCntr, memCntr._register.C)
    return 4


def OX1D(memCntr):
    memCntr._register.E = decX(memCntr, memCntr._register.E)
    return 4


def OX25(memCntr):
    memCntr._register.H = decX(memCntr, memCntr._register.H)
    return 4


def OX2D(memCntr):
    memCntr._register.L = decX(memCntr, memCntr._register.L)
    return 4


def OX3D(memCntr):
    memCntr._register.A = decX(memCntr, memCntr._register.A)
    return 4
