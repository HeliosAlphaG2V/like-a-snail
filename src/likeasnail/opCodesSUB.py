#!python
#cython: language_level=3
from .enumRegister import R8ID


def subX(memCntr, currentReg):

    if(memCntr._register.A & (1 << 4) == 0):
        memCntr._register.A = memCntr._register.A - currentReg
        memCntr._registerFlags.H = 0
    else:
        memCntr._register.A = memCntr._register.A - currentReg
        if(memCntr._register.A & (1 << 4) == 1):
            memCntr._registerFlags.H = 1

    if(memCntr._register.A == 0):
        memCntr._registerFlags.Z = 1
        memCntr._registerFlags.C = 0
    else:
        memCntr._registerFlags.Z = 0
        if(memCntr._register.A < 0):
            memCntr._register.A = 0
            memCntr._registerFlags.C = 1
        else:
            memCntr._registerFlags.C = 0

    memCntr._registerFlags.N = 1
    #logAction(subX.__name__, '-', aLog, x, memCntr.getR8(R8ID.A), memCntr.getR8(R8ID.F))


def subCX(memCntr, targetID, sourceID):

    currentReg = memCntr.getR8(sourceID)
    reg = memCntr.getR8(targetID) + memCntr.getCarry()

    if(reg & (1 << 4) == 0):
        reg = reg - currentReg
        memCntr._registerFlags.H = 0
    else:
        reg = reg - currentReg
        if(reg & (1 << 4) == 1):
            memCntr._registerFlags.H = 1

    if(reg == 0):
        memCntr._registerFlags.Z = 1
        memCntr._registerFlags.C = 0
    else:
        memCntr._registerFlags.Z = 0
        if(reg < 0):
            reg = 0
            memCntr._registerFlags.C = 1
        else:
            memCntr._registerFlags.C = 0

    memCntr._registerFlags.N = 1
    memCntr.setR8(targetID, reg)
    #logAction(subX.__name__, '-', aLog, x, memCntr.getR8(R8ID.A), memCntr.getR8(R8ID.F))


def OX90(memCntr):
    subX(memCntr, memCntr._register.B)
    return 4


def OX91(memCntr):
    subX(memCntr, memCntr._register.C)
    return 4


def OX92(memCntr):
    subX(memCntr, memCntr._register.D)
    return 4


def OX93(memCntr):
    subX(memCntr, memCntr._register.E)
    return 4


def OX94(memCntr):
    subX(memCntr, memCntr._register.H)
    return 4


def OX95(memCntr):
    subX(memCntr, memCntr._register.L)
    return 4


def OX96(memCntr):
    subX(memCntr, memCntr.getMemValue(memCntr.getR16FromR8(R8ID.H)))
    return 8


def OX97(memCntr):
    subX(memCntr, memCntr._register.A)
    return 4

#############################################


def OX99(memCntr):
    subCX(memCntr, R8ID.A, R8ID.C)
    return 4


def OX9B(memCntr):
    subCX(memCntr, R8ID.A, R8ID.E)
    return 4


def OX9C(memCntr):
    subCX(memCntr, R8ID.A, R8ID.H)
    return 4


def OX9D(memCntr):
    subCX(memCntr, R8ID.A, R8ID.L)
    return 4


def OX9F(memCntr):
    subCX(memCntr, R8ID.A, R8ID.A)
    return 4

#############################################
# Immediate Data in cartidge
#############################################


def OXD6(memCntr):
    subX(memCntr, memCntr.memory[memCntr.getPC()])
    memCntr.setPC(memCntr.getPC() + 1)
    return 8
