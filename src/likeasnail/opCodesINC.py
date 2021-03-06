#!python
#cython: language_level=3
from .enumRegister import R8ID
maxIncX = 0x100


def incX(memCntr, ID):
    reg = memCntr.getR8(ID) + 1

    # Overflow
    if(reg == maxIncX):
        reg = 0

    memCntr.resetSubstract()
    # ToDo: Set if carry from Bit 3 => H = 1!

    if(reg == 0):
        memCntr._registerFlags.Z = 1
    else:
        memCntr._registerFlags.Z = 0

    memCntr.setR8(ID, reg)
#     logAction(incX.__name__,
#                       '+',
#                       xLog,
#                       0x01,
#                       x,
#                       memCntr.getR8(R8ID.F)
#                       )


def incX16(memCntr, ID):

    x = memCntr.getR16FromR8(ID)
    #xLog = x
    x += 1

    # Overflow
    if(x > 0xFFFF):
        x = 0

    memCntr.setR16FromR8(ID, x)

#     logAction(incX16.__name__,
#                       '+',
#                       xLog,
#                       0x01,
#                       memCntr.getR16FromR8(ID),
#                       memCntr.getR8(R8ID.F)
#                       )

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
    sp = memCntr.getSP()
    sp += 1
    memCntr.setSP(sp)
    return 8


def OX34(memCntr):
    #     hl = memCntr.getHLValue()
    #     hlLog = hl
    #
    #     hl += 1
    #     memCntr.setR16FromR8(R8ID.H, hl)
    adressHL = memCntr.getR16FromR8(R8ID.H)

    value = memCntr.memory[adressHL]
    #logValue = value
    value += 1

    if(value > 0xFF):
        value = 0
        memCntr.setZero()
    else:
        memCntr.resetZero()

    memCntr.resetSubstract()

    memCntr.setMemValue(adressHL, value)

#     logAction('INC (HL)',
#                       '|',
#                       adressHL,
#                       logValue,
#                       memCntr.getMemValue( adressHL ),
#                       memCntr.getR8(R8ID.F)
#                       )
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
