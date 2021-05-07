#!python
# cython: language_level=3
import array
import logging
import os
from os.path import normpath
from random import randint
import struct
import sys

from lasregister.lib import registerFlags, registerC, getAF, getBC, getHL, getDE, setAF, setBC, setDE, setHL
from likeasnail.enumRegister import R8ID


class MemCntr:
    __instance = None

    _registerFlags = registerFlags
    _register = registerC

    #  Init values
    vRAMLoad = 0
    vRAMOld = 0
    vRAMFlag = 0
    oldPC = 0x00
    register16Bit = array.array('H')
    sp = array.array('H')
    registers = array.array('B')
    registerFlags = array.array('B')
    memory = array.array('B')
    bBootloader = array.array('B')
    bCartidge = array.array('B')
    bStack = array.array('B')
    cartidgeMax = 0x8000
    biosActive = True
    accessViolation = False
    bHandleInterrupt = False
    bInterruptOn = False
    opCode = 0xFFFF

    # Stack is working with HRAM, Work RAM
    def push(self, value):
        # self.bStack[self.getSP()] = value
        if(value > 0xFF):
            print("Overflow alert")
            raise MemoryError

        if(self.getSP() - 1 < 0):
            self.setSP(0xFFFE)
        else:
            self.setSP(self.getSP() - 1)

        self.memory[self.getSP()] = value

        logger = logging.getLogger()
        logger.info("PUSH (PC " + format(self.getPC(), '04X') + "): " +
                    format(self.getSP(), '04X') + " = " + format(value, '04X'))

        # if( self.getSP() < 0xFF80):
        #    print("SP violation 0xFF80: "+ format(self.getSP(), '04X'))

    # Stack is working with HRAM, Work RAM
    def pop(self):
        # value = self.bStack[self.getSP()]
        # self.bStack[self.getSP()] = 0x00

        value = self.memory[self.getSP()]
        self.setSP(self.getSP() + 1)

        # if( self.getSP() > 0xFFFF):
        #    print("SP violation 0xFF80: "+ format(self.getSP(), '04X'))
        if(value > 0xFF):
            print("Overflow alert")
            raise MemoryError

        return value

    def getAsR16(self, valueBig, valueLow):
        #         return int.from_bytes(
        #                    bytearray([valueBig, valueLow]),
        #                    byteorder='big',
        #                    signed=False)

        return (valueBig << 8) | valueLow
        # print("%0.2X" % valueLow + str(" - ") + "%0.2X" % valueBig)
        # return int(binascii.hexlify(bytearray([valueBig, valueLow])), 16)

    def getADR(self, valueBig, valueLow):
        return self.getAsR16(valueBig, valueLow)

    # @profile
    def getCombinedAdress(self):
        return (0xFF00 | self.getNextParam())

    def getTwoR8FromR16(self, value):

        bArray = struct.pack(">H", value)
#         a = struct.unpack(">I", "\x00\x00\x00"+bArray[0])[0]
#         b = struct.unpack(">I", "\x00\x00\x00"+bArray[1])[0]
#
        return bArray
        # return value.to_bytes(2, byteorder='big', signed=False)

#     def getR16FromR8(self, ID):
#         return int(binascii.hexlify(bytearray([self.getR8(ID), self.getR8(ID + 1)])), 16)
#
#     def setR16FromR8(self, ID, value):
#         bArray = struct.pack(">H", value)
#         self.setR8(ID, bArray[0])
#         self.setR8(ID+1, bArray[1])

    def getR16FromR8(self, ID):
        if(ID == R8ID.A):
            return getAF()
        elif(ID == R8ID.B):
            return getBC()
        elif(ID == R8ID.D):
            return getDE()
        elif(ID == R8ID.H):
            return getHL()
#         return int.from_bytes(
#                bytearray([self.getR8(ID), self.getR8(ID + 1)]),
#                byteorder='big',
#                signed=False)
        # reg16 = (self.getR8(ID) & 0xF0) & (self.getR8(ID+1) & 0xF0)
        # return int(binascii.hexlify(bytearray([self.getR8(ID), self.getR8(ID + 1)])), 16)
        # return (self.getR8(ID) & 0x00FF) & (self.getR8(ID+1) & 0xFF00)

    def setR16FromR8(self, ID, value):
        if(value > 0xFFFF):
            print("Overflow alert")
            raise MemoryError

        if(ID == R8ID.A):
            setAF((value & 0xFFF0))
        elif(ID == R8ID.B):
            setBC(value)
        elif(ID == R8ID.D):
            setDE(value)
        elif(ID == R8ID.H):
            setHL(value)

#         bArray = struct.pack(">H", value)
# #         a = struct.unpack(">I", "\x00\x00\x00"+bArray[0])[0]
# #         b = struct.unpack(">I", "\x00\x00\x00"+bArray[1])[0]
# #
#         #bArray = value.to_bytes(2, byteorder='big', signed=False)
#         self.setR8(ID, bArray[0])
#         self.setR8(ID+1, bArray[1])

    def setLine(self, value):
        self.memory[0xFF44] = value

    def getLine(self):
        return self.memory[0xFF44]

#     def getHLValue(self):
#         return self.getMemValue(self.getR16FromR8(R8ID.H))

    '''
    Address
    0x8000 = 32.768
    >= 0xFF80 (HRAM)
    '''

    def setMemValue(self, address, value):

        if type(value) is bytes:
            value = int.from_bytes(value, byteorder='little', signed=False)

        if(address < 32768) & (self.biosActive == False):
            print('Access violation on ',
                  hex(address),
                  '\tValue: ',
                  hex(value))

            print('# Current state ###########################')
            print(' A:\t', hex(self.getR8(R8ID.A)))
            print(' F:\t', bin(self.getR8(R8ID.F)), ('\t Z N H C'))
            print(' B:\t', hex(self.getR8(R8ID.B)))
            print(' C:\t', hex(self.getR8(R8ID.C)))
            print('PC:\t', hex(self.getPC()), '\t', self.getPC())
            print('SP:\t', hex(self.getSP()))
            print('HL:\t', hex(self.getR16FromR8(R8ID.H)))
            print('DE:\t', hex(self.getR16FromR8(R8ID.H)))
            print('############################################')
        else:
            if(address == 65360) & (value == 1):  # 0xFF50 = 65.360
                self.unmapBios()
                print('bios unmapped')

            elif(address == 65350):  # 0xFF46
                print('DMA transfer...')

                startAddress = value * 100
                for i in range(0, 160):  # 0 -> 0xA0
                    # 0xFE00
                    self.memory[65024 + i] = self.memory[startAddress + i]

                print('DMA transfer complete.')
                return

            elif(address == 65280):  # 0xFF00

                # 0x00CF is set to begin
                if(value == 0x0020):
                    self.memory[0xFF00] = 0x00EF  # No key was pressed FAKE
                elif(value == 0x0010):
                    self.memory[0xFF00] = 0x00DF  # No key was pressed FAKE
                elif(value == 0x0030):
                    self.memory[0xFF00] = 0x00FF  # No key was pressed FAKE
                else:
                    print("Error: Joypad matrix value is unknown")
                return

            elif(address == 65348):  # 0xFF44
                self.memory[address] = 0
                print("Scanline reset.")
                return

            # Check if interrupt is requested
            elif(address == 0xFF0F):

                logger = logging.getLogger()

                if((self.memory[0xFFFF] > 0) & (self.bInterruptOn) & (self.memory[0xFF0F] != 0xE0)):
                    self.bHandleInterrupt = True
                    logger.info("Interrupt request: " + format(self.getPC(), '04X') +
                                " --> " + format(self.oldPC, '04X') + ", type: " + format(value, '08b'))
                    self.setPC(self.oldPC)

                if(value == 0):
                    self.memory[0xFF0F] = 0xE0  # Remove all requests
                else:
                    self.memory[0xFF0F] = 0xE0 | value

                logger.info("Interrupt flag is set to: " +
                            format(self.memory[0xFF0F], '08b'))
                return

            if(value > 0xFF):
                print("Can not set memory value because it is to high: " +
                      str(value) + " Register A: " + str(self.getR8(R8ID.A)))
                print(format(self.getPC() - 1, '04X') + " PC -1 opCode: " +
                      format(self.memory[self.getPC() - 1], '04X'))
                print(format(self.getPC() - 2, '04X') + " PC -2 opCode: " +
                      format(self.memory[self.getPC() - 2], '04X'))
            else:
                self.memory[address] = value

            if(((address >= 0x8000) & (address <= 0x8FFF)) |
                    ((address >= 0x9800) & (address <= 0x9BFF))):
                self.vRAMLoad += 1
                # print("VRAM UPDATING...")

            # check if still increasing
            if((self.vRAMLoad == self.vRAMOld) & (self.vRAMLoad > 0) & (address != 0xFF44)):
                # print("Tile FLAG")
                self.vRAMFlag = 1
                self.vRAMLoad = 0
                self.vRAMOld = 0

            self.vRAMOld = self.vRAMLoad

    # @profile
    def getMemValue(self, address):
        return self.memory[address]

    def getNextParam(self):
        param = self.memory[self.getPC()]
        self.incPC()
        return param

#     def getR8(self, ID):
#         return self.registers[ID]
#
#     def setR8(self, ID, value):
#         self.registers[ID] = value
#
    def getR8(self, ID):
        if(ID == R8ID.A):
            return self._register.A
        elif(ID == R8ID.F):
            return (self._registerFlags.Z << 7) | (self._registerFlags.N << 6) | (self._registerFlags.H << 5) | (self._registerFlags.C << 4) | 0x00
        elif(ID == R8ID.B):
            return self._register.B
        elif(ID == R8ID.C):
            return self._register.C
        elif(ID == R8ID.D):
            return self._register.D
        elif(ID == R8ID.E):
            return self._register.E
        elif(ID == R8ID.H):
            return self._register.H
        elif(ID == R8ID.L):
            return self._register.L
        else:
            print("Error getR8: " + str(ID))
            raise MemoryError

    def setR8(self, ID, value):
        if(value > 0xFF):
            print("Overflow alert")
            raise MemoryError

        if(ID == R8ID.A):
            self._register.A = value
        elif(ID == R8ID.F):
            # Deny access to 0th - 3th Bit
            self._registerFlags.Z = (value & 0x80) >> 7
            self._registerFlags.N = (value & 0x40) >> 6
            self._registerFlags.H = (value & 0x20) >> 5
            self._registerFlags.C = (value & 0x10) >> 4
        elif(ID == R8ID.B):
            self._register.B = value
        elif(ID == R8ID.C):
            self._register.C = value
        elif(ID == R8ID.D):
            self._register.D = value
        elif(ID == R8ID.E):
            self._register.E = value
        elif(ID == R8ID.H):
            self._register.H = value
        elif(ID == R8ID.L):
            self._register.L = value
        else:
            print("Error setR8: " + str(ID))
            raise MemoryError

    def setSP(self, value):
        if(value > 0xFFFE):
            print("Stack pointer overflow!")
            raise MemoryError
        else:
            self.register16Bit[1] = value

    def getSP(self):
        return self.register16Bit[1]

    def setPC(self, value):
        self._register.PC = value
#         if(value == 0xC7C3):
#             for i in range(0x100, 0x8000):
#                 self.setMemValue(i, self.bCartidge[i])
#                 print("PC of " + "_0X%0.4X" % i + ": " + "_0X%0.2X" % self.getMemValue(i))
#
#             sys.exit()

    def getPC(self):
        return self._register.PC

    def getPCBefore(self):

        if(self.oldPC == None):
            return 0x00

        return self.oldPC

    def incPC(self):
        self._register.PC += 1
        # self.register16Bit[0] += 1

#     def loadOpCode(self):
#         #logger = logging.getLogger()
#         #logPC = self.getPC()
#
#         self.opCode = self.getMemValue(self.getPC())
#         self.oldPC = self.getPC()
#         self.incPC()

        # print(str(opCode))
        # logger.info( format(logPC, '04X') + " -> " + format(opCode, '04X') )

        # return self.opCode

    def getLastOpCode(self):
        return self.opCode

    '''
    Superfast C struct flag registers
    Read:  ~40 ns
    Write: ~50 ns
    '''

    @staticmethod
    def setCarry():
        registerFlags.C = 1

    @staticmethod
    def setHalfCarry():
        registerFlags.H = 1

    @staticmethod
    def setSubstract():
        registerFlags.N = 1

    @staticmethod
    def setZero():
        registerFlags.Z = 1

    @staticmethod
    def resetCarry():
        registerFlags.C = 0

    @staticmethod
    def resetHalfCarry():
        registerFlags.H = 0

    @staticmethod
    def resetSubstract():
        registerFlags.N = 0

    @staticmethod
    def resetZero():
        registerFlags.Z = 0

    @staticmethod
    def getCarry():
        return registerFlags.C

    @staticmethod
    def getHalfCarry():
        return registerFlags.H

    @staticmethod
    def getSubstract():
        return registerFlags.N

    @staticmethod
    def getZero():
        return registerFlags.Z

    def getReduced(self, item16Bit):
        item8Bit = 0

        for i in range(8):
            item8Bit |= item16Bit & (1 << i)

        return item8Bit
    ##################################################

    def loadBootloader(self, bootloader):
        fBootloader = open(bootloader, 'rb')

        # Load bootloader into memory
        self.bBootloader.fromfile(fBootloader,
                                  os.path.getsize(bootloader))

        # Map bios into memory
        if(len(self.bBootloader) == 0x100):
            for i in range(0x00, 0x100):
                self.setMemValue(i, self.bBootloader[i])
        else:
            print('Bios broken! Length is: ', len(self.bBootloader))

    def unmapBios(self):
        for i in range(0x00, 0x100):
            self.setMemValue(i, self.bCartidge[i])

        self.biosActive = False
        logger = logging.getLogger()
        logger.info('%s', '######### Bios unmapped #########')

    def loadCartidge(self, rom):
        fCartidge = open(rom, 'rb')

        # Load cartidge into memory
        self.bCartidge.fromfile(fCartidge,
                                os.path.getsize(rom))

        # Map cartidge into memory without unmapping the bios
        for i in range(0x100, 0x8000):
            self.setMemValue(i, self.bCartidge[i])

    @staticmethod
    def getInstance():
        if MemCntr.__instance != None:
            return MemCntr.__instance
        else:
            return None

    def __init__(self, boot, rom, skip=False):

        if MemCntr.__instance == None:
            MemCntr.__instance = self

        # System ON simulation - Fill registers with random data
        for i in range(0, 0x10000):
            self.memory.append(randint(0x00, 0x00))
            self.bStack.append(0x00)

            if(i < R8ID.PC):
                self.registers.append(randint(0x00, 0xFF))

        self.register16Bit.append(randint(0x0000, 0xFFFF))
        self.register16Bit.append(randint(0x0000, 0xFFFF))

        # Initial V-Blank (Set by bootloader)
        # self.memory[0xFF0F] = 0xE1

        # Boot routine
        self.register16Bit[0] = 0x0000
        self.register16Bit[1] = 0xFFFF
        self.registers[R8ID.F] = 0x00

        self._register.A = 0
        self._register.B = 0
        self._register.C = 0
        self._register.D = 0
        self._register.E = 0
        self._register.H = 0
        self._register.L = 0

        self._registerFlags.Z = 0
        self._registerFlags.N = 0
        self._registerFlags.H = 0
        self._registerFlags.C = 0

        # Bootloader
        self.setMemValue(0xFF50, 0x00)  # Map bootloader

        if not skip:
            self.loadBootloader(boot)
            self.loadCartidge(rom)
