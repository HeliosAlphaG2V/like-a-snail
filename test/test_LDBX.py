import pytest
import unittest

from likeasnail.opcodes import OX40, OX41, OX42, OX43, OX44, OX45, OX46, OX47
from likeasnail.memoryController import MemCntr
from likeasnail.enumRegister import R8ID


class Test(unittest.TestCase):

    def test0X40(self):
        MemCntr.resetInstance()
        memCntr = MemCntr('', '', True)

        memCntr.setR8(R8ID.B, 95)
        OX40(memCntr)

        self.assertEqual(memCntr.getR8(R8ID.A), 0)
        self.assertEqual(memCntr.getR8(R8ID.B), 95)
        self.assertEqual(memCntr.getR8(R8ID.C), 0)
        self.assertEqual(memCntr.getR8(R8ID.D), 0)
        self.assertEqual(memCntr.getR8(R8ID.E), 0)
        self.assertEqual(memCntr.getR8(R8ID.F), 0)
        self.assertEqual(memCntr.getR8(R8ID.H), 0)
        self.assertEqual(memCntr.getR8(R8ID.L), 0)

    def test0X41(self):
        MemCntr.resetInstance()
        memCntr = MemCntr('', '', True)

        memCntr.setR8(R8ID.C, 95)
        OX41(memCntr)

        self.assertEqual(memCntr.getR8(R8ID.A), 0)
        self.assertEqual(memCntr.getR8(R8ID.B), 95)
        self.assertEqual(memCntr.getR8(R8ID.C), 95)
        self.assertEqual(memCntr.getR8(R8ID.D), 0)
        self.assertEqual(memCntr.getR8(R8ID.E), 0)
        self.assertEqual(memCntr.getR8(R8ID.F), 0)
        self.assertEqual(memCntr.getR8(R8ID.H), 0)
        self.assertEqual(memCntr.getR8(R8ID.L), 0)

    def test0X42(self):
        MemCntr.resetInstance()
        memCntr = MemCntr('', '', True)

        memCntr.setR8(R8ID.D, 95)
        OX42(memCntr)

        self.assertEqual(memCntr.getR8(R8ID.A), 0)
        self.assertEqual(memCntr.getR8(R8ID.B), 95)
        self.assertEqual(memCntr.getR8(R8ID.C), 0)
        self.assertEqual(memCntr.getR8(R8ID.D), 95)
        self.assertEqual(memCntr.getR8(R8ID.E), 0)
        self.assertEqual(memCntr.getR8(R8ID.F), 0)
        self.assertEqual(memCntr.getR8(R8ID.H), 0)
        self.assertEqual(memCntr.getR8(R8ID.L), 0)

    def test0X43(self):
        MemCntr.resetInstance()
        memCntr = MemCntr('', '', True)

        memCntr.setR8(R8ID.E, 95)
        OX43(memCntr)

        self.assertEqual(memCntr.getR8(R8ID.A), 0)
        self.assertEqual(memCntr.getR8(R8ID.B), 95)
        self.assertEqual(memCntr.getR8(R8ID.C), 0)
        self.assertEqual(memCntr.getR8(R8ID.D), 0)
        self.assertEqual(memCntr.getR8(R8ID.E), 95)
        self.assertEqual(memCntr.getR8(R8ID.F), 0)
        self.assertEqual(memCntr.getR8(R8ID.H), 0)
        self.assertEqual(memCntr.getR8(R8ID.L), 0)

    def test0X44(self):
        MemCntr.resetInstance()
        memCntr = MemCntr('', '', True)

        memCntr.setR8(R8ID.H, 95)
        OX44(memCntr)

        self.assertEqual(memCntr.getR8(R8ID.A), 0)
        self.assertEqual(memCntr.getR8(R8ID.B), 95)
        self.assertEqual(memCntr.getR8(R8ID.C), 0)
        self.assertEqual(memCntr.getR8(R8ID.D), 0)
        self.assertEqual(memCntr.getR8(R8ID.E), 0)
        self.assertEqual(memCntr.getR8(R8ID.F), 0)
        self.assertEqual(memCntr.getR8(R8ID.H), 95)
        self.assertEqual(memCntr.getR8(R8ID.L), 0)

    def test0X45(self):
        MemCntr.resetInstance()
        memCntr = MemCntr('', '', True)

        memCntr.setR8(R8ID.L, 95)
        OX45(memCntr)

        self.assertEqual(memCntr.getR8(R8ID.A), 0)
        self.assertEqual(memCntr.getR8(R8ID.B), 95)
        self.assertEqual(memCntr.getR8(R8ID.C), 0)
        self.assertEqual(memCntr.getR8(R8ID.D), 0)
        self.assertEqual(memCntr.getR8(R8ID.E), 0)
        self.assertEqual(memCntr.getR8(R8ID.F), 0)
        self.assertEqual(memCntr.getR8(R8ID.H), 0)
        self.assertEqual(memCntr.getR8(R8ID.L), 95)

    def test0X46(self):
        MemCntr.resetInstance()
        memCntr = MemCntr('', '', True)

        memCntr.setMemValue(memCntr.getAsR16(95, 95), 127)
        memCntr.setR8(R8ID.H, 95)
        memCntr.setR8(R8ID.L, 95)
        OX46(memCntr)

        self.assertEqual(memCntr.getR8(R8ID.A), 0)
        self.assertEqual(memCntr.getR8(R8ID.B), 127)
        self.assertEqual(memCntr.getR8(R8ID.C), 0)
        self.assertEqual(memCntr.getR8(R8ID.D), 0)
        self.assertEqual(memCntr.getR8(R8ID.E), 0)
        self.assertEqual(memCntr.getR8(R8ID.F), 0)
        self.assertEqual(memCntr.getR8(R8ID.H), 95)
        self.assertEqual(memCntr.getR8(R8ID.L), 95)

    def test0X47(self):
        MemCntr.resetInstance()
        memCntr = MemCntr('', '', True)

        memCntr.setR8(R8ID.A, 95)
        OX47(memCntr)

        self.assertEqual(memCntr.getR8(R8ID.A), 95)
        self.assertEqual(memCntr.getR8(R8ID.B), 95)
        self.assertEqual(memCntr.getR8(R8ID.C), 0)
        self.assertEqual(memCntr.getR8(R8ID.D), 0)
        self.assertEqual(memCntr.getR8(R8ID.E), 0)
        self.assertEqual(memCntr.getR8(R8ID.F), 0)
        self.assertEqual(memCntr.getR8(R8ID.H), 0)
        self.assertEqual(memCntr.getR8(R8ID.L), 0)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
