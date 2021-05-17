#!python
#cython: language_level=3
from struct import pack, unpack

from .enumRegister import R8ID


##from .log import logAction
def addX(memCntr, x):
    a = memCntr.getR8(R8ID.A)
    aLog = a

    # Halfcarry from 3rd to 4th bit
    if((((a & 0x0F) + (x & 0x0F)) & (0x10)) >= 0x10):
        memCntr.setHalfCarry()
    else:
        memCntr.resetHalfCarry()

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

    # logAction(addX.__name__,
    #           '+',
    #           aLog,
    #           x,
    #           memCntr.getR8(R8ID.A),
    #           memCntr.getR8(R8ID.F)
    #           )


def addXR16(memCntr, x, value, ID):

    # Halfcarry from 7th to 8th bit
    if((((x & 0xFF) + (value & 0xFF)) & (0x100)) >= 0x100):
        memCntr.setHalfCarry()
    else:
        memCntr.resetHalfCarry()

    x += value

    # Remove possible overflow
    if(x > 0xFFFF):
        x &= 0xFFFF
        memCntr.setCarry()

    memCntr.resetSubstract()

    bArray = memCntr.getTwoR8FromR16(x)

    memCntr.setR8(ID, bArray[0])
    memCntr.setR8(ID + 1, bArray[1])

    # logAction(addXR16.__name__,
    #           '+',
    #           xLog,
    #           value,
    #           memCntr.getR16FromR8(ID),
    #           memCntr.getR8(R8ID.F))

# SP


def OXF8(memCntr):
    param = memCntr.getNextParam()
    sp = memCntr.getSP()

    # Halfcarry from 7th to 8th bit
    if((((sp & 0xFF) + (param & 0xFF)) & (0x100)) >= 0x100):
        memCntr.setHalfCarry()
    else:
        memCntr.resetHalfCarry()

    signedJpValue = unpack('b', pack('B', param))[0]
    sp += signedJpValue

    # Remove possible overflow
    if(sp > 0xFFFF):
        sp &= 0xFFFF
        memCntr.setCarry()
    elif(sp < 0):
        sp = 0xFFFF + sp

    memCntr.resetSubstract()
    memCntr.resetZero()
    memCntr.setR16FromR8(R8ID.H, sp)

    return 8


def OXE8(memCntr):
    param = memCntr.getNextParam()
    sp = memCntr.getSP()

    # Halfcarry from 7th to 8th bit
    if((((sp & 0xFF) + (param & 0xFF)) & (0x100)) >= 0x100):
        memCntr.setHalfCarry()
    else:
        memCntr.resetHalfCarry()

    signedJpValue = unpack('b', pack('B', param))[0]
    sp += signedJpValue

    # Remove possible overflow
    if(sp > 0xFFFF):
        sp &= 0xFFFF
        memCntr.setCarry()
    elif(sp < 0):
        sp = 0xFFFF + sp

    memCntr.resetSubstract()
    memCntr.resetZero()
    memCntr.setSP(sp)

    return 8

# R16


def OX09(memCntr):
    hl = memCntr.getR16FromR8(R8ID.H)
    bc = memCntr.getR16FromR8(R8ID.B)
    addXR16(memCntr, hl, bc, R8ID.H)
    return 8


def OX19(memCntr):
    de = memCntr.getR16FromR8(R8ID.D)
    hl = memCntr.getR16FromR8(R8ID.H)
    addXR16(memCntr, hl, de, R8ID.H)
    return 8


def OX29(memCntr):
    hl = memCntr.getR16FromR8(R8ID.H)
    addXR16(memCntr, hl, hl, R8ID.H)
    return 8


def OX39(memCntr):
    sp = memCntr.getSP()
    hl = memCntr.getR16FromR8(R8ID.H)
    addXR16(memCntr, hl, sp, R8ID.H)
    return 8

# R8


def OX80(memCntr):
    addX(memCntr, memCntr.getR8(R8ID.B))
    return 4


def OX81(memCntr):
    addX(memCntr, memCntr.getR8(R8ID.C))
    return 4


def OX82(memCntr):
    addX(memCntr, memCntr.getR8(R8ID.D))
    return 4


def OX83(memCntr):
    addX(memCntr, memCntr.getR8(R8ID.E))
    return 4


def OX84(memCntr):
    addX(memCntr, memCntr.getR8(R8ID.H))
    return 4


def OX85(memCntr):
    addX(memCntr, memCntr.getR8(R8ID.L))
    return 4


def OX86(memCntr):
    addX(memCntr, memCntr.memory[memCntr.getR16FromR8(R8ID.H)])
    return 4


def OX87(memCntr):
    addX(memCntr, memCntr.getR8(R8ID.A))
    return 4


def OXC6(memCntr):
    addX(memCntr, memCntr.getNextParam())
    return 8
