from .log import logAction
from .enumRegister import R8ID

def andX(memCntr, x):
    a = memCntr.getR8(R8ID.A)
    aLog = a
    a = x & a
    
    memCntr.setR8(R8ID.A, a)      
    
    memCntr.setHalfCarry()
    memCntr.resetSubstract()
    memCntr.resetCarry()
    
    if( a == 0 ):
        memCntr.setZero()
    else:
        memCntr.resetZero() 
    
    logAction(andX.__name__, '&',aLog, x, memCntr.getR8(R8ID.A), memCntr.getR8(R8ID.F))       
    
def OXA0(memCntr):
    andX(memCntr, memCntr.getR8(R8ID.B))  
    return 4

def OXA1(memCntr):
    andX(memCntr, memCntr.getR8(R8ID.C))  
    return 4

def OXA2(memCntr):
    andX(memCntr, memCntr.getR8(R8ID.D))  
    return 4

def OXA3(memCntr):
    andX(memCntr, memCntr.getR8(R8ID.E))  
    return 4

def OXA4(memCntr):
    andX(memCntr, memCntr.getR8(R8ID.H))  
    return 4

def OXA5(memCntr):
    andX(memCntr, memCntr.getR8(R8ID.L))  
    return 4  

def OXA6(memCntr):
    andX(memCntr, memCntr.getHLValue())
    return 8

def OXA7(memCntr):
    andX(memCntr, memCntr.getR8(R8ID.A))  
    return 4

def OXE6(memCntr):
    andX(memCntr, memCntr.getNextParam())  
    return 8