import opcodes
from enumRegister import R8ID;

def logPushPop(strType, ID, memCntr):
    opcodes.logAction(strType,
                      '=',
                      memCntr.getAsR16(memCntr.getR8(ID), memCntr.getR8(ID+1)),
                      memCntr.getAsR16(memCntr.getR8(ID), memCntr.getR8(ID+1)),
                      memCntr.getAsR16(memCntr.getR8(ID), memCntr.getR8(ID+1)),
                      memCntr.getR8(R8ID.F)) 
    
def _0XC1(memCntr):
    memCntr.setR8(R8ID.C, memCntr.pop())
    memCntr.setR8(R8ID.B, memCntr.pop())
    
    logPushPop('POP BC', R8ID.B, memCntr)
    return 12

def _0XD1(memCntr):
    memCntr.setR8(R8ID.E, memCntr.pop())
    memCntr.setR8(R8ID.D, memCntr.pop())
    
    logPushPop('POP DE', R8ID.D, memCntr)
    return 12
        
def _0XE1(memCntr):
    memCntr.setR8(R8ID.L, memCntr.pop())
    memCntr.setR8(R8ID.H, memCntr.pop())

    logPushPop('POP HL', R8ID.H, memCntr)
    return 12

def _0XF1(memCntr):
    memCntr.setR8(R8ID.F, memCntr.pop())
    memCntr.setR8(R8ID.A, memCntr.pop())
    
    logPushPop('POP AF', R8ID.A, memCntr)
    return 12
          
def _0XC5(memCntr):
    memCntr.push(memCntr.getR8(R8ID.B))
    memCntr.push(memCntr.getR8(R8ID.C))
    
    logPushPop('PUSH BC', R8ID.B, memCntr)
    return 12
    
def _0XD5(memCntr):
    memCntr.push(memCntr.getR8(R8ID.D))
    memCntr.push(memCntr.getR8(R8ID.E))
    
    logPushPop('PUSH DE', R8ID.D, memCntr)
    return 12

def _0XE5(memCntr):
    memCntr.push(memCntr.getR8(R8ID.H))
    memCntr.push(memCntr.getR8(R8ID.L))

    logPushPop('PUSH HL', R8ID.H, memCntr)
    return 12

def _0XF5(memCntr):
    memCntr.push(memCntr.getR8(R8ID.A))
    memCntr.push(memCntr.getR8(R8ID.F))
    
    logPushPop('PUSH AF', R8ID.A, memCntr)
    return 12