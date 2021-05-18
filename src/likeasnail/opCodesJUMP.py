#!python
#cython: language_level=3

from struct import pack, unpack
from .enumRegister import R8ID, R8TOR16


def rstPush(memCntr, rst):
    bArray = memCntr.getTwoR8FromR16(memCntr.getPC())
    memCntr.push(bArray[R8TOR16.LOWER])
    memCntr.push(bArray[R8TOR16.UPPER])
    memCntr.setPC(rst)


# Jump if Z-Flag 0
def OX20(memCntr):

    if(memCntr.getZero() == 0):
        uJmpValue = memCntr.memory[memCntr._register.PC]

        if(uJmpValue > 127):
            uJmpValue = uJmpValue - 256

        memCntr._register.PC = memCntr._register.PC + uJmpValue + 1
        return 12
    else:
        memCntr._register.PC += 1
        return 8

# Jump


def OX18(memCntr):

    unsignedJpValue = memCntr.getNextParam()
    pc = memCntr.getPC()
    signedJpValue = unpack('b', pack('B', unsignedJpValue))[0]
    pc += signedJpValue
    memCntr.setPC(pc)

    return 12

# Jump to d16


def OXC3(memCntr):
    lowerParam = memCntr.getNextParam()
    upperParam = memCntr.getNextParam()

    memCntr.setPC(memCntr.getAsR16(upperParam, lowerParam))

    return 16

# Jump Zero to d16


def OXCA(memCntr):
    ret = 12
    lowerParam = memCntr.getNextParam()
    upperParam = memCntr.getNextParam()

    if (memCntr.getZero() == 1):  # Jump if z = 1
        memCntr.setPC(memCntr.getAsR16(upperParam, lowerParam))
        ret = 16

    return ret

# Jump Carry to d16


def OXDA(memCntr):
    ret = 12
    lowerParam = memCntr.getNextParam()
    upperParam = memCntr.getNextParam()

    if (memCntr.getCarry() == 1):  # Jump if z = 1
        memCntr.setPC(memCntr.getAsR16(upperParam, lowerParam))
        ret = 16

    return ret

# Jump if NC


def OX30(memCntr):
    ret = 8
    unsignedJpValue = memCntr.getNextParam()
    pc = memCntr.getPC()
    signedJpValue = 0

    if (memCntr.getCarry() == 0):
        signedJpValue = unpack('b', pack('B', unsignedJpValue))[0]
        pc += signedJpValue
        memCntr.setPC(pc)
        return 12

    return ret

# Jump if Zero


def OX28(memCntr):

    ret = 8
    unsignedJpValue = memCntr.getNextParam()
    pc = memCntr.getPC()
    signedJpValue = 0

    if (memCntr.getZero() == 1):  # Jump if z = 1
        signedJpValue = unpack('b', pack('B', unsignedJpValue))[0]
        pc += signedJpValue
        memCntr.setPC(pc)
        ret = 12

    return ret

# Jump if Carry


def OX38(memCntr):

    ret = 8
    unsignedJpValue = memCntr.getNextParam()
    pc = memCntr.getPC()
    signedJpValue = 0

    if (memCntr.getCarry() == 1):  # Jump if c = 1
        signedJpValue = unpack('b', pack('B', unsignedJpValue))[0]
        pc += signedJpValue
        memCntr.setPC(pc)
        ret = 12

    return ret

# JMP NZ, 0xNNNN


def OXC2(memCntr):
    ret = 12
    lowerParam = memCntr.getNextParam()
    upperParam = memCntr.getNextParam()

    # Call
    if (memCntr.getZero() == 0):
        # Callback address to stack
        memCntr.setPC(memCntr.getAsR16(upperParam, lowerParam))
        ret = 16

    return ret

# Call 0xNNNN


def OXCD(memCntr):
    lowerParam = memCntr.getNextParam()
    upperParam = memCntr.getNextParam()

    # Callback address to stack
    bArray = memCntr.getTwoR8FromR16(memCntr.getPC())
    memCntr.push(bArray[R8TOR16.LOWER])
    memCntr.push(bArray[R8TOR16.UPPER])

    # Call
    memCntr.setPC(memCntr.getAsR16(upperParam, lowerParam))

    return 24

# CALL NZ, 0xNNNN


def OXC4(memCntr):
    ret = 12
    lowerParam = memCntr.getNextParam()
    upperParam = memCntr.getNextParam()

    # Call
    if (memCntr.getZero() == 0):
        # Callback address to stack
        bArray = memCntr.getTwoR8FromR16(memCntr.getPC())
        memCntr.push(bArray[R8TOR16.LOWER])
        memCntr.push(bArray[R8TOR16.UPPER])
        memCntr.setPC(memCntr.getAsR16(upperParam, lowerParam))
        ret = 24

    return ret

# CALL NC, 0xNNNN


def OXD4(memCntr):
    ret = 12
    lowerParam = memCntr.getNextParam()
    upperParam = memCntr.getNextParam()

    # Call
    if (memCntr.getCarry() == 0):
        # Callback address to stack
        bArray = memCntr.getTwoR8FromR16(memCntr.getPC())
        memCntr.push(bArray[R8TOR16.LOWER])
        memCntr.push(bArray[R8TOR16.UPPER])
        memCntr.setPC(memCntr.getAsR16(upperParam, lowerParam))
        ret = 24

    return ret

# RET


def OXC9(memCntr):
    upperParam = memCntr.pop()
    lowerParam = memCntr.pop()
    memCntr.setPC(memCntr.getAsR16(upperParam, lowerParam))

    return 16

# RETI


def OXD9(memCntr):
    upperParam = memCntr.pop()
    lowerParam = memCntr.pop()

    memCntr.setPC(memCntr.getAsR16(upperParam, lowerParam))

    # Enable interrupt
    memCntr.bInterruptOn = True
    memCntr.setMemValue(0xFFFF, 0xFF)
    return 16

# RET NZ


def OXC0(memCntr):
    ret = 8

    if (memCntr.getZero() == 0):
        upperParam = memCntr.pop()
        lowerParam = memCntr.pop()
        memCntr.setPC(memCntr.getAsR16(upperParam, lowerParam))
        ret = 20

    return ret

# RET Z


def OXC8(memCntr):
    ret = 8

    if (memCntr.getZero() == 1):  # Jump if z = 1
        upperParam = memCntr.pop()
        lowerParam = memCntr.pop()
        memCntr.setPC(memCntr.getAsR16(upperParam, lowerParam))
        ret = 20

    return ret

# RET NC


def OXD0(memCntr):
    ret = 8

    if (memCntr.getCarry() == 0):
        upperParam = memCntr.pop()
        lowerParam = memCntr.pop()
        memCntr.setPC(memCntr.getAsR16(upperParam, lowerParam))
        ret = 20

    return ret

# RET C


def OXD8(memCntr):
    ret = 8

    if (memCntr.getCarry() == 1):
        upperParam = memCntr.pop()
        lowerParam = memCntr.pop()
        memCntr.setPC(memCntr.getAsR16(upperParam, lowerParam))
        ret = 20

    return ret
# JP


def OXE9(memCntr):
    memCntr.setPC(memCntr.getR16FromR8(R8ID.H))
    return 4

# RST


def OXCF(memCntr):
    rstPush(memCntr, 0x0008)
    return 16


def OXDF(memCntr):
    rstPush(memCntr, 0x0018)
    return 16


def OXEF(memCntr):
    rstPush(memCntr, 0x0028)
    return 16


def OXFF(memCntr):
    rstPush(memCntr, 0x0038)
    return 16


def OXC7(memCntr):
    rstPush(memCntr, 0x0000)
    return 16


def OXD7(memCntr):
    rstPush(memCntr, 0x0010)
    return 16


def OXE7(memCntr):
    rstPush(memCntr, 0x0020)
    return 16


def OXF7(memCntr):
    rstPush(memCntr, 0x0030)
    return 16
