# !python
# cython: language_level=3

from _ast import Or
import logging
import os
from struct import pack, unpack
import sys

from .enumRegister import R8ID
from .log import logState
from .opCodesADC import (OX89, OX8B, OX8D, OX8F, OXCE, OX8E)
from .opCodesADD import (OX80, OX81, OX82, OX83, OX84, OX85, OX86, OX87, OXC6, OX19, OX29, OX39, OXE8, OXF8, OX09)
from .opCodesAND import (OXA0, OXA1, OXA2, OXA3, OXA4, OXA5, OXA6, OXA7, OXE6)
from .opCodesCP import (OXB8, OXB9, OXBA, OXBB, OXBC, OXBD, OXBE, OXBF, OXFE)
from .opCodesDEC import (OX05, OX15, OX0D, OX1D, OX25, OX2B, OX2D, OX35, OX3D, OX0B, OX1B, OX3B)
from .opCodesINC import (OX03, OX13, OX23, OX2C, OX33, OX34, OX3C, OX04, OX14, OX24, OX0C, OX1C)
from .opCodesJUMP import (OX18, OXD0, OX20, OX28, OX30, OX38, OXC0, OXC3, OXC4, OXC7, OXC8, OXC9, OXCA, OXD4,
                          OXDA, OXCD, OXCF, OXD7, OXD9, OXDF, OXE7, OXE9, OXEF, OXF7, OXFF, OXD8, OXC2)
from .opCodesOR import (OXB0, OXB1, OXB2, OXB3, OXB4, OXB5, OXB6, OXB7, OXF6)
from .opCodesPushPop import (OXC1, OXD1, OXE1, OXF1, OXC5, OXD5, OXE5, OXF5)
from .opCodesRotate import (OX07, OX17, OX0F, OX1F, cbOX11, cbOX18, cbOX19, cbOX1A, cbOX1B, cbOX1C, cbOX1D,
                            cbOX1F, cbOX47, cbOX61, cbOX69, cbOX3F, cbOX40, cbOX41, cbOX42, cbOX43, cbOX44, cbOX42,
                            cbOX86, cbOX14, cbOX87, cbOX48, cbOX5F, cbOX6F, cbOX77, cbOX41, cbOXDE, cbOX68, cbOX60, cbOX58,
                            cbOXFE, cbOXBE, cbOX38, cbOXEE, cbOX7E, cbOX27, cbOX7E, cbOX7F, cbOX50)
from .opCodesSUB import (OX90, OX91, OX92, OX93, OX94, OX95, OX96, OX97, OXD6, OX99, OX9B, OX9D, OX9F, OX9C)
from .opCodesSpecial import (OX00, OX10, OX76, OXF3, OXFB, OX27, OX3F)
from .opCodesXOR import (OXA8, OXA9, OXAA, OXAB, OXAC, OXAD, OXAE, OXAF, OXEE)


#from .opCodesJUMP import OX18, OX20, OX28, OX30, OX38, OXC0, OXC3, OXC4, OXC7, OXC8, OXC9, OXCA, OXDA, OXCD, OXCF, OXD7, OXD9, OXDF, OXE7, OXE9, OXEF, OXF7, OXFF
#from .memoryController import MemCntr
# lp = line_profiler.LineProfiler()
# FORMAT = '%(funcName)s %(message)s %(filename=gb.log)s'
# logging.basicConfig(format=FORMAT)
# '%(funcName)s, \t\t\t%(message)s'
# # Helper functions

# NOP
def OXD3(*_):
    return 0


def OXE4(*_):
    return 0


def OXE3(*_):
    return 0


def OXF4(*_):
    return 0


def OXFC(*_):
    return 0


def OXEC(*_):
    return 0


def OXED(*_):
    return 0


def OXEB(*_):
    return 0


def OXDD(*_):
    return 0


def OXDB(*_):
    return 0


def OXFD(*_):
    return 0


'''
### Address calculation opcodes
'''


# LD (a16), SP
def OX08(memCntr):
    para1 = memCntr.getNextParam()
    para2 = memCntr.getNextParam()

    adr = memCntr.getAsR16(para2, para1)

    bArray = memCntr.getTwoR8FromR16(memCntr.getSP())

    memCntr.setMemValue(adr, bArray[1])
    memCntr.setMemValue(adr + 1, bArray[0])

    return 20


# LD SP, HL
def OXF9(memCntr):
    hl = memCntr.getR16FromR8(R8ID.H)
    memCntr.setSP(hl)

    # logAction('SP, HL',
    #           '<>',
    #           0,
    #           hl,
    #           memCntr.getSP(),
    #           memCntr.getR8(R8ID.F))
    return 8


# LD (BC), A
def OX02(memCntr):
    bc = memCntr.getR16FromR8(R8ID.B)
    memCntr.setMemValue(bc, memCntr.getR8(R8ID.A))
    return 8


# LD A, (BC)
def OX0A(memCntr):
    bc = memCntr.getR16FromR8(R8ID.B)
    memValue = memCntr.getMemValue(bc)
    memCntr.setR8(R8ID.A, memValue)
    return 8


# LD (DE), A
def OX12(memCntr):
    de = memCntr.getR16FromR8(R8ID.D)
    memCntr.setMemValue(de, memCntr.getR8(R8ID.A))
    return 8


# LD A, (DE)
def OX1A(memCntr):
    de = memCntr.getR16FromR8(R8ID.D)
    memValue = memCntr.getMemValue(de)
    memCntr.setR8(R8ID.A, memValue)
    return 8


# LD (HL+), A
def OX22(memCntr):
    hl = memCntr.getR16FromR8(R8ID.H)
    memCntr.setMemValue(hl, memCntr.getR8(R8ID.A))
    hl += 1
    memCntr.setR16FromR8(R8ID.H, hl)
    return 8


# LD (HL-), A
def OX32(memCntr):
    hl = memCntr.getR16FromR8(R8ID.H)
    memCntr.setMemValue(hl, memCntr.getR8(R8ID.A))
    hl -= 1
    memCntr.setR16FromR8(R8ID.H, hl)

    # logAction(OX32.__name__,
    #           '|',
    #           hl,
    #           memCntr.getR8(R8ID.A),
    #           memCntr.getMemValue(hl + 1),
    #           memCntr.getR8(R8ID.F))

    return 8


# LD A, (HL+)
def OX2A(memCntr):
    hl = memCntr.getR16FromR8(R8ID.H)

    memValue = memCntr.getMemValue(hl)
    memCntr.setR8(R8ID.A, memValue)

    hl += 1
    memCntr.setR16FromR8(R8ID.H, hl)
    return 8


# LD A, (HL-)
def OX3A(memCntr):
    hl = memCntr.getR16FromR8(R8ID.H)

    memValue = memCntr.getMemValue(hl)
    memCntr.setR8(R8ID.A, memValue)

    hl -= 1

    if(hl == -1):
        hl = 0xFFFF

    memCntr.setR16FromR8(R8ID.H, hl)
    return 8


# LD (HL), X
def LDHLx(memCntr, x):
    hl = memCntr.getR16FromR8(R8ID.H)
    xLog = memCntr.getMemValue(hl)
    memCntr.setMemValue(hl, x)

    # logAction(LDxHL.__name__,
    #           '=',
    #           xLog,
    #           x,
    #           memCntr.getMemValue(hl),
    #           memCntr.getR8(R8ID.F)
    #           )


def OX36(memCntr):
    LDHLx(memCntr, memCntr.getNextParam())
    return 12


def OX70(memCntr):
    LDHLx(memCntr, memCntr.getR8(R8ID.B))
    return 8


def OX71(memCntr):
    LDHLx(memCntr, memCntr.getR8(R8ID.C))
    return 8


def OX72(memCntr):
    LDHLx(memCntr, memCntr.getR8(R8ID.D))
    return 8


def OX73(memCntr):
    LDHLx(memCntr, memCntr.getR8(R8ID.E))
    return 8


def OX74(memCntr):
    LDHLx(memCntr, memCntr.getR8(R8ID.H))
    return 8


def OX75(memCntr):
    LDHLx(memCntr, memCntr.getR8(R8ID.L))
    return 8


def OX77(memCntr):
    LDHLx(memCntr, memCntr.getR8(R8ID.A))
    return 8


# LD X, (HL)
def LDxHL(memCntr, ID):
    hl = memCntr.getR16FromR8(R8ID.H)
    memValue = memCntr.getMemValue(hl)
    memCntr.setR8(ID, memValue)


def OX46(memCntr):
    LDxHL(memCntr, R8ID.B)
    return 8


def OX56(memCntr):
    LDxHL(memCntr, R8ID.D)
    return 8


def OX66(memCntr):
    LDxHL(memCntr, R8ID.H)
    return 8


def OX4E(memCntr):
    LDxHL(memCntr, R8ID.C)
    return 8


def OX5E(memCntr):
    LDxHL(memCntr, R8ID.E)
    return 8


def OX6E(memCntr):
    LDxHL(memCntr, R8ID.L)
    return 8


def OX7E(memCntr):
    LDxHL(memCntr, R8ID.A)
    return 8


# LDH X, X --- r8 (0xFF00 = 65280)
def OXE0(memCntr):
    adrParam = memCntr.getNextParam()
    memCntr.setMemValue(memCntr.getADR(0xFF, adrParam), memCntr.getR8(R8ID.A))
    return 12


def OXF0(memCntr):
    memCntr._register.A = memCntr.memory[0xFF00 |
                                         memCntr.memory[memCntr._register.PC]]
    memCntr._register.PC = memCntr._register.PC + 1

    # logAction("OXF0",
    #           '->',
    #           0xFF00 | memCntr.memory[memCntr._register.PC],
    #           memCntr.getMemValue(
    #               0xFF00 | memCntr.memory[memCntr._register.PC]),
    #           memCntr.getR8(R8ID.A),
    #           memCntr.getR8(R8ID.F))
    return 12


def OXE2(memCntr):
    memCntr.setMemValue(memCntr.getADR(
        0xFF, memCntr.getR8(R8ID.C)), memCntr.getR8(R8ID.A))
    return 8


def OXF2(memCntr):
    memValue = memCntr.getMemValue(memCntr.getADR(0xFF, memCntr.getR8(R8ID.C)))
    memCntr.setR8(R8ID.A, memValue)
    return 8


# LD X, X --- r16
def OXEA(memCntr):
    param1 = memCntr.getNextParam()
    param2 = memCntr.getNextParam()

    adr = memCntr.getADR(param2, param1)
    memCntr.setMemValue(adr, memCntr.getR8(R8ID.A))
    return 16


def OXFA(memCntr):
    param1 = memCntr.getNextParam()
    param2 = memCntr.getNextParam()

    adr = memCntr.getADR(param2, param1)
    memValue = memCntr.getMemValue(adr)
    memCntr.setR8(R8ID.A, memValue)
    return 16

###################################################


'''
### LD R, r8 ---- 8 Bit into Register
'''


def LD_R8(memCntr, ID):
    param = memCntr.getNextParam()
    oldLog = memCntr.getR8(ID)
    memCntr.setR8(ID, param)

    # logAction(LD_R8.__name__,
    #           '<',
    #           oldLog,
    #           param,
    #           memCntr.getR8(ID),
    #           memCntr.getR8(R8ID.F)
    #           )


def OX06(memCntr):
    LD_R8(memCntr, R8ID.B)
    return 8


def OX16(memCntr):
    LD_R8(memCntr, R8ID.D)
    return 8


def OX26(memCntr):
    LD_R8(memCntr, R8ID.H)
    return 8


def OX0E(memCntr):
    LD_R8(memCntr, R8ID.C)
    return 8


def OX1E(memCntr):
    LD_R8(memCntr, R8ID.E)
    return 8


def OX2E(memCntr):
    LD_R8(memCntr, R8ID.L)
    return 8


def OX3E(memCntr):
    LD_R8(memCntr, R8ID.A)
    return 8

###################################################


'''
### LD R, R ---- Register to Register
'''


def LD_RToR(memCntr, Rtarget, Rsource):
    oldLog = memCntr.getR8(Rtarget)

    # memCntr.registers[Rtarget] = memCntr.registers[Rsource]
    memCntr.setR8(Rtarget, memCntr.getR8(Rsource))
    # logAction(LD_RToR.__name__,
    #           '<',
    #           oldLog,
    #           memCntr.getR8(Rsource),
    #           memCntr.getR8(Rtarget),
    #           memCntr.getR8(R8ID.F)
    #           )


# LD B, X
def OX40(memCntr):
    LD_RToR(memCntr, R8ID.B, R8ID.B)
    return 4


def OX41(memCntr):
    LD_RToR(memCntr, R8ID.B, R8ID.C)
    return 4


def OX42(memCntr):
    LD_RToR(memCntr, R8ID.B, R8ID.D)
    return 4


def OX43(memCntr):
    LD_RToR(memCntr, R8ID.B, R8ID.E)
    return 4


def OX44(memCntr):
    LD_RToR(memCntr, R8ID.B, R8ID.H)
    return 4


def OX45(memCntr):
    LD_RToR(memCntr, R8ID.B, R8ID.L)
    return 4


def OX47(memCntr):
    LD_RToR(memCntr, R8ID.B, R8ID.A)
    return 4


# LD C, X
def OX48(memCntr):
    LD_RToR(memCntr, R8ID.C, R8ID.B)
    return 4


def OX49(memCntr):
    LD_RToR(memCntr, R8ID.C, R8ID.C)
    return 4


def OX4A(memCntr):
    LD_RToR(memCntr, R8ID.C, R8ID.D)
    return 4


def OX4B(memCntr):
    LD_RToR(memCntr, R8ID.C, R8ID.E)
    return 4


def OX4C(memCntr):
    LD_RToR(memCntr, R8ID.C, R8ID.H)
    return 4


def OX4D(memCntr):
    LD_RToR(memCntr, R8ID.C, R8ID.L)
    return 4


def OX4F(memCntr):
    LD_RToR(memCntr, R8ID.C, R8ID.A)
    return 4


# LD D, X
def OX50(memCntr):
    LD_RToR(memCntr, R8ID.D, R8ID.B)
    return 4


def OX51(memCntr):
    LD_RToR(memCntr, R8ID.D, R8ID.C)
    return 4


def OX52(memCntr):
    LD_RToR(memCntr, R8ID.D, R8ID.D)
    return 4


def OX53(memCntr):
    LD_RToR(memCntr, R8ID.D, R8ID.E)
    return 4


def OX54(memCntr):
    LD_RToR(memCntr, R8ID.D, R8ID.H)
    return 4


def OX55(memCntr):
    LD_RToR(memCntr, R8ID.D, R8ID.L)
    return 4


def OX57(memCntr):
    LD_RToR(memCntr, R8ID.D, R8ID.A)
    return 4


# LD E, X
def OX58(memCntr):
    LD_RToR(memCntr, R8ID.E, R8ID.B)
    return 4


def OX59(memCntr):
    LD_RToR(memCntr, R8ID.E, R8ID.C)
    return 4


def OX5A(memCntr):
    LD_RToR(memCntr, R8ID.E, R8ID.D)
    return 4


def OX5B(memCntr):
    LD_RToR(memCntr, R8ID.E, R8ID.E)
    return 4


def OX5C(memCntr):
    LD_RToR(memCntr, R8ID.E, R8ID.H)
    return 4


def OX5D(memCntr):
    LD_RToR(memCntr, R8ID.E, R8ID.L)
    return 4


def OX5F(memCntr):
    LD_RToR(memCntr, R8ID.E, R8ID.A)
    return 4


# LD H, X
def OX60(memCntr):
    LD_RToR(memCntr, R8ID.H, R8ID.B)
    return 4


def OX61(memCntr):
    LD_RToR(memCntr, R8ID.H, R8ID.C)
    return 4


def OX62(memCntr):
    LD_RToR(memCntr, R8ID.H, R8ID.D)
    return 4


def OX63(memCntr):
    LD_RToR(memCntr, R8ID.H, R8ID.E)
    return 4


def OX64(memCntr):
    LD_RToR(memCntr, R8ID.H, R8ID.H)
    return 4


def OX65(memCntr):
    LD_RToR(memCntr, R8ID.H, R8ID.L)
    return 4


def OX67(memCntr):
    LD_RToR(memCntr, R8ID.H, R8ID.A)
    return 4


# LD L, X
def OX68(memCntr):
    LD_RToR(memCntr, R8ID.L, R8ID.B)
    return 4


def OX69(memCntr):
    LD_RToR(memCntr, R8ID.L, R8ID.C)
    return 4


def OX6A(memCntr):
    LD_RToR(memCntr, R8ID.L, R8ID.D)
    return 4


def OX6B(memCntr):
    LD_RToR(memCntr, R8ID.L, R8ID.E)
    return 4


def OX6C(memCntr):
    LD_RToR(memCntr, R8ID.L, R8ID.H)
    return 4


def OX6D(memCntr):
    LD_RToR(memCntr, R8ID.L, R8ID.L)
    return 4


def OX6F(memCntr):
    LD_RToR(memCntr, R8ID.L, R8ID.A)
    return 4


# LD A, X
def OX78(memCntr):
    LD_RToR(memCntr, R8ID.A, R8ID.B)
    return 4


def OX79(memCntr):
    LD_RToR(memCntr, R8ID.A, R8ID.C)
    return 4


def OX7A(memCntr):
    LD_RToR(memCntr, R8ID.A, R8ID.D)
    return 4


def OX7B(memCntr):
    LD_RToR(memCntr, R8ID.A, R8ID.E)
    return 4


def OX7C(memCntr):
    LD_RToR(memCntr, R8ID.A, R8ID.H)
    return 4


def OX7D(memCntr):
    LD_RToR(memCntr, R8ID.A, R8ID.L)
    return 4


def OX7F(memCntr):
    LD_RToR(memCntr, R8ID.A, R8ID.A)
    return 4

###################################################


# CPL A
def OX2F(memCntr):
    a = memCntr.getR8(R8ID.A)
    aNew = ~a

    if aNew < 0:
        aNew = unpack('H', pack('h', aNew))[0]

        # Ignore first byte
        bArray = aNew.to_bytes(2, byteorder='big', signed=False)
        aNew = bArray[1]

    memCntr.setR8(R8ID.A, aNew)
    memCntr.setHalfCarry()
    memCntr.setSubstract()

    # logAction(OX2F.__name__, '~', a, aNew,
    #           memCntr.getR8(R8ID.A), memCntr.getR8(R8ID.F))
    return 4


# LD BC, d16
def OX01(memCntr):
    memCntr.setR8(R8ID.C, memCntr.memory[memCntr._register.PC])
    memCntr.setR8(R8ID.B, memCntr.memory[memCntr._register.PC + 1])
    memCntr._register.PC = memCntr._register.PC + 2
    return 12


# LD DE, d16
def OX11(memCntr):
    memCntr.setR8(R8ID.E, memCntr.memory[memCntr._register.PC])
    memCntr.setR8(R8ID.D, memCntr.memory[memCntr._register.PC + 1])
    memCntr._register.PC = memCntr._register.PC + 2
    return 12


# LD SP, d16
def OX31(memCntr):
    sp = memCntr.getAsR16(
        memCntr.memory[memCntr._register.PC + 1], memCntr.memory[memCntr._register.PC])
    memCntr._register.PC = memCntr._register.PC + 2
    memCntr.setSP(sp)
    # logAction('SP d16',
    #           '<>',
    #           memCntr.memory[memCntr._register.PC + 1],
    #           memCntr.memory[memCntr._register.PC],
    #           sp,
    #           memCntr.getR8(R8ID.F))
    return 12
#     memCntr.setSP(
#         int.from_bytes(
#         bytearray([para2, para1]),
#         byteorder='big',
#         signed=False)
#     )


# LD HL, d16
def OX21(memCntr):
    memCntr.setR8(R8ID.L, memCntr.memory[memCntr._register.PC])
    memCntr.setR8(R8ID.H, memCntr.memory[memCntr._register.PC + 1])
    memCntr._register.PC = memCntr._register.PC + 2

    # logAction('LD HL d16',
    #           '_',
    #           memCntr.getR8(R8ID.H),
    #           memCntr.getR8(R8ID.L),
    #           memCntr.getAsR16(memCntr.getR8(R8ID.H), memCntr.getR8(R8ID.L)),
    #           memCntr.getR8(R8ID.F))

    return 12


'''
### CB Codes
'''


# Swap A upper with higher nibbles
def cbOX37(memCntr):

    a = memCntr.getR8(R8ID.A)
    x = a

    for i in range(0, 4):
        x *= 2

        # Remove 9th Bit and add put it to the start
        if(x & (1 << 8)):
            x = x | (1 << 0)
            x = x & ~(1 << 8)

    if(x == 0):
        memCntr.setZero()
    else:
        memCntr.resetZero()

    memCntr.resetSubstract()
    memCntr.resetHalfCarry()
    memCntr.resetCarry()

    memCntr.setR8(R8ID.A, x)

    # logAction(cbOX37.__name__,
    #           '#',
    #           a,
    #           x,
    #           memCntr.getR8(R8ID.A),
    #           memCntr.getR8(R8ID.F))
    return 8


# # Test bit 7 of H
def cbOX7C(memCntr):

    if(memCntr.getR8(R8ID.H) & (1 << 7) == 0):
        memCntr._registerFlags.Z = 1
    else:
        memCntr._registerFlags.Z = 0

    memCntr._registerFlags.N = 0
    memCntr._registerFlags.H = 1

    # logAction('B7 = 0',
    #           'B7',
    #           0xFF,
    #           0x80,
    #           memCntr.getR8(R8ID.H),
    #           memCntr.getR8(R8ID.F))
    return 8


# def OXCB(memCntr):
#     cbCode = memCntr.getNextParam()
#     func = globals()["cbOX%0.2X" % cbCode]
#     return func(memCntr) + 4  # +4 cycles for fetching cb

# Analysis


def OXCB(memCntr):
    cbCode = memCntr.getNextParam()
    func = globals()["cbOX%0.2X" % cbCode]

    # if str("cbOX%0.2X" % cbCode) in globals():
    #     func = globals()["cbOX%0.2X" % cbCode]
    #
    #     print('PC: ' + format(memCntr.getPC(), '02X') + ' - ' + func.__name__)
    #
    #     func(memCntr)
    #
    #     key = str("cbOX%0.2X" % cbCode)
    #
    #     if(thisdict.get(key, -1) == -1):
    #         thisdict.setdefault(key, 1)
    #     else:
    #         value = thisdict.pop(key)
    #         thisdict.setdefault(key, value + 1)
    # else:
    #     print("cbOX%0.2X" % cbCode)
    #
    #     if(str("cbOX%0.2X" % cbCode) == 'cbOX78' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOX71' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOX32' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOX77' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOX6F' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOX3F' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOX13' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOX50' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOX60' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOX68' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOX58' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOX7F' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOX5F' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOXFE' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOX47' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOX70' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOX40' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOX48' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOX79' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOX57' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOX07' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOX9E' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOXCC' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOX33' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOX86' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOX61' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOXD8' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOXF8' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOX69' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOX27' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOXF0' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOXD0' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOX46' or
    #        str("cbOX%0.2X" % cbCode) == 'cbOXB2'):
    #         return 0
    #     else:
    #         sys.exit()

    return func(memCntr)  # +4 cycles for fetching cb

#     switcher = {
#        0x11: cbOX11,
#        0x7C: cbOX7C,
#        0x37: cbOX37,
#        0x87: cbOX87,
#        0x38: cbOX38,
#        0x18: cbOX18,
#        0x19: cbOX19,
#        0x1A: cbOX1A,
#        0x1B: cbOX1B,
#        0x1C: cbOX1C,
#        0x1D: cbOX1D,
#        0x1F: cbOX1F
#     }
#    func = switcher.get(cbCode)
#
#     if callable(func):
#         return func(memCntr) + 4 # +4 cycles for fetching cb
#     else:
#         print('Unknown CB opcode:\t', hex(cbCode))
#         return 0xFFFFFF
###################################################


'''
    Processor codes
'''
thisdict = {}


def fetchOpCodeAnalysis(memCntr):

    memCntr.setSP(0)

    if(memCntr._register.PC < 0x150):
        memCntr._register.PC = 0x150
    elif(memCntr.memory[memCntr._register.PC] == 0x00):
        memCntr.incPC()
        return 0
    elif(memCntr._register.PC > 0x8000):
        print(thisdict)
        sys.exit()

    if str("OX%0.2X" % memCntr.memory[memCntr._register.PC]) in globals():
        func = globals()["OX%0.2X" % memCntr.memory[memCntr._register.PC]]

        print('PC: ' + format(memCntr.getPC(), '02X') + ' - ' + func.__name__)
        memCntr.oldPC = memCntr.getPC()
        memCntr.incPC()

        if (str("OX%0.2X" % memCntr.memory[memCntr.oldPC]) != 'OXF9'):
            func(memCntr)

        key = str("OX%0.2X" % memCntr.memory[memCntr._register.PC])

        if(thisdict.get(key, -1) == -1):
            thisdict.setdefault(key, 1)
        else:
            value = thisdict.pop(key)
            thisdict.setdefault(key, value + 1)

    else:
        print("OX%0.2X" % memCntr.memory[memCntr._register.PC])

        if(str("OX%0.2X" % memCntr.memory[memCntr._register.PC]) == 'OXCC' or
           str("OX%0.2X" % memCntr.memory[memCntr._register.PC]) == 'OXD4' or
           str("OX%0.2X" % memCntr.memory[memCntr._register.PC]) == 'OXD2' or
           str("OX%0.2X" % memCntr.memory[memCntr._register.PC]) == 'OXDC' or
           str("OX%0.2X" % memCntr.memory[memCntr._register.PC]) == 'OXC2'):
            memCntr.incPC()
            memCntr.incPC()
            memCntr.incPC()
        elif(str("OX%0.2X" % memCntr.memory[memCntr._register.PC]) == 'OXDE' or
             str("OX%0.2X" % memCntr.memory[memCntr._register.PC]) == 'OXF8' or
             str("OX%0.2X" % memCntr.memory[memCntr._register.PC]) == 'OXE8'):
            memCntr.incPC()
            memCntr.incPC()
        elif(str("OX%0.2X" % memCntr.memory[memCntr._register.PC]) == 'OXD8' or
             str("OX%0.2X" % memCntr.memory[memCntr._register.PC]) == 'OXD0' or
             str("OX%0.2X" % memCntr.memory[memCntr._register.PC]) == 'OX09' or
             str("OX%0.2X" % memCntr.memory[memCntr._register.PC]) == 'OX9E' or
             str("OX%0.2X" % memCntr.memory[memCntr._register.PC]) == 'OX3B' or
             str("OX%0.2X" % memCntr.memory[memCntr._register.PC]) == 'OX3F' or
             str("OX%0.2X" % memCntr.memory[memCntr._register.PC]) == 'OX37' or
             str("OX%0.2X" % memCntr.memory[memCntr._register.PC]) == 'OX8E' or
             str("OX%0.2X" % memCntr.memory[memCntr._register.PC]) == 'OX88' or
             str("OX%0.2X" % memCntr.memory[memCntr._register.PC]) == 'OX8C' or
             str("OX%0.2X" % memCntr.memory[memCntr._register.PC]) == 'OX98' or
             str("OX%0.2X" % memCntr.memory[memCntr._register.PC]) == 'OX9A' or
             str("OX%0.2X" % memCntr.memory[memCntr._register.PC]) == 'OX8A'):
            memCntr.incPC()
        else:
            print(str("OX%0.2X" % memCntr.memory[memCntr._register.PC]))
            print(thisdict)
            sys.exit()

    return 0


def fetchOpCode(memCntr):

    if(memCntr.halt):
        return 4
    #     if(opCode == ):
    #         start_time = time.perf_counter()
    # time.perf_counter() # start time of the loop
    func = globals()["OX%0.2X" % memCntr.memory[memCntr._register.PC]]
    # func = opCodeToFunction[memCntr.memory[memCntr._register.PC]]
#     memCntr.oldPC = memCntr.memory[memCntr._register.PC]

    # print("PC: " + "OX%0.2X" % memCntr._register.PC + ", OPCode: " + "OX%0.2X" % memCntr.memory[memCntr._register.PC] + " - " + str(memCntr.memory[memCntr._register.PC]) + " func: " + func.__name__)

    memCntr.oldPC = memCntr.getPC()
    memCntr.incPC()

    # if(memCntr.memory[memCntr._register.PC] == 0x00 and memCntr.memory[memCntr.oldPC] == 0x00):
    #     sys.exit()

    # memCntr._register.PC = memCntr._register.PC + 1

#     start_time = time.perf_counter()
    timeDuration = func(memCntr)
    #logState(memCntr, func.__name__)

    return timeDuration

#     end_time = time.perf_counter() #time.perf_counter()
#     executionTimeReal = end_time - start_time
#     executionTimeReal *= 1000.0 * 1000.0
#     executionTimeShall = result * 0.0000002386 * 1000 * 1000
#     if( executionTimeReal > executionTimeShall ):
#         print("Timing er qs: " + str(executionTimeReal) + "/" + str(executionTimeShall) + " OpCode: " + str("0X%0.2X" % memCntr.oldPC))
#
    # return result
#     if(opCode == 0x20):
#         end_time = time.perf_counter() #time.perf_counter()
#         executionTimeReal = end_time - start_time
#         print("0x20: " + str(executionTimeReal * 1000 * 1000 * 1000) + str(" ns"))


# opCodeToFunction = {
#     0: OX00,
#     1: OX01,
#     13: OX0D,
#     11: OX0B,
#     61: OX3D,
#     4: OX04,
#     5: OX05,
#     6: OX06,
#     12: OX0C,
#     14: OX0E,
#     17: OX11,
#     19: OX13,
#     23: OX17,
#     26: OX1A,
#     49: OX31,
#     50: OX32,
#     62: OX3E,
#     175: OXAF,
#     32: OX20,
#     33: OX21,
#     79: OX4F,
#     203: OXCB,
#     205: OXCD,
#     224: OXE0,
#     226: OXE2,
#     119: OX77,
#     123: OX7B,
#     193: OXC1,
#     197: OXC5,
#     34: OX22,
#     35: OX23,
#     201: OXC9,
#     254: OXFE,
#     234: OXEA,
#     40: OX28,
#     24: OX18,
#     46: OX2E,
#     103: OX67,
#     87: OX57,
#     30: OX1E,
#     29: OX1D,
#     240: OXF0,
#     36: OX24,
#     124: OX7C,
#     21: OX15,
#     22: OX16,
#     144: OX90,
#     190: OXBE,
#     125: OX7D,
#     120: OX78,
#     134: OX86,
#     195: OXC3,
#     128: OX80,
#     243: OXF3,
#     54: OX36,
#     42: OX2A,
#     177: OXB1,
#     251: OXFB,
#     47: OX2F,
#     230: OXE6,
#     71: OX47,
#     176: OXB0,
#     169: OXA9,
#     161: OXA1,
#     121: OX79,
#     239: OXEF,
#     135: OX87,
#     225: OXE1,
#     95: OX5F,
#     25: OX19,
#     94: OX5E,
#     86: OX56,
#     213: OXD5,
#     233: OXE9,
#     255: OXFF,
#     38: OX26,
#     3: OX03,
#     27: OX1B,
#     18: OX12,
#     28: OX1C,
#     41: OX29,
#     229: OXE5,
#     209: OXD1,
#     245: OXF5,
#     250: OXFA,
#     167: OXA7,
#     202: OXCA,
#     200: OXC8,
#     126: OX7E,
#     241: OXF1,
#     53: OX35,
#     44: OX2C,
#     192: OXC0,
#     2: OX02,
#     60: OX3C,
#     111: OX6F,
#     249: OXF9,
#     122: OX7A,
#     183: OXB7,
#     20: OX14,
#     52: OX34,
#     217: OXD9,
#     196: OXC4,
#     198: OXC6,
#     214: OXD6,
#     70: OX46,
#     45: OX2D,
#     78: OX4E,
#     174: OXAE,
#     31: OX1F,
#     48: OX30,
#     37: OX25,
#     114: OX72,
#     113: OX71,
#     112: OX70,
#     206: OXCE,
#     182: OXB6,
#     110: OX6E,
#     102: OX66,
#     118: OX76,
#     108: OX6C,
#     96: OX60,
#     238: OXEE,
#     127: OX7F,
#     107: OX6B,
#     130: OX82
# }
