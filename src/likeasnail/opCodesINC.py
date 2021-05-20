#!python
#cython: language_level=3
from .enumRegister import R8ID


def incX(memCntr, ID, indirect=False):

    if(indirect):
        reg = memCntr.getMemValue(memCntr.getR16FromR8(ID))
    else:
        reg = memCntr.getR8(ID)

    # Halfcarry from 3rd to 4th bit
    if((((reg & 0x0F) + (0x01 & 0x0F)) & (0x10)) >= 0x10):
        memCntr.setHalfCarry()
    else:
        memCntr.resetHalfCarry()

    reg += 1

    # Overflow
    if(reg > 0xFF):
        reg = 0

    memCntr.resetSubstract()

    if(reg == 0):
        memCntr.setZero()
    else:
        memCntr.resetZero()

    if(indirect):
        memCntr.setMemValue(memCntr.getR16FromR8(ID), reg)
    else:
        memCntr.setR8(ID, reg)


def incX16(memCntr, ID):

    x = memCntr.getR16FromR8(ID)
    x += 1

    # Overflow
    if(x > 0xFFFF):
        x = 0

    memCntr.setR16FromR8(ID, x)

# R16


def OX03(memCntr):
    incX16(memCntr, R8ID.B)
    return 8


def OX13(memCntr):
    incX16(memCntr, R8ID.D)
    return 8


def OX23(memCntr):
    incX16(memCntr, R8ID.H)
    return 8


def OX33(memCntr):
    sp = 1 + memCntr.getSP()

    if(sp == 0x10000):
        sp = 0

    memCntr.setSP(sp)
    return 8


def OX34(memCntr):
    incX(memCntr, R8ID.H, True)
    return 12

# R8


def OX04(memCntr):
    incX(memCntr, R8ID.B)
    return 4


def OX14(memCntr):
    incX(memCntr, R8ID.D)
    return 4


def OX24(memCntr):
    incX(memCntr, R8ID.H)
    return 4


def OX0C(memCntr):
    incX(memCntr, R8ID.C)
    return 4


def OX1C(memCntr):
    incX(memCntr, R8ID.E)
    return 4


def OX2C(memCntr):
    incX(memCntr, R8ID.L)
    return 4


def OX3C(memCntr):
    incX(memCntr, R8ID.A)
    return 4
