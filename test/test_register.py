import unittest

import pytest

from likeasnail.enumRegister import R8ID
from likeasnail.memoryController import MemCntr


class Test(unittest.TestCase):

    def testARegister(self):
        MemCntr.resetInstance()
        memCntr = MemCntr('', '', True)

        self.assertEqual(memCntr.getR8(R8ID.A), 0)
        self.assertEqual(memCntr.getR8(R8ID.B), 0)
        self.assertEqual(memCntr.getR8(R8ID.C), 0)
        self.assertEqual(memCntr.getR8(R8ID.D), 0)
        self.assertEqual(memCntr.getR8(R8ID.E), 0)
        self.assertEqual(memCntr.getR8(R8ID.F), 0)
        self.assertEqual(memCntr.getR8(R8ID.H), 0)
        self.assertEqual(memCntr.getR8(R8ID.L), 0)

    def testBRegister(self):
        MemCntr.resetInstance()
        memCntr = MemCntr('', '', True)

        self.assertEqual(memCntr.getR8(R8ID.A), 0)
        self.assertEqual(memCntr.getR8(R8ID.B), 0)
        self.assertEqual(memCntr.getR8(R8ID.C), 0)
        self.assertEqual(memCntr.getR8(R8ID.D), 0)
        self.assertEqual(memCntr.getR8(R8ID.E), 0)
        self.assertEqual(memCntr.getR8(R8ID.F), 0)
        self.assertEqual(memCntr.getR8(R8ID.H), 0)
        self.assertEqual(memCntr.getR8(R8ID.L), 0)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
