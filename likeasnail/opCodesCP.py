#!python
#cython: language_level=3
from .enumRegister import R8ID
from .log import logAction


def cmpX(memCntr, x):

    # ToDo FLAG.H borrow...
    if(memCntr._register.A < x):
        memCntr._registerFlags.C = 1
    else:
        memCntr._registerFlags.C = 0

    if(memCntr._register.A - x == 0):
        memCntr._registerFlags.Z = 1
    else:
        memCntr._registerFlags.Z = 0

    memCntr._registerFlags.N = 1
    logAction(cmpX.__name__, '-', 0, x, 0, memCntr.getR8(R8ID.F))


def OXB8(memCntr):
    cmpX(memCntr, memCntr.getR8(R8ID.B))
    return 4


def OXB9(memCntr):
    cmpX(memCntr, memCntr.getR8(R8ID.C))
    return 4


def OXBA(memCntr):
    cmpX(memCntr, memCntr.getR8(R8ID.D))
    return 4


def OXBB(memCntr):
    cmpX(memCntr, memCntr.getR8(R8ID.E))
    return 4


def OXBC(memCntr):
    cmpX(memCntr, memCntr.getR8(R8ID.H))
    return 4


def OXBD(memCntr):
    cmpX(memCntr, memCntr.getR8(R8ID.L))
    return 4


def OXBE(memCntr):
    cmpX(memCntr, memCntr.memory[memCntr.getR16FromR8(R8ID.H)])
    return 8


def OXBF(memCntr):
    cmpX(memCntr, memCntr.getR8(R8ID.A))
    return 4


def OXFE(memCntr):

    # ToDo FLAG.H borrow...
    if(memCntr._register.A < memCntr.memory[memCntr._register.PC]):
        memCntr._registerFlags.C = 1
    else:
        memCntr._registerFlags.C = 0

    if(memCntr._register.A - memCntr.memory[memCntr._register.PC] == 0):
        memCntr._registerFlags.Z = 1
    else:
        memCntr._registerFlags.Z = 0

    memCntr._registerFlags.N = 1
    memCntr._register.PC = memCntr._register.PC + 1
    return 8
