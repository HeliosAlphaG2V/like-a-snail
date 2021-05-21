#!python
# cython: language_level=3
from .enumRegister import R8ID
##from .log import logAction

# 7th --- 0th
# 0 0 0 0  0 0 0 0
# variable << Bitstelle
# (1 << X) Die 1 um X verschieben

# C 8 7 6 5 4 3 2 1
# 0 0 0 0 0 0 0 0 0
# Rotate left through carry


def rlCX(memCntr, Id):

    nReg = memCntr.getR8(Id)
    carry = 0

    if(memCntr.getCarry() == 1):
        carry = 0x1

    # Test 7th Bit and put it in Carry if 1
    if(nReg & (1 << 7)):
        memCntr.setCarry()
        nReg &= 0x7F
    else:
        memCntr.resetCarry()

    nReg = nReg * 2  # Shift to Left
    nReg |= carry

    memCntr.setR8(Id, nReg)
    memCntr.resetSubstract()
    memCntr.resetHalfCarry()

    if(nReg == 0):
        memCntr.setZero()
    else:
        memCntr.resetZero()


def rlX(memCntr, Id):

    nReg = memCntr.getR8(Id)

    # Test 7th Bit and put it in Carry if 1
    if(nReg & (1 << 7)):
        memCntr.setCarry()
        nReg &= 0x7F
    else:
        memCntr.resetCarry()

    nReg = nReg * 2  # Shift to Left

    memCntr.setR8(Id, nReg)
    memCntr.resetSubstract()
    memCntr.resetHalfCarry()

    if(nReg == 0):
        memCntr.setZero()
    else:
        memCntr.resetZero()

    # logAction('RR ' + str(Id),
    #           'to MSB',
    #           memCntr.getCarry(),
    #           nReg,
    #           memCntr.getR8(Id),
    #           memCntr.getR8(R8ID.F))


def rrCX(memCntr, Id):

    #     logCarryFlag = memCntr.getCarry()
    nReg = memCntr.getR8(Id)

    if(memCntr.getCarry() == 1):
        nReg |= 0x100

    # Test 0th Bit and put it in Carry if 1
    if(nReg & (1 << 0)):
        memCntr.setCarry()
    else:
        memCntr.resetCarry()

    nReg = int(nReg / 2)  # Shift to Right

#     if(logCarryFlag == 1):
#         nReg = nReg | 0x80  # MSB Bit = 1

    memCntr.setR8(Id, nReg)
    memCntr.resetSubstract()
    memCntr.resetHalfCarry()

    if(nReg == 0):
        memCntr.setZero()
    else:
        memCntr.resetZero()


def rrX(memCntr, Id):

    #     logCarryFlag = memCntr.getCarry()
    nReg = memCntr.getR8(Id)

    # Test 0th Bit and put it in Carry if 1
    if(nReg & (1 << 0)):
        memCntr.setCarry()
    else:
        memCntr.resetCarry()

    nReg = int(nReg / 2)  # Shift to Right

#     if(logCarryFlag == 1):
#         nReg = nReg | 0x80  # MSB Bit = 1

    memCntr.setR8(Id, nReg)
    memCntr.resetSubstract()
    memCntr.resetHalfCarry()

    if(nReg == 0):
        memCntr.setZero()
    else:
        memCntr.resetZero()

    # logAction('RR ' + str(Id),
    #           'to MSB',
    #           memCntr.getCarry(),
    #           nReg,
    #           memCntr.getR8(Id),
    #           memCntr.getR8(R8ID.F))


def bitX(memCntr, Id, bit, indirect=False):

    if indirect:
        nReg = memCntr.getMemValue(memCntr.getR16FromR8(Id))
    else:
        nReg = memCntr.getR8(Id)

    if not (nReg & (1 << bit)):
        memCntr.setZero()

    memCntr.resetSubstract()
    memCntr.setHalfCarry()


def setX(memCntr, Id, bit, indirect=False):

    if indirect:
        before = memCntr.getMemValue(memCntr.getR16FromR8(Id))
        nReg = memCntr.getMemValue(memCntr.getR16FromR8(Id)) | (1 << bit)
        memCntr.setMemValue(memCntr.getR16FromR8(Id), nReg)
    else:
        before = memCntr.getR8(Id)
        nReg = memCntr.getR8(Id) | (1 << bit)
        memCntr.setR8(Id, nReg)


def resX(memCntr, Id, bit, indirect=False):

    if indirect:
        nReg = memCntr.getMemValue(memCntr.getR16FromR8(Id)) & ~(1 << bit)
        memCntr.setMemValue(memCntr.getR16FromR8(Id), nReg)
    else:
        nReg = memCntr.getR8(Id) & ~(1 << bit)
        memCntr.setR8(Id, nReg)

# RES X, n


def cbOXBE(memCntr):
    resX(memCntr, R8ID.H, 7, True)

    return 16


def cbOX86(memCntr):
    resX(memCntr, R8ID.H, 0, True)
    return 16


def cbOX87(memCntr):
    resX(memCntr, R8ID.A, 0)
    return 8

# SET X, n


def cbOXDE(memCntr):
    setX(memCntr, R8ID.H, 3, True)
    return 8


def cbOXEE(memCntr):
    setX(memCntr, R8ID.H, 5, True)
    return 8


def cbOXFE(memCntr):
    setX(memCntr, R8ID.H, 7, True)
    return 16

# BIT X, n


def cbOX40(memCntr):
    bitX(memCntr, R8ID.B, 0)
    return 8


def cbOX41(memCntr):
    bitX(memCntr, R8ID.C, 0)
    return 8


def cbOX42(memCntr):
    bitX(memCntr, R8ID.D, 0)
    return 8


def cbOX43(memCntr):
    bitX(memCntr, R8ID.E, 0)
    return 8


def cbOX44(memCntr):
    bitX(memCntr, R8ID.H, 0)
    return 8


def cbOX45(memCntr):
    bitX(memCntr, R8ID.L, 0)
    return 8


def cbOX47(memCntr):
    bitX(memCntr, R8ID.A, 0)
    return 8


def cbOX48(memCntr):
    bitX(memCntr, R8ID.B, 1)
    return 8


def cbOX50(memCntr):
    bitX(memCntr, R8ID.B, 2)
    return 8


def cbOX5F(memCntr):
    bitX(memCntr, R8ID.A, 3)
    return 8


def cbOX60(memCntr):
    bitX(memCntr, R8ID.B, 4)
    return 8


def cbOX61(memCntr):
    bitX(memCntr, R8ID.C, 4)
    return 8


def cbOX69(memCntr):
    bitX(memCntr, R8ID.C, 5)
    return 8


def cbOX58(memCntr):
    bitX(memCntr, R8ID.B, 3)
    return 8


def cbOX68(memCntr):
    bitX(memCntr, R8ID.B, 5)
    return 8


def cbOX7E(memCntr):
    bitX(memCntr, R8ID.H, 7, True)
    return 16


def cbOX6F(memCntr):
    bitX(memCntr, R8ID.A, 5)
    return 8


def cbOX77(memCntr):
    bitX(memCntr, R8ID.A, 6)
    return 8


def cbOX7F(memCntr):
    bitX(memCntr, R8ID.A, 7)
    return 8

# RL X


def cbOX11(memCntr):
    rlCX(memCntr, R8ID.C)
    return 8


def cbOX14(memCntr):
    rlCX(memCntr, R8ID.H)
    return 8

# RR X


def cbOX18(memCntr):
    rrCX(memCntr, R8ID.B)
    return 8


def cbOX19(memCntr):
    rrCX(memCntr, R8ID.C)
    return 8


def cbOX1A(memCntr):
    rrCX(memCntr, R8ID.D)
    return 8


def cbOX1B(memCntr):
    rrCX(memCntr, R8ID.E)
    return 8


def cbOX1C(memCntr):
    rrCX(memCntr, R8ID.H)
    return 8


def cbOX1D(memCntr):
    rrCX(memCntr, R8ID.L)
    return 8


def cbOX1F(memCntr):
    rrCX(memCntr, R8ID.A)
    return 8

# SRL X


def cbOX3F(memCntr):
    rrX(memCntr, R8ID.A)
    return 8


def cbOX38(memCntr):
    rrX(memCntr, R8ID.B)
    return 8

# SLA X


def cbOX27(memCntr):
    rlX(memCntr, R8ID.A)
    return 8


# RRCA


def OX0F(memCntr):
    rrCX(memCntr, R8ID.A)

    memCntr.resetZero()
    return 4

# RRA


def OX1F(memCntr):
    rrCX(memCntr, R8ID.A)

    memCntr.resetZero()
    return 4


# RLCA


def OX07(memCntr):
    rlCX(memCntr, R8ID.A)

    memCntr.resetZero()
    return 4

# RLA


def OX17(memCntr):
    rlCX(memCntr, R8ID.A)

    memCntr.resetZero()
    return 4
