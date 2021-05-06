import pytest
import unittest

from likeasnail.opcodes import OXC8
from likeasnail.memoryController import MemCntr
from likeasnail.enumRegister import R8ID


class TestClass(unittest.TestCase):

    # Init
    memCntr = MemCntr('', '', True)

    def testOXC8(self):
        self.resetRegister()

        self.memCntr.setMemValue(0xFFFD, 0x95)
        self.memCntr.setMemValue(0xFFFC, 0x95)
        self.memCntr.setSP(0xFFFC)
        self.memCntr.setZero()
        OXC8(self.memCntr)

        self.assertEqual(self.memCntr.getMemValue(0xFFFE), 0)
        self.assertEqual(self.memCntr.getMemValue(0xFFFD), 0x95)
        self.assertEqual(self.memCntr.getMemValue(0xFFFC), 0x95)
        self.assertEqual(self.memCntr.getMemValue(0xFFFB), 0)
        self.assertEqual(self.memCntr.getSP(), 0xFFFE)
        self.assertEqual(self.memCntr.getPC(), 0x9595)
        self.assertEqual(self.memCntr.getR8(R8ID.A), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.B), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.C), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.D), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.E), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.F), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.H), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.L), 0)

    def resetRegister(self):
        self.memCntr.setPC(0)
        self.memCntr.setSP(0xFFFE)
        self.memCntr.setMemValue(0x0, 0)
        self.memCntr.setMemValue(0x1, 0)
        self.memCntr.setMemValue(0x2, 0)
        self.memCntr.setMemValue(0xFFFE, 0)
        self.memCntr.setMemValue(0xFFFD, 0)
        self.memCntr.setMemValue(0xFFFC, 0)
        self.memCntr.setMemValue(0xFFFB, 0)

        self.memCntr.setR8(R8ID.A, 0)
        self.memCntr.setR8(R8ID.B, 0)
        self.memCntr.setR8(R8ID.C, 0)
        self.memCntr.setR8(R8ID.D, 0)
        self.memCntr.setR8(R8ID.E, 0)
        self.memCntr.setR8(R8ID.F, 0)
        self.memCntr.setR8(R8ID.H, 0)
        self.memCntr.setR8(R8ID.L, 0)

        self.assertEqual(self.memCntr.getR8(R8ID.A), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.B), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.C), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.D), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.E), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.F), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.H), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.L), 0)
