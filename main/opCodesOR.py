import opcodes
from enumRegister import R8ID

def orrX(memCntr, x):
    a = memCntr.getR8(R8ID.A)
    aLog = a
    a = a | memCntr.getReduced(x)
    
    memCntr.setR8(R8ID.A, a)
    
    memCntr.resetSubstract()
    memCntr.resetHalfCarry()
    memCntr.resetCarry()
    
    if( a == 0 ):
        memCntr.setZero()
    else:
        memCntr.resetZero()
            
    opcodes.logAction(orrX.__name__, '|',aLog, x, memCntr.getR8(R8ID.A), memCntr.getR8(R8ID.F))    
      
def _0XB0(memCntr):
    orrX(memCntr, memCntr.getR8(R8ID.B))
    return 4
    
def _0XB1(memCntr):
    orrX(memCntr, memCntr.getR8(R8ID.C))
    return 4
        
def _0XB2(memCntr):
    orrX(memCntr, memCntr.getR8(R8ID.D))
    return 4
        
def _0XB3(memCntr):
    orrX(memCntr, memCntr.getR8(R8ID.E))
    return 4
    
def _0XB4(memCntr):
    orrX(memCntr, memCntr.getR8(R8ID.H))
    return 4
    
def _0XB5(memCntr):
    orrX(memCntr, memCntr.getR8(R8ID.L))
    return 4
    
def _0XB6(memCntr):
    orrX(memCntr, memCntr.getR16FromR8(R8ID.H))
    return 8
    
def _0XB7(memCntr):
    orrX(memCntr, memCntr.getR8(R8ID.A))
    return 4
    
def _0XF6(memCntr):
    orrX(memCntr, memCntr.getNextParam())
    return 8