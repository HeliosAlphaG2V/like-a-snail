#!python
#cython: language_level=3
from enumRegister import R8ID
import opcodes
minimum = 0xFF

def decX(memCntr, x):

    if( x & (1 << 4) == 0 ):
        memCntr._registerFlags.C = 0
    else:
        memCntr._registerFlags.C = 1   
    
    x -= 1
    
    # Overflow
    if(x == -1):
        x = minimum
        
    memCntr._registerFlags.N = 1

    if( x == 0 ):
        memCntr._registerFlags.Z = 1
    else:
        memCntr._registerFlags.Z = 0   

    return x
    opcodes.logAction(decX.__name__,
                      '-',
                      0,
                      0x01,
                      x,
                      memCntr.getR8(R8ID.F)
                      )


def decX16(memCntr, ID):

    x = memCntr.getR16FromR8(ID)
    xLog = x
    x -= 1

    # Overflow
    if(x == -1):
        x = 0xFFFF
        
    memCntr.setR16FromR8(ID, x)
 
    opcodes.logAction(decX16.__name__,
                      '-',
                      xLog,
                      0x01,
                      x,
                      memCntr.getR8(R8ID.F)
                      )
        
################### R16
def _0X0B(memCntr):
    decX16(memCntr, R8ID.B)
    return 8

def _0X1B(memCntr):
    decX16(memCntr, R8ID.D)
    return 8

def _0X2B(memCntr):
    decX16(memCntr, R8ID.H)
    return 8

def _0X3B(memCntr):
    sp = memCntr.getSP()
    sp -= 1
    memCntr.setSP(sp)
    return 8

def _0X35(memCntr):
    adressHL = memCntr.getR16FromR8(R8ID.H)
    
    value = memCntr.getMemValue( adressHL )
    logValue = value
    value -= 1
    
    if( value == -1 ):
        value = 0xFF
        memCntr.resetZero()
    elif( value == 0 ):
        memCntr.setZero()
        
    memCntr.setSubstract()
        
    memCntr.setMemValue( adressHL, value )
    
#     opcodes.logAction('DEC (HL)',
#                       '|',
#                       adressHL,
#                       logValue,
#                       memCntr.getMemValue( adressHL ),
#                       memCntr.getR8(R8ID.F)
#                       )
    return 12

################### R8
def _0X05(memCntr):
    memCntr._register.B = decX(memCntr, memCntr._register.B)
    return 4

def _0X15(memCntr):
    memCntr._register.D = decX(memCntr, memCntr._register.D)  
    return 4

def _0X0D(memCntr):
    memCntr._register.C = decX(memCntr, memCntr._register.C)
    return 4

def _0X1D(memCntr):
    memCntr._register.E = decX(memCntr, memCntr._register.E)
    return 4

def _0X25(memCntr):
    memCntr._register.H = decX(memCntr, memCntr._register.H)
    return 4

def _0X2D(memCntr):
    memCntr._register.L = decX(memCntr, memCntr._register.L)
    return 4

def _0X3D(memCntr):
    memCntr._register.A = decX(memCntr, memCntr._register.A)
    return 4