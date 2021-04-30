import unittest
import opcodes
import memoryController
from enumRegister import R8ID

class Test(unittest.TestCase):
    
    # Init
    memCntr = memoryController.MemCntr()
    
    def test0X70(self):
        self.resetRegister()
            
        self.memCntr.setR8(R8ID.H, 95)
        self.memCntr.setR8(R8ID.L, 95)
        self.memCntr.setR8(R8ID.B, 127)
        opcodes._0X70(self.memCntr)
        
        self.assertEqual(self.memCntr.getMemValue(self.memCntr.getAsR16(95, 95)), 127)
        self.assertEqual(self.memCntr.getR8(R8ID.A), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.B), 127)
        self.assertEqual(self.memCntr.getR8(R8ID.C), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.D), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.E), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.F), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.H), 95)
        self.assertEqual(self.memCntr.getR8(R8ID.L), 95)
           
    def resetRegister(self):
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