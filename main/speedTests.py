import timeit
number=1000

def printTime(value):      
    print(value)
    print(value / number)


register = [0, 0, 0, 0, 0, 0, 0, 0, 0]

register[1] = 0xFF

print(hex((register[1] & 1)))
print(hex((register[1] & (1 << 0))))

"""
0.0015924520000000011
1.592452000000001e-07

"""
  
setup = """
register = [0, 0, 0, 0, 0, 0, 0, 0, 0]
register[1] = 0xFE
"""

stmt= """
register[1] = 0xA0 | register[1] & (1 << 0)
"""

a = timeit.timeit(setup = setup, stmt = stmt, number=number)
printTime(a)

setup = """
register = [0, 0, 0, 0, 0, 0, 0, 0, 0]
register[1] = 0xFE
"""

stmt= """
register[1] |= 0xA0 | register[1] & (1 << 0)
"""

a = timeit.timeit(setup = setup, stmt = stmt, number=number)
printTime(a)

# setup = """
# from _register.lib import registerC
# class MemCntr:
#     _register = registerC
#     
# a = MemCntr()
# """
# stmt= """
# a._register.A = 20
# """
# a = timeit.timeit(setup = setup, stmt = stmt, number=number)
# printTime(a)
# 
# setup = """
# import array
# registers = array.array('B');
# registers.append(20)
# """
# stmt= """
# registers[0] = 30
# """
# a = timeit.timeit(setup = setup, stmt = stmt, number=number)
# printTime(a)
# 
# # 
# # a = timeit.timeit(setup = "from _registerFlags.lib import registerFlags; a = registerFlags", stmt = "a.C = 1", number=number)    
# # printTime(a)
# # a = timeit.timeit(setup = "from _registerFlags.lib import registerFlags", stmt = "registerFlags.C = 1", number=number)    
# # printTime(a)
# 
# #a = timeit.timeit(setup = "a = 0xF3", stmt = "a >= 256", number=number)
# #printTime(a)
# # import ctypes
# # 
# # 
# 
# 
# setup = """
# 
# def _0X00():
#     return 0
# 
# """
# stmt= """
# _0X00()
# """
# a = timeit.timeit(setup = setup, stmt = stmt, number=number)
# printTime(a)
# 
# setup = """
# class cx:
#     def _0X00(self):
#         return 0
#         
#     def _0X01(self):
#         return 0
#         
# b = cx()
# """
# stmt= """
# b._0X00()
# """
# a = timeit.timeit(setup = setup, stmt = stmt, number=number)
# printTime(a)
# 
# 
# # setup = """
# # import ctypes
# # uJmpValue = -50                        
# # """
# # stmt= """
# # a = ctypes.c_int8(uJmpValue).value  
# # """
# # a = timeit.timeit(setup = setup, stmt = stmt, number=number)
# # printTime(a)
# # setup = """
# # from _register.lib import registerC
# # import array
# # register16Bit = array.array('H');
# # register16Bit.append(0)
# # register16Bit.append(0)
# # _register = registerC
# # """
# # stmt= """
# # _register.PC = 0
# # _register.PC = _register.PC + 1
# # register16Bit[_register.PC]
# # """
# # a = timeit.timeit(setup = setup, stmt = stmt, number=number)
# # printTime(a)
# # 
# # setup = """
# # import array
# # register16Bit = array.array('H');
# # register16Bit.append(0)
# # register16Bit.append(0)
# # """
# # stmt= """
# # register16Bit[0] = 0
# # register16Bit[register16Bit[0]]
# # register16Bit[0] = register16Bit[0] + 1
# # """
# # a = timeit.timeit(setup = setup, stmt = stmt, number=number)
# # printTime(a)
# # setup = """
# # import numpy as np
# # 
# # tileArray = np.zeros(10, dtype = np.uint8);
# # a = 5                      
# # """
# # stmt= """
# # if( tileArray[0] == 1):
# #     a = 0
# # else:
# #     a = 2
# # """
# # a = timeit.timeit(setup = setup, stmt = stmt, number=number)
# # printTime(a)
# # 
# # #a = timeit.timeit(setup = "import enumRegister2", stmt = "enumRegister2.getState(0x03)" , number=number)
# # #printTime(a)
# # #print( timeit.timeit(setup = "from enumRegister2 import WAS", stmt = "WAS.G" , number=100000) )