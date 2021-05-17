#!python
#cython: language_level=3
from .enumRegister import R8ID


def adCX(memCntr, x):
    a = memCntr.getR8(R8ID.A)

    # Halfcarry from 3rd to 4th bit
    if((((a & 0x0F) + (x & 0x0F)) & (0x10)) >= 0x10):
        memCntr.setHalfCarry()
    else:
        memCntr.resetHalfCarry()

    if(memCntr.getCarry() == 1):
        a += x + 1
        memCntr.resetCarry()
    else:
        a += x

    # Carry from 7th bit to 8th bit
    if((a & 0x100) >= 0x100):
        memCntr.setCarry()
        a = a & 0xFF
    else:
        memCntr.resetCarry()

    if(a == 0):
        memCntr.setZero()
    else:
        memCntr.resetZero()

    memCntr.resetSubstract()
    memCntr.setR8(R8ID.A, a)


def OXCE(memCntr):
    adCX(memCntr, memCntr.getR8(R8ID.A))
    return 8


def OX89(memCntr):
    adCX(memCntr, memCntr.getR8(R8ID.C))
    return 4


def OX8B(memCntr):
    adCX(memCntr, memCntr.getR8(R8ID.E))
    return 4


def OX8D(memCntr):
    adCX(memCntr, memCntr.getR8(R8ID.L))
    return 4


def OX8E(memCntr):
    adCX(memCntr, memCntr.getMemValue(memCntr.getR16FromR8(R8ID.H)))
    return 8


def OX8F(memCntr):
    adCX(memCntr, memCntr.getR8(R8ID.A))
    return 4
