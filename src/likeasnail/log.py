import logging

from .enumRegister import R8ID
from .memoryController import MemCntr


# def logAction(strFName, strAction, aLog, x, result, flags):
#     # return
#     strPC = '%s: '
#     stroLXogTab = '%s\t\t'
#     stroLXog = '%s %s %s = %s'
#     stroLXogFlag = '\tF: %s'
#
#     if(len(strFName) > 5):
#         stroLXogTab = '%s\t'
#
#     # '04X' '08b'
#     memCntr = MemCntr.getInstance()
#
#     logger = logging.getLogger()
#     logger.info(strPC + stroLXogTab + stroLXog + stroLXogFlag,
#                 format(memCntr.getPCBefore(), '04X'),
#                 strFName,
#                 format(aLog, '04X'),
#                 strAction,
#                 format(x, '04X'),
#                 format(result, '04X'),
#                 format(flags, '08b')
#                 )
def showTileIds(text, identifier):
    print(text + ' in range: ' + format(identifier[0], '04X') + " - " + format(identifier[1], '04X'))


def logState(memCntr, strFName):

    strPC = '%s: '
    funcName = '%s\t'
    registerLog = '\tA - L: %s%s %s%s %s%s %s%s %s (Z N H C)'

    if(len(strFName) > 5):
        funcName = '%s\t\t'

    logger = logging.getLogger()
    logger.info(strPC + funcName + registerLog + '\tSP: %s',
                format(memCntr.oldPC, '04X'),
                strFName,
                format(memCntr.getR8(R8ID.A), '02X'),
                format(memCntr.getR8(R8ID.F), '02X'),
                format(memCntr.getR8(R8ID.B), '02X'),
                format(memCntr.getR8(R8ID.C), '02X'),
                format(memCntr.getR8(R8ID.D), '02X'),
                format(memCntr.getR8(R8ID.E), '02X'),
                format(memCntr.getR8(R8ID.H), '02X'),
                format(memCntr.getR8(R8ID.L), '02X'),
                format((memCntr.getR8(R8ID.F) >> 3) & 0xF, '04b'),
                format(memCntr.getSP(), '04X')
                )
