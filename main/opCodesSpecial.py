import logging
import memoryController
import opcodes

def logSpecial(strFnName, strCommand):
    
    memCntr = memoryController.MemCntr.getInstance()
    
#     logger = logging.getLogger()
#     logger.info('%s: %s\t\t%s',
#                 format(memCntr.getPC(), '04X'), 
#                 strFnName,
#                 strCommand)   

# DI
def _0XF3(*_):
    # ToDo Disable interrupt
    memCntr = memoryController.MemCntr.getInstance()
    memCntr.bInterruptOn = False
    memCntr.memory[0xFFFF] = 0x00
    logSpecial(_0XF3.__name__, 'Disable Interrupt')
    return 4

# EI
def _0XFB(*_):
    # ToDo Enable interrupt
    memCntr = memoryController.MemCntr.getInstance()
    memCntr.bInterruptOn = True
    memCntr.memory[0xFFFF] = 0xFF
    logSpecial(_0XFB.__name__, 'Enable Interrupt')
    return 4

# NOP
def _0X00(*_):
    logSpecial(_0X00.__name__, 'NOP')
    
    opcodes.logAction('NOP 0x00',
                      '<',
                      0,
                      0,
                      0,
                      0)
    
    return 4

# STOP
def _0X10(*_):
    logSpecial(_0X10.__name__, 'Stop')
    return 4

# HALT
def _0X76(*_):
    logSpecial(_0X76.__name__, 'Halt')
    return 4