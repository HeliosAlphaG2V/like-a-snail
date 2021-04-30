#!python
# cython: language_level=3
from enumRegister import R8ID
import opcodes

# 7th --- 0th
# 0 0 0 0  0 0 0 0
# variable << Bitstelle
# (1 << X) Die 1 um X verschieben

# C 8 7 6 5 4 3 2 1
# 0 0 0 0 0 0 0 0 0
# Rotate left through carry
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
        
    opcodes.logAction('RR ' + str(Id),
              'to MSB',
              memCntr.getCarry(),
              nReg,
              memCntr.getR8(Id),
              memCntr.getR8(R8ID.F))


def rrX(memCntr, Id):
    
#     logCarryFlag = memCntr.getCarry()   
    nReg = memCntr.getR8(Id)
    
    # Test 0th Bit and put it in Carry if 1
    if(nReg & (1 << 0)):
        memCntr.setCarry()
        nReg &= 0x01
    else:
        memCntr.resetCarry()
        
    nReg = nReg // 2  # Shift to Right   
    
#     if(logCarryFlag == 1):
#         nReg = nReg | 0x80  # MSB Bit = 1
    
    memCntr.setR8(Id, nReg)
    memCntr.resetSubstract()
    memCntr.resetHalfCarry()
    
    if(nReg == 0):
        memCntr.setZero()
    else:
        memCntr.resetZero()
        
    opcodes.logAction('RR ' + str(Id),
              'to MSB',
              memCntr.getCarry(),
              nReg,
              memCntr.getR8(Id),
              memCntr.getR8(R8ID.F))

def bitX(memCntr, Id, bit, indirect = False):
    
    if indirect:
        nReg = memCntr.getMemValue(memCntr.getR16FromR8(Id))
    else:    
        nReg = memCntr.getR8(Id)
    
    if not (nReg & (1 << bit)):
        memCntr.setZero()
        
    memCntr.resetSubstract()
    memCntr.setHalfCarry()
   
    opcodes.logAction('BIT ' + str(Id),
              '>&<',
              memCntr.getCarry(),
              nReg,
              0x01,
              memCntr.getR8(R8ID.F))
    
def setX(memCntr, Id, bit, indirect = False):
    
    if indirect:
        before = memCntr.getMemValue(memCntr.getR16FromR8(Id))
        nReg = memCntr.getMemValue(memCntr.getR16FromR8(Id)) | (1 << bit)
        memCntr.setMemValue(memCntr.getR16FromR8(Id), nReg)
    else:    
        before = memCntr.getR8(Id)
        nReg = memCntr.getR8(Id) | (1 << bit)
        memCntr.setR8(Id, nReg)

    opcodes.logAction('SET bit ' + str(bit),
              '>1<',
              before,
              nReg,
              memCntr.getMemValue(memCntr.getR16FromR8(Id)),
              memCntr.getR8(R8ID.F))

################### SET X, n
def cb_0XDE(memCntr):
    setX(memCntr, R8ID.H, 3, True)
    return 8

def cb_0XEE(memCntr):
    setX(memCntr, R8ID.H, 5, True)
    return 8

################### BIT X, n
def cb_0X41(memCntr):
    bitX(memCntr, R8ID.C, 0)
    return 8

def cb_0X7E(memCntr):
    bitX(memCntr, R8ID.H, 7, True)
    return 8

################### RL X
def cb_0X14(memCntr):
    rrX(memCntr, R8ID.H)
    return 8

################### RR X
def cb_0X18(memCntr):
    rrX(memCntr, R8ID.B)
    return 8


def cb_0X19(memCntr):
    rrX(memCntr, R8ID.C)
    return 8

    
def cb_0X1A(memCntr):
    rrX(memCntr, R8ID.D)
    return 8


def cb_0X1B(memCntr):
    rrX(memCntr, R8ID.E)
    return 8

    
def cb_0X1C(memCntr):
    rrX(memCntr, R8ID.H)
    return 8

    
def cb_0X1D(memCntr):
    rrX(memCntr, R8ID.L)
    return 8


def cb_0X1F(memCntr):
    rrX(memCntr, R8ID.A)
    return 8


################### RR (C) A
def _0X1F(memCntr):
    rrX(memCntr, R8ID.A)
    return 4

################### RL (C) A
def _0X07(memCntr):
    rlX(memCntr, R8ID.A)
    return 4