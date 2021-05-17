# from likeasnail.opcodes import
from .enumRegister import R8ID


def logPushPop(strType, ID, memCntr):
    return
    # logAction(strType,
    #                   '=',
    #                   memCntr.getAsR16(memCntr.getR8(ID), memCntr.getR8(ID+1)),
    #                   memCntr.getAsR16(memCntr.getR8(ID), memCntr.getR8(ID+1)),
    #                   memCntr.getAsR16(memCntr.getR8(ID), memCntr.getR8(ID+1)),
    #                   memCntr.getR8(R8ID.F))


def OXC1(memCntr):
    memCntr.setR8(R8ID.B, memCntr.pop())
    memCntr.setR8(R8ID.C, memCntr.pop())

    logPushPop('POP BC', R8ID.B, memCntr)
    return 12


def OXD1(memCntr):
    memCntr.setR8(R8ID.D, memCntr.pop())
    memCntr.setR8(R8ID.E, memCntr.pop())

    logPushPop('POP DE', R8ID.D, memCntr)
    return 12


def OXE1(memCntr):
    memCntr.setR8(R8ID.H, memCntr.pop())
    memCntr.setR8(R8ID.L, memCntr.pop())
    logPushPop('POP HL', R8ID.H, memCntr)
    return 12


def OXF1(memCntr):
    memCntr.setR8(R8ID.A, memCntr.pop())
    memCntr.setR8(R8ID.F, memCntr.pop())
    logPushPop('POP AF', R8ID.A, memCntr)
    return 12


def OXC5(memCntr):
    memCntr.push(memCntr.getR8(R8ID.C))
    memCntr.push(memCntr.getR8(R8ID.B))
    logPushPop('PUSH BC', R8ID.B, memCntr)
    return 12


def OXD5(memCntr):
    memCntr.push(memCntr.getR8(R8ID.E))
    memCntr.push(memCntr.getR8(R8ID.D))
    logPushPop('PUSH DE', R8ID.D, memCntr)
    return 12


def OXE5(memCntr):
    memCntr.push(memCntr.getR8(R8ID.L))
    memCntr.push(memCntr.getR8(R8ID.H))
    logPushPop('PUSH HL', R8ID.H, memCntr)
    return 12


def OXF5(memCntr):
    memCntr.push(memCntr.getR8(R8ID.F))
    memCntr.push(memCntr.getR8(R8ID.A))
    logPushPop('PUSH AF', R8ID.A, memCntr)
    return 12
