#!python
#cython: language_level=3
import opcodes
import sys

from struct import pack, unpack
from enumRegister import R8ID

def rstPush(memCntr, rst):
    bArray = memCntr.getTwoR8FromR16(memCntr.getPC())
    memCntr.push(bArray[0])
    memCntr.push(bArray[1])   
    
#    logPC = memCntr.getPC()
    memCntr.setPC(rst)
       
#     opcodes.logAction('rstPush',
#                       '<',
#                       logPC,
#                       rst,
#                       memCntr.getPC(),
#                       memCntr.getR8(R8ID.F))
                
# Jump if Z-Flag 0 / Optimized for high performance (more optimization possible)
def _0X20(memCntr):

    if( memCntr._registerFlags.Z == 0 ):
        uJmpValue = memCntr.memory[memCntr._register.PC]
         
        if( uJmpValue > 127 ):
            uJmpValue = uJmpValue - 256

        memCntr._register.PC = memCntr._register.PC + uJmpValue + 1
        return 12
    else:
        memCntr._register.PC += 1
        return 8
    
#     opcodes.logAction('JPz0 20',
#                       '+',
#                       pcLog,
#                       signedJpValue,
#                       memCntr.getPC(),
#                       memCntr.getR8(R8ID.F))    
    

# Jump
def _0X18(memCntr):
    
    unsignedJpValue = memCntr.getNextParam()
    pc = memCntr.getPC()
    pcLog = pc
    signedJpValue = unpack('b', pack('B', unsignedJpValue))[0]
    pc += signedJpValue
    memCntr.setPC(pc)

#     opcodes.logAction('JP 18',
#                       '+',
#                       pcLog,
#                       signedJpValue,
#                       memCntr.getPC(),
#                       memCntr.getR8(R8ID.F))  
    
    return 12
        
# Jump to d16
def _0XC3(memCntr):

    pcLog = memCntr.getPC()
    param1 = memCntr.getNextParam()
    param2 = memCntr.getNextParam()
    
    memCntr.setPC(memCntr.getAsR16(param2, param1))
    
    opcodes.logAction('JPd16 C3',
                      '<',
                      pcLog,
                      memCntr.getAsR16(param2, param1),
                      memCntr.getPC(),
                      memCntr.getR8(R8ID.F))
    return 16

# Jump Zero to d16
def _0XCA(memCntr):
    ret = 12
    
    pcLog = memCntr.getPC()
    param1 = memCntr.getNextParam()
    param2 = memCntr.getNextParam()
     
    if (memCntr.getZero() == 1): # Jump if z = 1   
        memCntr.setPC(memCntr.getAsR16(param2, param1))
        ret = 16
    
    opcodes.logAction('JPZ d16 CA',
                      '<',
                      pcLog,
                      memCntr.getAsR16(param2, param1),
                      memCntr.getPC(),
                      memCntr.getR8(R8ID.F))
    return ret

# Jump Carry to d16
def _0XDA(memCntr):
    ret = 12
    
    pcLog = memCntr.getPC()
    param1 = memCntr.getNextParam()
    param2 = memCntr.getNextParam()
     
    if (memCntr.getCarry() == 1): # Jump if z = 1   
        memCntr.setPC(memCntr.getAsR16(param2, param1))
        ret = 16
    
    opcodes.logAction('JPC d16 CA',
                      '<',
                      pcLog,
                      memCntr.getAsR16(param2, param1),
                      memCntr.getPC(),
                      memCntr.getR8(R8ID.F))
    return ret
    
# Jump if NC
def _0X30(memCntr):
    ret = 8
    unsignedJpValue = memCntr.getNextParam()
    pc = memCntr.getPC()
    pcLog = pc
    signedJpValue = 0
    
    if (memCntr.getCarry() == 0):   
        signedJpValue = unpack('b', pack('B', unsignedJpValue))[0]
        pc += signedJpValue
        memCntr.setPC(pc)
        return 12
        
    opcodes.logAction('JP NC, r8',
                      '+',
                      pcLog,
                      signedJpValue,
                      memCntr.getPC(),
                      memCntr.getR8(R8ID.F))  
    return ret 
          
# Jump if Zero
def _0X28(memCntr):
    
    ret = 8
    unsignedJpValue = memCntr.getNextParam()
    pc = memCntr.getPC()
    pcLog = pc
    signedJpValue = 0
    
    if (memCntr.getZero() == 1): # Jump if z = 1   
        signedJpValue = unpack('b', pack('B', unsignedJpValue))[0]
        pc += signedJpValue
        memCntr.setPC(pc)
        ret = 12
        
    opcodes.logAction('JPz 28',
                      '+',
                      pcLog,
                      signedJpValue,
                      memCntr.getPC(),
                      memCntr.getR8(R8ID.F))  
    return ret

# Jump if Carry
def _0X38(memCntr):
    
    ret = 8
    unsignedJpValue = memCntr.getNextParam()
    pc = memCntr.getPC()
    pcLog = pc
    signedJpValue = 0
    
    if (memCntr.getCarry() == 1): # Jump if c = 1   
        signedJpValue = unpack('b', pack('B', unsignedJpValue))[0]
        pc += signedJpValue
        memCntr.setPC(pc)
        ret = 12
        
    opcodes.logAction('JPc 38',
                      '+',
                      pcLog,
                      signedJpValue,
                      memCntr.getPC(),
                      memCntr.getR8(R8ID.F))  
    return ret

################### Call 0xNNNN
def _0XCD(memCntr):
    param1 = memCntr.getNextParam()
    param2 = memCntr.getNextParam()

    # Callback address to stack
    bArray = memCntr.getTwoR8FromR16(memCntr.getPC())
    memCntr.push(bArray[0])
    memCntr.push(bArray[1])

    pcLog = memCntr.getPC()
    
    # Call             
    memCntr.setPC(memCntr.getAsR16(param2, param1))
    
    opcodes.logAction('CALL',
                      '<',
                      pcLog,
                      memCntr.getAsR16(param2, param1),
                      memCntr.getPC(),
                      memCntr.getR8(R8ID.F))
    
    print(str(param2))
    print(str(param1))
    print(str(pcLog))
    
    return 24

# CALL NZ, 0xNNNN 
def _0XC4(memCntr):
    ret = 12
    param1 = memCntr.getNextParam()
    param2 = memCntr.getNextParam()

    # Callback address to stack
    bArray = memCntr.getTwoR8FromR16(memCntr.getPC())
    memCntr.push(bArray[0])
    memCntr.push(bArray[1])

    pcLog = memCntr.getPC()
    
    # Call
    if (memCntr.getZero() == 0):              
        memCntr.setPC(memCntr.getAsR16(param2, param1))
        ret = 24

    opcodes.logAction('CALL NZ',
                      '<',
                      pcLog,
                      memCntr.getAsR16(param2, param1),
                      memCntr.getPC(),
                      memCntr.getR8(R8ID.F))
    
    return ret
    
################### RET
def _0XC9(memCntr):
    param1 = memCntr.pop()
    param2 = memCntr.pop()
    
    pcLog = memCntr.getPC()
    
    memCntr.setPC(memCntr.getAsR16(param2, param1))
    
    opcodes.logAction('RET C9',
                      '<',
                      pcLog,
                      memCntr.getAsR16(param2, param1),
                      memCntr.getPC(),
                      memCntr.getR8(R8ID.F))
    return 16

# RETI
def _0XD9(memCntr):
    param1 = memCntr.pop()
    param2 = memCntr.pop()

    memCntr.setPC(memCntr.getAsR16(param1, param2))
    
    # Enable interrupt
    memCntr.bInterruptOn = True
    memCntr.setMemValue(0xFFFF, 0xFF)
    
    opcodes.logAction('RETI',
                      '|',
                      memCntr.getSP(),
                      memCntr.getAsR16(param1, param2),
                      memCntr.getPC(),
                      memCntr.getR8(R8ID.F))    
    return 16
    
# RET NZ
def _0XC0(memCntr):
    
    ret = 8
    
    param1 = memCntr.pop()
    param2 = memCntr.pop()
    
    #pcLog = memCntr.getPC()
    
    if (memCntr.getZero() == 0): 
        memCntr.setPC(memCntr.getAsR16(param2, param1))
        ret = 20
    
#     opcodes.logAction('RET NZ C8',
#                       '<',
#                       pcLog,
#                       memCntr.getAsR16(param2, param1),
#                       memCntr.getPC(),
#                       memCntr.getR8(R8ID.F))
    
    return ret
    
# RET Z
def _0XC8(memCntr):
    
    ret = 8
    param1 = memCntr.pop()
    param2 = memCntr.pop()
    
    pcLog = memCntr.getPC()
    
    if (memCntr.getZero() == 1): # Jump if z = 1   
        memCntr.setPC(memCntr.getAsR16(param2, param1))
        ret = 20
        
    opcodes.logAction('RET Z C8',
                      '<',
                      pcLog,
                      memCntr.getAsR16(param2, param1),
                      memCntr.getPC(),
                      memCntr.getR8(R8ID.F))
    
    return ret
    
################### JP
def _0XE9(memCntr):
    pcLog = memCntr.getPC()
    memCntr.setPC(memCntr.getR16FromR8(R8ID.H))
    
    opcodes.logAction('JPhl',
                      '<',
                      pcLog,
                      memCntr.getR16FromR8(R8ID.H),
                      memCntr.getPC(),
                      memCntr.getR8(R8ID.F))
    
    return 4
   
################### RST
def _0XCF(memCntr):
    rstPush(memCntr, 0x0008)
    return 16

def _0XDF(memCntr):
    rstPush(memCntr, 0x0018)
    return 16
    
def _0XEF(memCntr):
    rstPush(memCntr, 0x0028)
    return 16
    
def _0XFF(memCntr):
    rstPush(memCntr, 0x0038)
    return 16

def _0XC7(memCntr):
    rstPush(memCntr, 0x0000)
    return 16
    
def _0XD7(memCntr):
    rstPush(memCntr, 0x0010)
    return 16

def _0XE7(memCntr):
    rstPush(memCntr, 0x0020)
    return 16
    
def _0XF7(memCntr):
    rstPush(memCntr, 0x0030)         
    return 16