import unittest
import opcodes
import memoryController
from enumRegister import R8ID

class Test(unittest.TestCase):
    
    # Init
    memCntr = memoryController.MemCntr()
    
    def test0XC5(self):
        self.resetRegister()
            
        self.memCntr.setR8(R8ID.B, 95)
        self.memCntr.setR8(R8ID.C, 95)
        self.memCntr.setSP(0xFFFE)
        opcodes._0XC5(self.memCntr)
        
        self.assertEqual(self.memCntr.getMemValue(0xFFFE), 0)
        self.assertEqual(self.memCntr.getMemValue(0xFFFD), 95)
        self.assertEqual(self.memCntr.getMemValue(0xFFFC), 95)
        self.assertEqual(self.memCntr.getMemValue(0xFFFB), 0)
        self.assertEqual(self.memCntr.getSP(), 0xFFFC)
        self.assertEqual(self.memCntr.getR8(R8ID.A), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.B), 95)
        self.assertEqual(self.memCntr.getR8(R8ID.C), 95)
        self.assertEqual(self.memCntr.getR8(R8ID.D), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.E), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.F), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.H), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.L), 0)

    def test0XC1(self):
        self.resetRegister()
            
        self.memCntr.setMemValue(0xFFFD, 95)
        self.memCntr.setMemValue(0xFFFC, 95)
        self.memCntr.setSP(0xFFFC)
        opcodes._0XC1(self.memCntr)
        
        self.assertEqual(self.memCntr.getMemValue(0xFFFE), 0)
        self.assertEqual(self.memCntr.getMemValue(0xFFFD), 95)
        self.assertEqual(self.memCntr.getMemValue(0xFFFC), 95)
        self.assertEqual(self.memCntr.getMemValue(0xFFFB), 0)
        self.assertEqual(self.memCntr.getSP(), 0xFFFE)
        self.assertEqual(self.memCntr.getR8(R8ID.A), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.B), 95)
        self.assertEqual(self.memCntr.getR8(R8ID.C), 95)
        self.assertEqual(self.memCntr.getR8(R8ID.D), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.E), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.F), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.H), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.L), 0)

    def test0X31(self):
        self.resetRegister()
            
        self.memCntr.setMemValue(self.memCntr.getPC(), 0x44)
        self.memCntr.setMemValue(self.memCntr.getPC() + 1, 0x23)
       
        opcodes._0X31(self.memCntr)
        
        self.assertEqual(self.memCntr.getPC(), 2)
        self.assertEqual(self.memCntr.getSP(), 0x2344)
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
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()