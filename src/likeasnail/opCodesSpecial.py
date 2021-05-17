import logging

from .enumRegister import R8ID
##from .log import logAction
from .memoryController import MemCntr


def logSpecial(strFnName, strCommand):

    memCntr = MemCntr.getInstance()

#     logger = logging.getLogger()
#     logger.info('%s: %s\t\t%s',
#                 format(memCntr.getPC(), '04X'),
#                 strFnName,
#                 strCommand)


# DAA - As Z80 DAA Table

def OX27(memCntr):
    carry = memCntr.getCarry()
    halfCarry = memCntr.getHalfCarry()
    substract = memCntr.getSubstract()
    regA = memCntr.getR8(R8ID.A)
    regAUpper = regA & 0xF0
    regALower = regA & 0x0F

    if(carry == 0 and halfCarry == 0 and regAUpper <= 0x80 and regALower >= 0xA):
        regA += 0x06
        memCntr.resetCarry()
    elif(carry == 0 and halfCarry == 1 and regAUpper <= 0x90 and regALower <= 0x3):
        regA += 0x06
        memCntr.resetCarry()
    elif(substract == 0 and carry == 0 and halfCarry == 0 and regAUpper >= 0xA0 and regALower <= 0x9):
        # ADD check
        regA += 0x60
        memCntr.setCarry()
    elif(substract == 0 and carry == 0 and halfCarry == 0 and regAUpper >= 0x90 and regALower >= 0xA):
        # ADC check
        regA += 0x66
        memCntr.setCarry()
    elif(substract == 0 and carry == 0 and halfCarry == 0 and regAUpper >= 0xA0 and regALower <= 0x3):
        # INC check
        regA += 0x66
        memCntr.setCarry()
    elif(carry == 1 and halfCarry == 1 and regAUpper <= 0x20 and regALower <= 0x9):
        regA += 0x06
        memCntr.setCarry()
    elif(carry == 1 and halfCarry == 0 and regAUpper <= 0x20 and regALower >= 0xA):
        regA += 0x66
        memCntr.setCarry()
    elif(carry == 1 and halfCarry == 0 and regAUpper <= 0x30 and regALower <= 0x3):
        regA += 0x66
        memCntr.setCarry()
    elif(substract == 1 and carry == 0 and halfCarry == 1 and regAUpper <= 0x80 and regALower >= 0x6):
        # SBC check
        regA += 0xFA
        memCntr.resetCarry()
    elif(substract == 1 and carry == 1 and halfCarry == 0 and regAUpper >= 0x7 and regALower <= 0x9):
        # DEC check
        regA += 0xA0
        memCntr.setCarry()
    else:
        memCntr.resetCarry()

    if regA == 0:
        memCntr.setZero()
    else:
        memCntr.resetZero()

    memCntr.resetHalfCarry()
    memCntr.setR8(R8ID.A, 0xFF & regA)
    return 4
# CCF


def OX3F(memCntr):
    if(memCntr.getCarry() == 1):
        memCntr.setCarry()
    else:
        memCntr.resetCarry()

    memCntr.resetSubstract()
    memCntr.resetHalfCarry()
    return 4

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
    print('STOP!')
    return 4

# HALT


def OX76(*_):
    MemCntr.halt = True
    logSpecial(OX76.__name__, 'Halt')
    print('HALT!')
    return 4
