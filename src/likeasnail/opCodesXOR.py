#!python
#cython: language_level=3
from .enumRegister import R8ID


def xorX(memCntr, x):
    a = x ^ memCntr.getR8(R8ID.A)

    memCntr.setR8(R8ID.A, a)

    memCntr.resetHalfCarry()
    memCntr.resetSubstract()
    memCntr.resetCarry()

    if (a == 0):
        memCntr.setZero()
    else:
        memCntr.resetZero()


def OXA8(memCntr):
    xorX(memCntr, memCntr.getR8(R8ID.B))
    return 4


def OXA9(memCntr):
    xorX(memCntr, memCntr.getR8(R8ID.C))
    return 4


def OXAA(memCntr):
    xorX(memCntr, memCntr.getR8(R8ID.D))
    return 4


def OXAB(memCntr):
    xorX(memCntr, memCntr.getR8(R8ID.E))
    return 4


def OXAC(memCntr):
    xorX(memCntr, memCntr.getR8(R8ID.H))
    return 4


def OXAD(memCntr):
    xorX(memCntr, memCntr.getR8(R8ID.L))
    return 4


def OXAE(memCntr):
    xorX(memCntr, memCntr.getMemValue(memCntr.getR16FromR8(R8ID.H)))
    return 8


def OXAF(memCntr):
    xorX(memCntr, memCntr.getR8(R8ID.A))
    return 4


def OXEE(memCntr):
    xorX(memCntr, memCntr.getNextParam())
    return 8
