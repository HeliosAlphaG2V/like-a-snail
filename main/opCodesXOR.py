#!python
#cython: language_level=3
from enumRegister import R8ID

def xorX(memCntr, x):
    #aLog = memCntr.getR8(R8ID.A)
    a = memCntr.getReduced(x) ^ memCntr.getR8(R8ID.A)

    memCntr.setR8(R8ID.A, a) 

    memCntr.resetHalfCarry()
    memCntr.resetSubstract()
    memCntr.resetCarry()
    
    if (a == 0):
        memCntr.setZero()
    else:
        memCntr.resetZero()
              
#     opcodes.logAction(xorX.__name__,
#                       '*',
#                       aLog,
#                       x,
#                       memCntr.getR8(R8ID.A),
#                       memCntr.getR8(R8ID.F)
#                       )    
        
def _0XA8(memCntr):
    xorX(memCntr, memCntr.getR8(R8ID.B))
    return 4
    
def _0XA9(memCntr):
    xorX(memCntr, memCntr.getR8(R8ID.C))
    return 4
    
def _0XAA(memCntr):
    xorX(memCntr, memCntr.getR8(R8ID.D))
    return 4
   
def _0XAB(memCntr):
    xorX(memCntr, memCntr.getR8(R8ID.E))
    return 4
    
def _0XAC(memCntr):
    xorX(memCntr, memCntr.getR8(R8ID.H))
    return 4
       
def _0XAD(memCntr):
    xorX(memCntr, memCntr.getR8(R8ID.L))
    return 4
    
def _0XAE(memCntr):
    xorX(memCntr, memCntr.getR16FromR8(R8ID.H))
    return 8

def _0XAF(memCntr):
    xorX(memCntr, memCntr.getR8(R8ID.A))
    return 4

def _0XEE(memCntr):
    xorX(memCntr, memCntr.getNextParam())
    return 8