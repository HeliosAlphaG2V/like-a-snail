from distutils.core import setup
from Cython.Build import cythonize
 
setup( name='GB emulator',
       ext_modules=cythonize(["enumRegister.py",
                              "opcodes.py",
                              "memoryController.py",
                              "opCodes*.py",
                              "main.py"
                              ])
      )