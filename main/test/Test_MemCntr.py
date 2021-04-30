import unittest
import opcodes
import memoryController
from enumRegister import R8ID

class Test(unittest.TestCase):
    
    # Init
    memCntr = memoryController.MemCntr()
   
    def testSetR8(self):
        self.memCntr.setR8(R8ID.F, 0xFF)
        self.assertEqual(self.memCntr.getR8(R8ID.F), 0xF0)
        
        self.memCntr.setR8(R8ID.F, 0xAF)
        self.assertEqual(self.memCntr.getR8(R8ID.F), 0xA0)
        
        self.memCntr.setR8(R8ID.F, 0x00)
        self.assertEqual(self.memCntr.getR8(R8ID.F), 0x00)
        
        self.memCntr.setR8(R8ID.F, 0x10)
        self.assertEqual(self.memCntr.getR8(R8ID.F), 0x10)
        
    
    def testGetAsR16(self):
        self.assertEqual(self.memCntr.getAsR16(0x95, 0x95), 0x9595)
        self.assertEqual(self.memCntr.getAsR16(0x44, 0x23), 0x4423)
           
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
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()