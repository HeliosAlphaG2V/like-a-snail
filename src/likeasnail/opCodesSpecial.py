import logging
from .memoryController import MemCntr
from .log import logAction


def logSpecial(strFnName, strCommand):

    memCntr = MemCntr.getInstance()

#     logger = logging.getLogger()
#     logger.info('%s: %s\t\t%s',
#                 format(memCntr.getPC(), '04X'),
#                 strFnName,
#                 strCommand)

# DI


def OXF3(*_):
    # ToDo Disable interrupt
    memCntr = MemCntr.getInstance()
    memCntr.bInterruptOn = False
    memCntr.memory[0xFFFF] = 0x00
    logSpecial(OXF3.__name__, 'Disable Interrupt')
    return 4

# EI


def OXFB(*_):
    # ToDo Enable interrupt
    memCntr = MemCntr.getInstance()
    memCntr.bInterruptOn = True
    memCntr.memory[0xFFFF] = 0xFF
    logSpecial(OXFB.__name__, 'Enable Interrupt')
    return 4

# NOP


def OX00(*_):
    logSpecial(OX00.__name__, 'NOP')

    # logAction('NOP 0x00',
    #                   '<',
    #                   0,
    #                   0,
    #                   0,
    #                   0)

    return 4

# STOP


def OX10(*_):
    logSpecial(OX10.__name__, 'Stop')
    return 4

# HALT


def OX76(*_):
    logSpecial(OX76.__name__, 'Halt')
    return 4
