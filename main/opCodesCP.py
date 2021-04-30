#!python
#cython: language_level=3
from enumRegister import R8ID
import opcodes

def cmpX(memCntr, x):

    # ToDo FLAG.H borrow...
    if( memCntr._register.A < x ):
        memCntr._registerFlags.C = 1
    else:
        memCntr._registerFlags.C = 0
    
    if( memCntr._register.A - x == 0 ):
        memCntr._registerFlags.Z = 1
    else:
        memCntr._registerFlags.Z = 0

    memCntr._registerFlags.N = 1
    opcodes.logAction(cmpX.__name__, '-', 0, x, 0, memCntr.getR8(R8ID.F))

def _0XB8(memCntr):
    cmpX(memCntr, memCntr.getR8(R8ID.B))
    return 4

def _0XB9(memCntr):
    cmpX(memCntr, memCntr.getR8(R8ID.C))
    return 4
    
def _0XBA(memCntr):
    cmpX(memCntr, memCntr.getR8(R8ID.D))
    return 4
    
def _0XBB(memCntr):
    cmpX(memCntr, memCntr.getR8(R8ID.E))
    return 4
   
def _0XBC(memCntr):
    cmpX(memCntr, memCntr.getR8(R8ID.H))
    return 4
   
def _0XBD(memCntr):
    cmpX(memCntr, memCntr.getR8(R8ID.L))
    return 4
   
def _0XBE(memCntr):
    cmpX(memCntr, memCntr.memory[memCntr.getR16FromR8(R8ID.H)])
    return 8
    
def _0XBF(memCntr):
    cmpX(memCntr, memCntr.getR8(R8ID.A))
    return 4

def _0XFE(memCntr):

    # ToDo FLAG.H borrow...
    if( memCntr._register.A < memCntr.memory[memCntr._register.PC] ):
        memCntr._registerFlags.C = 1
    else:
        memCntr._registerFlags.C = 0
    
    if( memCntr._register.A - memCntr.memory[memCntr._register.PC] == 0 ):
        memCntr._registerFlags.Z = 1
    else:
        memCntr._registerFlags.Z = 0

    memCntr._registerFlags.N = 1
    memCntr._register.PC = memCntr._register.PC + 1
    return 8