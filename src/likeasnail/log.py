import logging


def logAction(strFName, strAction, aLog, x, result, flags):
    # return
    strPC = '%s: '
    stroLXogTab = '%s\t\t'
    stroLXog = '%s %s %s = %s'
    stroLXogFlag = '\tF: %s'

    if(len(strFName) > 5):
        stroLXogTab = '%s\t'

    # '04X' '08b'
    #memCntr = MemCntr.getInstance()

    logger = logging.getLogger()
    logger.info(strPC + stroLXogTab + stroLXog + stroLXogFlag,
                format(0, '04X'),
                strFName,
                format(aLog, '04X'),
                strAction,
                format(x, '04X'),
                format(result, '04X'),
                format(flags, '08b')
                )
