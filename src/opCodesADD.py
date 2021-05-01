#!python
#cython: language_level=3
import opcodes
from enumRegister import R8ID

def addX(memCntr, x, carry = False):
    a = memCntr.getR8(R8ID.A)
    aLog = a
    
    if( carry ):
        a += x + 1
        memCntr.resetCarry()
    else:
        a += x

    # Put 9th Bit into Carryflag
    if( a & (1 << 8) ):
        memCntr.setCarry
        a = a & ~(1 << 8)
        
    memCntr.setR8(R8ID.A, a)
    
    # ToDo: Carry from 3th Bit
    
    memCntr.resetSubstract()
    
    if( a == 0 ):
        memCntr.setZero()
    else:
        memCntr.resetZero()  
    
    opcodes.logAction(addX.__name__,
                      '+',
                      aLog,
                      x, 
                      memCntr.getR8(R8ID.A), 
                      memCntr.getR8(R8ID.F)
                      )

def addXR16(memCntr, x, value, ID):
    
    xLog = x
    x += value
    
    # Remove possible overflow
    if(x > 65535):
        x &= (x - (x & (1 << 16)))
    
    memCntr.resetSubstract()
    
    
    bArray = memCntr.getTwoR8FromR16(x)
    
    memCntr.setR8(ID, bArray[0])
    memCntr.setR8(ID + 1, bArray[1])

    opcodes.logAction(addXR16.__name__,
                      '+',
                      xLog, 
                      value, 
                      memCntr.getR16FromR8(ID), 
                      memCntr.getR8(R8ID.F))
    
################### R16
def _0X19(memCntr):
    de = memCntr.getR16FromR8(R8ID.D)
    hl = memCntr.getR16FromR8(R8ID.H)
    addXR16(memCntr, hl, de, R8ID.H)
    return 8

def _0X29(memCntr):
    hl = memCntr.getR16FromR8(R8ID.H)
    addXR16(memCntr, hl, hl, R8ID.H)
    return 8

def _0X39(memCntr):
    sp = memCntr.getSP()
    hl = memCntr.getR16FromR8(R8ID.H)
    addXR16(memCntr, hl, sp, R8ID.H)
    return 8
   
################### R8     
def _0X80(memCntr):
    addX(memCntr, memCntr.getR8(R8ID.B))
    return 4
    
def _0X81(memCntr):
    addX(memCntr, memCntr.getR8(R8ID.C))
    return 4

def _0X82(memCntr):
    addX(memCntr, memCntr.getR8(R8ID.D))
    return 4
    
def _0X83(memCntr):
    addX(memCntr, memCntr.getR8(R8ID.E))
    return 4
    
def _0X84(memCntr):
    addX(memCntr, memCntr.getR8(R8ID.H))
    return 4
    
def _0X85(memCntr):
    addX(memCntr, memCntr.getR8(R8ID.L))
    return 4

def _0X86(memCntr):
    addX(memCntr, memCntr.memory[memCntr.getR16FromR8(R8ID.H)])
    return 4

def _0X87(memCntr):
    addX(memCntr, memCntr.getR8(R8ID.A))
    return 4

def _0XC6(memCntr):
    addX(memCntr, memCntr.getNextParam())
    return 8

################### ADC
def _0XCE(memCntr):
    addX(memCntr, memCntr.getR8(R8ID.A), memCntr.getCarry())
    return 8

def _0X89(memCntr):
    addX(memCntr, memCntr.getR8(R8ID.C), memCntr.getCarry())
    return 4

def _0X8B(memCntr):
    addX(memCntr, memCntr.getR8(R8ID.E), memCntr.getCarry())
    return 4

def _0X8D(memCntr):
    addX(memCntr, memCntr.getR8(R8ID.L), memCntr.getCarry())
    return 4

def _0X8F(memCntr):
    addX(memCntr, memCntr.getR8(R8ID.A), memCntr.getCarry())
    return 4