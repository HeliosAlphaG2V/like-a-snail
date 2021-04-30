import unittest
import opcodes
import memoryController
from enumRegister import R8ID

class Test(unittest.TestCase):
    
    # Init
    memCntr = memoryController.MemCntr()
    
    def test0X40(self):
        self.resetRegister()
            
        self.memCntr.setR8(R8ID.B, 95)
        opcodes._0X40(self.memCntr)
        
        self.assertEqual(self.memCntr.getR8(R8ID.A), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.B), 95)
        self.assertEqual(self.memCntr.getR8(R8ID.C), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.D), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.E), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.F), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.H), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.L), 0)

    def test0X41(self):
        self.resetRegister()
        
        self.memCntr.setR8(R8ID.C, 95)
        opcodes._0X41(self.memCntr)
        
        self.assertEqual(self.memCntr.getR8(R8ID.A), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.B), 95)
        self.assertEqual(self.memCntr.getR8(R8ID.C), 95)
        self.assertEqual(self.memCntr.getR8(R8ID.D), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.E), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.F), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.H), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.L), 0)

    def test0X42(self):
        self.resetRegister()
        
        self.memCntr.setR8(R8ID.D, 95)
        opcodes._0X42(self.memCntr)
        
        self.assertEqual(self.memCntr.getR8(R8ID.A), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.B), 95)
        self.assertEqual(self.memCntr.getR8(R8ID.C), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.D), 95)
        self.assertEqual(self.memCntr.getR8(R8ID.E), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.F), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.H), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.L), 0)

    def test0X43(self):
        self.resetRegister()
        
        self.memCntr.setR8(R8ID.E, 95)
        opcodes._0X43(self.memCntr)
        
        self.assertEqual(self.memCntr.getR8(R8ID.A), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.B), 95)
        self.assertEqual(self.memCntr.getR8(R8ID.C), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.D), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.E), 95)
        self.assertEqual(self.memCntr.getR8(R8ID.F), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.H), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.L), 0)

    def test0X44(self):
        self.resetRegister()
        
        self.memCntr.setR8(R8ID.H, 95)
        opcodes._0X44(self.memCntr)
        
        self.assertEqual(self.memCntr.getR8(R8ID.A), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.B), 95)
        self.assertEqual(self.memCntr.getR8(R8ID.C), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.D), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.E), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.F), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.H), 95)
        self.assertEqual(self.memCntr.getR8(R8ID.L), 0)
        
    def test0X45(self):
        self.resetRegister()
        
        self.memCntr.setR8(R8ID.L, 95)
        opcodes._0X45(self.memCntr)
        
        self.assertEqual(self.memCntr.getR8(R8ID.A), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.B), 95)
        self.assertEqual(self.memCntr.getR8(R8ID.C), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.D), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.E), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.F), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.H), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.L), 95)

    def test0X46(self):
        self.resetRegister()
        
        self.memCntr.setMemValue(self.memCntr.getAsR16(95, 95), 127)
        self.memCntr.setR8(R8ID.H, 95)
        self.memCntr.setR8(R8ID.L, 95)
        opcodes._0X46(self.memCntr)
        
        self.assertEqual(self.memCntr.getR8(R8ID.A), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.B), 127)
        self.assertEqual(self.memCntr.getR8(R8ID.C), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.D), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.E), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.F), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.H), 95)
        self.assertEqual(self.memCntr.getR8(R8ID.L), 95)
        
    def test0X47(self):
        self.resetRegister()
        
        self.memCntr.setR8(R8ID.A, 95)
        opcodes._0X47(self.memCntr)
        
        self.assertEqual(self.memCntr.getR8(R8ID.A), 95)
        self.assertEqual(self.memCntr.getR8(R8ID.B), 95)
        self.assertEqual(self.memCntr.getR8(R8ID.C), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.D), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.E), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.F), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.H), 0)
        self.assertEqual(self.memCntr.getR8(R8ID.L), 0)    
           
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