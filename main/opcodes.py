#!python
#cython: language_level=3
import logging
import os
#import line_profiler
import time
from struct import pack, unpack
from enumRegister import R8ID

# Remove memoryController
import memoryController

from opCodesSpecial import  _0X00, _0X10, _0X76, _0XF3, _0XFB
from opCodesINC import      _0X03, _0X13, _0X23, _0X2C, _0X33, _0X34, _0X3C, _0X04, _0X14, _0X24, _0X0C, _0X1C
from opCodesDEC import      _0X05, _0X15, _0X0D, _0X1D, _0X25, _0X2B, _0X2D, _0X35, _0X3D, _0X0B, _0X1B
from opCodesADD import      _0X80, _0X81, _0X82, _0X83, _0X84, _0X85, _0X86, _0X87, _0X89, _0X8B, _0X8D, _0X8F, _0XC6, _0X19, _0X29, _0XCE, _0X39
from opCodesSUB import      _0X90, _0X91, _0X92, _0X93, _0X94, _0X95, _0X96, _0X97, _0XD6, _0X99, _0X9B, _0X9D, _0X9F, _0X9C 
from opCodesAND import      _0XA0, _0XA1, _0XA2, _0XA3, _0XA4, _0XA5, _0XA6, _0XA7, _0XE6
from opCodesXOR import      _0XA8, _0XA9, _0XAA, _0XAB, _0XAC, _0XAD, _0XAE, _0XAF, _0XEE
from opCodesOR import       _0XB0, _0XB1, _0XB2, _0XB3, _0XB4, _0XB5, _0XB6, _0XB7, _0XF6 
from opCodesCP import       _0XB8, _0XB9, _0XBA, _0XBB, _0XBC, _0XBD, _0XBE, _0XBF, _0XFE
from opCodesJUMP import     _0X18, _0X20, _0X28, _0X30, _0X38, _0XC0, _0XC3, _0XC4, _0XC7, _0XC8, _0XC9, _0XCA, _0XDA,_0XCD, _0XCF, _0XD7, _0XD9, _0XDF, _0XE7, _0XE9, _0XEF, _0XF7, _0XFF
from opCodesPushPop import  _0XC1, _0XD1, _0XE1, _0XF1, _0XC5, _0XD5, _0XE5, _0XF5
from opCodesRotate import   _0X07, _0X1F, cb_0X18, cb_0X19, cb_0X1A, cb_0X1B, cb_0X1C, cb_0X1D, cb_0X1F, cb_0X14, cb_0X41, cb_0XDE, cb_0XEE, cb_0X7E

#lp = line_profiler.LineProfiler()

#FORMAT = '%(funcName)s %(message)s %(filename=gb.log)s'
#logging.basicConfig(format=FORMAT)
#'%(funcName)s, \t\t\t%(message)s'
logPath = os.path.join(os.getcwd()+'\\Resource\\' , 'gb.log')
logging.basicConfig(level=logging.CRITICAL, #logging.DEBUG
                    format='%(message)s',
                    filename=logPath,
                    filemode='w')
logger = logging.getLogger()

def logAction(strFName, strAction, aLog, x, result, flags):
    #return
    strPC = '%s: '
    stroLXogTab = '%s\t\t'
    stroLXog = '%s %s %s = %s'
    stroLXogFlag = '\tF: %s'
    
    if( len(strFName) > 5 ):
        stroLXogTab = '%s\t'
    
    '04X' '08b'
    memCntr = memoryController.MemCntr.getInstance()
    
    logger = logging.getLogger() 
    logger.info(strPC + stroLXogTab + stroLXog + stroLXogFlag,
                format(memCntr.getPCBefore(), '04X'), 
                strFName,
                format(aLog, '04X'), 
                strAction,
                format(x, '04X'), 
                format(result, '04X'), 
                format(flags, '08b')
                )
    
## Helper functions
def roLX(memCntr, ID):
    x = memCntr.getR8(ID)
    xLog = x
    x *= 2
    
    # Put Carryflag into first bit
    if( memCntr.getCarry() == 1 ):
        x = x | (1 << 0)
        memCntr.resetCarry()  
    
    # Put 9th Bit into Carryflag
    if( x & (1 << 8) == 256 ):
        memCntr.setCarry() 
        x = x & ~(1 << 8)
    
    memCntr.setR8(ID, x)
    
    if( x == 0 ):
        memCntr.setZero()
    else:
        memCntr.resetZero()  
           
    memCntr.resetHalfCarry()
    memCntr.resetSubstract()
    
    logAction(roLX.__name__,
              '{',
              xLog,
              x,
              memCntr.getR8(ID),
              memCntr.getR8(R8ID.F))  


##################### NOP
def _0XD3(memCntr):
    return 0

def _0XE4(memCntr):
    return 0

def _0XE3(memCntr):
    return 0

def _0XF4(memCntr):
    return 0

def _0XFC(memCntr):
    return 0
''' 
### Address calculation opcodes
''' 
# LD (a16), SP
def _0X08(memCntr):     
    para1 = memCntr.getNextParam()
    para2 = memCntr.getNextParam()

    adr = memCntr.getAsR16(para2, para1)
    
    bArray = memCntr.getTwoR8FromR16(memCntr.getSP())

    memCntr.setMemValue(adr, bArray[1]) 
    memCntr.setMemValue(adr + 1, bArray[0]) 

    return 20
     
# LD SP, HL
def _0XF9(memCntr):    
    hl = memCntr.getAsR16(memCntr.getR8(R8ID.H), memCntr.getR8(R8ID.L))
    memCntr.setSP(hl)

    logAction('SP, HL',
          '<>',
          0,
          hl,
          memCntr.getSP(),
          memCntr.getR8(R8ID.F))
    return 8
    
# LD (BC), A
def _0X02(memCntr):
    bc = memCntr.getR16FromR8(R8ID.B)
    memCntr.setMemValue(bc, memCntr.getR8(R8ID.A))
    return 8

# LD A, (BC)
def _0X0A(memCntr):
    bc = memCntr.getR16FromR8(R8ID.B)
    memValue = memCntr.getMemValue(bc)
    memCntr.setR8(R8ID.A, memValue)
    return 8
    
# LD (DE), A
def _0X12(memCntr):
    de = memCntr.getR16FromR8(R8ID.D)
    memCntr.setMemValue(de, memCntr.getR8(R8ID.A))
    return 8
    
# LD A, (DE)
def _0X1A(memCntr):
    de = memCntr.getR16FromR8(R8ID.D)
    memValue = memCntr.getMemValue(de)
    memCntr.setR8(R8ID.A, memValue)
    return 8
        
# LD (HL+), A
def _0X22(memCntr):
    hl = memCntr.getR16FromR8(R8ID.H)
    memCntr.setMemValue(hl, memCntr.getR8(R8ID.A))
    hl += 1
    memCntr.setR16FromR8(R8ID.H, hl)
    return 8
    
# LD (HL-), A    
def _0X32(memCntr):
    hl = memCntr.getR16FromR8(R8ID.H)
    memCntr.setMemValue(hl, memCntr.getR8(R8ID.A))
    hl -= 1
    memCntr.setR16FromR8(R8ID.H, hl)
   
    logAction(_0X32.__name__,
          '|',
          hl,
          memCntr.getR8(R8ID.A),
          memCntr.getMemValue(hl + 1),
          memCntr.getR8(R8ID.F))
    
    return 8

# LD A, (HL+)
def _0X2A(memCntr):
    hl = memCntr.getR16FromR8(R8ID.H)

    memValue = memCntr.getMemValue(hl)
    memCntr.setR8(R8ID.A, memValue)
    
    hl += 1
    memCntr.setR16FromR8(R8ID.H, hl) 
    return 8

# LD A, (HL-)
def _0X3A(memCntr):
    hl = memCntr.getR16FromR8(R8ID.H)

    memValue = memCntr.getMemValue(hl)
    memCntr.setR8(R8ID.A, memValue)
    
    hl -= 1
    memCntr.setR16FromR8(R8ID.H, hl) 
    return 8
          
################### LD (HL), X
def LDHLx(memCntr, x):
    hl = memCntr.getR16FromR8(R8ID.H)
    xLog = memCntr.getMemValue(hl)
    memCntr.setMemValue(hl, x)   
    
    logAction(LDxHL.__name__,
      '=',
      xLog,
      x,
      memCntr.getMemValue(hl),
      memCntr.getR8(R8ID.F)
      )   
    
def _0X36(memCntr):
    LDHLx(memCntr, memCntr.getNextParam())
    return 12

def _0X70(memCntr):
    LDHLx(memCntr, memCntr.getR8(R8ID.B))
    return 8

def _0X71(memCntr):
    LDHLx(memCntr, memCntr.getR8(R8ID.C))
    return 8
    
def _0X72(memCntr):
    LDHLx(memCntr, memCntr.getR8(R8ID.D))
    return 8

def _0X73(memCntr):
    LDHLx(memCntr, memCntr.getR8(R8ID.E))
    return 8

def _0X74(memCntr):
    LDHLx(memCntr, memCntr.getR8(R8ID.H)) 
    return 8

def _0X75(memCntr):
    LDHLx(memCntr, memCntr.getR8(R8ID.L))
    return 8

def _0X77(memCntr):
    LDHLx(memCntr, memCntr.getR8(R8ID.A))
    return 8

################### LD X, (HL)
def LDxHL(memCntr, ID):
    hl = memCntr.getR16FromR8(R8ID.H)
    memValue = memCntr.getMemValue(hl)
    xLog = memCntr.getR8(ID)
    memCntr.setR8(ID, memValue)
    
    logAction(LDxHL.__name__,
          '=',
          xLog,
          memValue,
          memCntr.getR8(ID),
          memCntr.getR8(R8ID.F)
          )  
    
def _0X46(memCntr):
    LDxHL(memCntr, R8ID.B)
    return 8

def _0X56(memCntr):
    LDxHL(memCntr, R8ID.D)
    return 8

def _0X66(memCntr):
    LDxHL(memCntr, R8ID.H)
    return 8

def _0X4E(memCntr):
    LDxHL(memCntr, R8ID.C)
    return 8

def _0X5E(memCntr):
    LDxHL(memCntr, R8ID.E)
    return 8

def _0X6E(memCntr):
    LDxHL(memCntr, R8ID.L)
    return 8

def _0X7E(memCntr):
    LDxHL(memCntr, R8ID.A)
    return 8

################### LDH X, X --- r8 (0xFF00 = 65280)
def _0XE0(memCntr):
    adrParam = memCntr.getNextParam()
    memCntr.setMemValue(memCntr.getADR(0xFF, adrParam), memCntr.getR8(R8ID.A))   
    return 12

def _0XF0(memCntr):
    memCntr._register.A = memCntr.memory[0xFF00 | memCntr.memory[memCntr._register.PC]]
    memCntr._register.PC = memCntr._register.PC + 1

    logAction("_0XF0",
              '->',
              0xFF00 | memCntr.memory[memCntr._register.PC],
              memCntr.getMemValue(0xFF00 | memCntr.memory[memCntr._register.PC]),
              memCntr.getR8(R8ID.A),
              memCntr.getR8(R8ID.F))  
    return 12

def _0XE2(memCntr):
    memCntr.setMemValue(memCntr.getADR(0xFF, memCntr.getR8(R8ID.C)), memCntr.getR8(R8ID.A))
    return 8
    
def _0XF2(memCntr):
    memValue = memCntr.getMemValue(memCntr.getADR(0xFF, memCntr.getR8(R8ID.C)))
    memCntr.setR8(R8ID.A, memValue)
    return 8
    
################### LD X, X --- r16
def _0XEA(memCntr):
    param1 = memCntr.getNextParam()
    param2 = memCntr.getNextParam()    
    
    adr = memCntr.getADR(param2, param1)
    memCntr.setMemValue(adr, memCntr.getR8(R8ID.A))
    return 16
    
def _0XFA(memCntr):
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
    
    logAction(LD_R8.__name__,
              '<',
              oldLog,
              param,
              memCntr.getR8(ID),
              memCntr.getR8(R8ID.F)
              )    
      
def _0X06(memCntr):
    LD_R8(memCntr, R8ID.B)
    return 8

def _0X16(memCntr):
    LD_R8(memCntr, R8ID.D) 
    return 8

def _0X26(memCntr):
    LD_R8(memCntr, R8ID.H)
    return 8

def _0X0E(memCntr):
    LD_R8(memCntr, R8ID.C) 
    return 8

def _0X1E(memCntr):
    LD_R8(memCntr, R8ID.E)
    return 8

def _0X2E(memCntr):
    LD_R8(memCntr, R8ID.L)
    return 8

def _0X3E(memCntr):
    LD_R8(memCntr, R8ID.A)
    return 8
     
###################################################

''' 
### LD R, R ---- Register to Register
'''
def LD_RToR(memCntr, Rtarget, Rsource):
    oldLog = memCntr.getR8(Rtarget)
    
    #memCntr.registers[Rtarget] = memCntr.registers[Rsource]
    memCntr.setR8(Rtarget, memCntr.getR8(Rsource))
    logAction(LD_RToR.__name__,
              '<',
              oldLog,
              memCntr.getR8(Rsource),
              memCntr.getR8(Rtarget),
              memCntr.getR8(R8ID.F)
              )  
    
################### LD B, X
def _0X40(memCntr):
    LD_RToR(memCntr, R8ID.B, R8ID.B)
    return 4
    
def _0X41(memCntr):
    LD_RToR(memCntr, R8ID.B, R8ID.C)
    return 4

def _0X42(memCntr):
    LD_RToR(memCntr, R8ID.B, R8ID.D)
    return 4

def _0X43(memCntr):
    LD_RToR(memCntr, R8ID.B, R8ID.E)
    return 4

def _0X44(memCntr):
    memCntr._register.B = memCntr._register.H 
    #LD_RToR(memCntr, R8ID.B, R8ID.H)
    return 4

def _0X45(memCntr):
    LD_RToR(memCntr, R8ID.B, R8ID.L)
    return 4

def _0X47(memCntr):
    LD_RToR(memCntr, R8ID.B, R8ID.A)    
    return 4
    
################### LD C, X  
def _0X48(memCntr):
    LD_RToR(memCntr, R8ID.C, R8ID.B)
    return 4

def _0X49(memCntr):
    LD_RToR(memCntr, R8ID.C, R8ID.C)
    return 4
    
def _0X4A(memCntr):
    LD_RToR(memCntr, R8ID.C, R8ID.D)
    return 4
    
def _0X4B(memCntr):
    LD_RToR(memCntr, R8ID.C, R8ID.E)
    return 4
    
def _0X4C(memCntr):
    LD_RToR(memCntr, R8ID.C, R8ID.H)
    return 4

def _0X4D(memCntr):
    LD_RToR(memCntr, R8ID.C, R8ID.L)
    return 4

def _0X4F(memCntr):
    LD_RToR(memCntr, R8ID.C, R8ID.A) 
    return 4

################### LD D, X  
def _0X50(memCntr):
    LD_RToR(memCntr, R8ID.D, R8ID.B)
    return 4

def _0X51(memCntr):
    LD_RToR(memCntr, R8ID.D, R8ID.C)
    return 4

def _0X52(memCntr):
    LD_RToR(memCntr, R8ID.D, R8ID.D)
    return 4

def _0X53(memCntr):
    LD_RToR(memCntr, R8ID.D, R8ID.E)
    return 4

def _0X54(memCntr):
    LD_RToR(memCntr, R8ID.D, R8ID.H)
    return 4

def _0X55(memCntr):
    LD_RToR(memCntr, R8ID.D, R8ID.L)
    return 4

def _0X57(memCntr):
    LD_RToR(memCntr, R8ID.D, R8ID.A)
    return 4

################### LD E, X  
def _0X58(memCntr):
    LD_RToR(memCntr, R8ID.E, R8ID.B)
    return 4
    
def _0X59(memCntr):
    LD_RToR(memCntr, R8ID.E, R8ID.C)
    return 4

def _0X5A(memCntr):
    LD_RToR(memCntr, R8ID.E, R8ID.D)
    return 4

def _0X5B(memCntr):
    LD_RToR(memCntr, R8ID.E, R8ID.E)
    return 4

def _0X5C(memCntr):
    LD_RToR(memCntr, R8ID.E, R8ID.H)
    return 4

def _0X5D(memCntr):
    LD_RToR(memCntr, R8ID.E, R8ID.L)
    return 4

def _0X5F(memCntr):
    LD_RToR(memCntr, R8ID.E, R8ID.A)
    return 4

################### LD H, X  
def _0X60(memCntr):
    LD_RToR(memCntr, R8ID.H, R8ID.B)
    return 4

def _0X61(memCntr):
    LD_RToR(memCntr, R8ID.H, R8ID.C)
    return 4

def _0X62(memCntr):
    LD_RToR(memCntr, R8ID.H, R8ID.D)
    return 4

def _0X63(memCntr):
    LD_RToR(memCntr, R8ID.H, R8ID.E)
    return 4

def _0X64(memCntr):
    LD_RToR(memCntr, R8ID.H, R8ID.H)
    return 4

def _0X65(memCntr):
    LD_RToR(memCntr, R8ID.H, R8ID.L)
    return 4

def _0X67(memCntr):
    LD_RToR(memCntr, R8ID.H, R8ID.A)
    return 4

################### LD L, X
def _0X68(memCntr):
    LD_RToR(memCntr, R8ID.L, R8ID.B)
    return 4

def _0X69(memCntr):
    LD_RToR(memCntr, R8ID.L, R8ID.C)
    return 4

def _0X6A(memCntr):
    LD_RToR(memCntr, R8ID.L, R8ID.D)
    return 4
        
def _0X6B(memCntr):
    LD_RToR(memCntr, R8ID.L, R8ID.E)
    return 4

def _0X6C(memCntr):
    LD_RToR(memCntr, R8ID.L, R8ID.H)
    return 4

def _0X6D(memCntr):
    LD_RToR(memCntr, R8ID.L, R8ID.L)
    return 4
  
def _0X6F(memCntr):
    LD_RToR(memCntr, R8ID.L, R8ID.A)
    return 4

################### LD A, X
def _0X78(memCntr):
    LD_RToR(memCntr, R8ID.A, R8ID.B)
    return 4

def _0X79(memCntr):
    LD_RToR(memCntr, R8ID.A, R8ID.C)
    return 4

def _0X7A(memCntr):
    LD_RToR(memCntr, R8ID.A, R8ID.D)
    return 4
        
def _0X7B(memCntr):
    LD_RToR(memCntr, R8ID.A, R8ID.E)
    return 4

def _0X7C(memCntr):
    LD_RToR(memCntr, R8ID.A, R8ID.H)
    return 4

def _0X7D(memCntr):
    LD_RToR(memCntr, R8ID.A, R8ID.L)
    return 4
  
def _0X7F(memCntr):
    LD_RToR(memCntr, R8ID.A, R8ID.A)
    return 4

###################################################

# CPL A
def _0X2F(memCntr):
    a = memCntr.getR8(R8ID.A)
    aNew = ~a
    
    if aNew < 0:
        aNew = unpack('H', pack('h', aNew))[0]
        
        # Ignore first byte
        bArray = aNew.to_bytes(2, byteorder='big', signed=False)
        aNew = bArray[1]

    memCntr.setR8(R8ID.A, aNew)

    logAction(_0X2F.__name__, '~', a, aNew, memCntr.getR8(R8ID.A), memCntr.getR8(R8ID.F))    
    return 4

# LD BC, d16
def _0X01(memCntr):
    memCntr.setR8(R8ID.C, memCntr.memory[memCntr._register.PC])
    memCntr.setR8(R8ID.B, memCntr.memory[memCntr._register.PC + 1])
    memCntr._register.PC = memCntr._register.PC + 2
    return 12
    
# LD DE, d16
def _0X11(memCntr):
    memCntr.setR8(R8ID.E, memCntr.memory[memCntr._register.PC])
    memCntr.setR8(R8ID.D, memCntr.memory[memCntr._register.PC + 1])
    memCntr._register.PC = memCntr._register.PC + 2
    return 12
    
# LD SP, d16
def _0X31(memCntr):
    sp = memCntr.getAsR16(memCntr.memory[memCntr._register.PC + 1], memCntr.memory[memCntr._register.PC])
    memCntr._register.PC = memCntr._register.PC + 2
    memCntr.setSP(sp)
    logAction('SP d16',
              '<>',
              memCntr.memory[memCntr._register.PC + 1],
              memCntr.memory[memCntr._register.PC],
              sp,
              memCntr.getR8(R8ID.F))
    return 12
#     memCntr.setSP(
#         int.from_bytes(
#         bytearray([para2, para1]),
#         byteorder='big', 
#         signed=False)
#     ) 

# LD HL, d16    
def _0X21(memCntr):  
    memCntr.setR8(R8ID.L, memCntr.memory[memCntr._register.PC])
    memCntr.setR8(R8ID.H, memCntr.memory[memCntr._register.PC + 1])
    memCntr._register.PC = memCntr._register.PC + 2
    
    logAction('LD HL d16',
              '_',
              memCntr.getR8(R8ID.H),
              memCntr.getR8(R8ID.L),
              memCntr.getAsR16(memCntr.getR8(R8ID.H), memCntr.getR8(R8ID.L)),
              memCntr.getR8(R8ID.F))
    
    return 12
       
# roLX A    
def _0X17(memCntr):
    roLX(memCntr, R8ID.A)
    return 4
'''
### CB Codes
''' 
# roLX C
def cb_0X11(memCntr):
    roLX(memCntr, R8ID.C)
    return 8

# Swap A upper with higher nibbles
def cb_0X37(memCntr):
    
    a = memCntr.getR8(R8ID.A)
    x = a
    
    for i in range(0, 4):
        x *= 2
            
        # Remove 9th Bit and add put it to the start
        if( x & (1 << 8) ): 
            x = x | (1 << 0)
            x = x & ~(1 << 8)
    
    if( x == 0 ):
        memCntr.setZero()
    else:
        memCntr.resetZero()
        
    memCntr.resetSubstract()
    memCntr.resetHalfCarry()  
    memCntr.resetCarry()    
    
    memCntr.setR8(R8ID.A, x)
    
    logAction(cb_0X37.__name__,
              '#',
              a,
              x,
              memCntr.getR8(R8ID.A),
              memCntr.getR8(R8ID.F))    
    return 8

# # Test bit 7 of H
def cb_0X7C(memCntr):
 
    if( memCntr.getR8(R8ID.H) & (1 << 7) == 0 ):
        memCntr._registerFlags.Z = 1 
    else:
        memCntr._registerFlags.Z = 0
         
    memCntr._registerFlags.N = 0
    memCntr._registerFlags.H = 1
     
    logAction('B7 = 0',
              'B7',
              0xFF,
              0x80,
              memCntr.getR8(R8ID.H),
              memCntr.getR8(R8ID.F))
    return 8

# Reset bit 0 of A
def cb_0X87(memCntr):
    
    a = memCntr.getR8(R8ID.A)
    aLog = a
    
    # Remove 0th Bit
    a = a & ~(1 << 0)  
    memCntr.setR8(R8ID.A, a)

    logAction('R0, X',
              '=',
              aLog,
              a,
              memCntr.getR8(R8ID.A),
              memCntr.getR8(R8ID.F))
    return 8

# SRL B
def cb_0X38(memCntr):
    
    b = memCntr.getR8(R8ID.B)
    
    # Test 0th Bit and put it in Carry if 1
    b = b & ~(1 << 0) 
    if( b == b-1 ):
        memCntr.selfCarry()
    else:
        memCntr.resetCarry()
        
    b = b // 2 # Shift to Right
    bLog = b
    
    # Remove MSB Bit
    b = b & ~(1 << 7)  
    memCntr.setR8(R8ID.B, b)

    memCntr.resetSubstract()
    memCntr.resetHalfCarry()
    
    if( b == 0 ):
        memCntr.setZero()
    else:
        memCntr.resetZero()
        
    logAction('SRL, B',
              '=',
              bLog,
              b,
              memCntr.getR8(R8ID.B),
              memCntr.getR8(R8ID.F))
    return 8

def _0XCB(memCntr):
    cbCode = memCntr.getNextParam()
    func = globals()["cb_0X%0.2X" % cbCode]
    return func(memCntr) + 4 # +4 cycles for fetching cb
    
#     switcher = {
#        0x11: cb_0X11,
#        0x7C: cb_0X7C,
#        0x37: cb_0X37,
#        0x87: cb_0X87,
#        0x38: cb_0X38,
#        0x18: cb_0X18,
#        0x19: cb_0X19,
#        0x1A: cb_0X1A,
#        0x1B: cb_0X1B,
#        0x1C: cb_0X1C,
#        0x1D: cb_0X1D,
#        0x1F: cb_0X1F
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
def fetchOpCode(memCntr):
    

    

#     if(opCode == ):
#         start_time = time.perf_counter() 
    #time.perf_counter() # start time of the loop
    func = globals()["_0X%0.2X" % memCntr.memory[memCntr._register.PC]]    
    #func = opCodeToFunction[memCntr.memory[memCntr._register.PC]]
#     memCntr.oldPC = memCntr.memory[memCntr._register.PC]

    #print("PC: " + "_0X%0.2X" % memCntr._register.PC + ", OPCode: " + "_0X%0.2X" % memCntr.memory[memCntr._register.PC] + " - " + str(memCntr.memory[memCntr._register.PC]) + " func: " + func.__name__)
    
    memCntr.oldPC = memCntr.getPC()
    memCntr.incPC()
    
    #memCntr._register.PC = memCntr._register.PC + 1
    
#     start_time = time.perf_counter()
    return func(memCntr)

#     end_time = time.perf_counter() #time.perf_counter()
#     executionTimeReal = end_time - start_time
#     executionTimeReal *= 1000.0 * 1000.0
#     executionTimeShall = result * 0.0000002386 * 1000 * 1000
#     if( executionTimeReal > executionTimeShall ):            
#         print("Timing er qs: " + str(executionTimeReal) + "/" + str(executionTimeShall) + " OpCode: " + str("0X%0.2X" % memCntr.oldPC))
#         
    #return result
#     if(opCode == 0x20):
#         end_time = time.perf_counter() #time.perf_counter()
#         executionTimeReal = end_time - start_time
#         print("0x20: " + str(executionTimeReal * 1000 * 1000 * 1000) + str(" ns"))    
     
opCodeToFunction = {
    0: _0X00,
    1: _0X01,
    13: _0X0D,
    11: _0X0B,
    61: _0X3D, 
    4: _0X04,
    5: _0X05,
    6: _0X06,
    12: _0X0C, 
    14: _0X0E,
    17: _0X11,
    19: _0X13,
    23: _0X17,
    26: _0X1A,
    49: _0X31,
    50: _0X32,
    62: _0X3E,
    175: _0XAF,
    32: _0X20,
    33: _0X21,
    79: _0X4F,
    203: _0XCB,
    205: _0XCD,
    224: _0XE0,
    226: _0XE2,
    119: _0X77,
    123: _0X7B,
    193: _0XC1,
    197: _0XC5,
    34: _0X22,
    35: _0X23,
    201: _0XC9,
    254: _0XFE,
    234: _0XEA,
    40: _0X28,
    24: _0X18,
    46: _0X2E,
    103: _0X67,
    87: _0X57,
    30: _0X1E,
    29: _0X1D,
    240: _0XF0,
    36: _0X24,
    124: _0X7C,
    21: _0X15,
    22: _0X16,
    144: _0X90,
    190: _0XBE,
    125: _0X7D,
    120: _0X78,
    134: _0X86,
    195: _0XC3,
    128: _0X80,
    243: _0XF3,
    54: _0X36,
    42: _0X2A,
    177: _0XB1,
    251: _0XFB,
    47: _0X2F,
    230: _0XE6,
    71: _0X47,
    176: _0XB0,
    169: _0XA9,
    161: _0XA1,
    121: _0X79,
    239: _0XEF,
    135: _0X87,
    225: _0XE1,
    95: _0X5F,
    25: _0X19,
    94: _0X5E,
    86: _0X56,  
    213: _0XD5,
    233: _0XE9,
    255: _0XFF,
    38: _0X26,
    3: _0X03,
    27: _0X1B,
    18: _0X12,
    28: _0X1C,
    41: _0X29,
    229: _0XE5,
    209: _0XD1,
    245: _0XF5,
    250: _0XFA,
    167: _0XA7,
    202: _0XCA,
    200: _0XC8,
    126: _0X7E,
    241: _0XF1,
    53: _0X35,
    44: _0X2C,
    192: _0XC0,
    2: _0X02,
    60: _0X3C,
    111: _0X6F,
    249: _0XF9,
    122: _0X7A,
    183: _0XB7,
    20: _0X14,
    52: _0X34,
    217: _0XD9,
    196: _0XC4,
    198: _0XC6,
    214: _0XD6,
    70: _0X46,
    45: _0X2D,
    78: _0X4E,
    174: _0XAE,
    31: _0X1F,
    48: _0X30,
    37: _0X25,
    114: _0X72,
    113: _0X71,
    112: _0X70,
    206: _0XCE,
    182: _0XB6,
    110: _0X6E,
    102: _0X66,
    118: _0X76,
    108: _0X6C,
    96: _0X60,
    238: _0XEE,
    127: _0X7F,
    107: _0X6B,
    130: _0X82
}