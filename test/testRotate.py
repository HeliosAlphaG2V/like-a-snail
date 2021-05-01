from opCodesRotate import rlX
from enumRegister import R8ID
import numpy as np
import memoryController

def main():
    
    #  Init
    memCntr = memoryController.MemCntr('', True)
    tileArray = np.zeros(16384, dtype = np.int16);
    tileArrayW = np.zeros(4096, dtype = np.int16);
    spriteArray = np.zeros((40, 4), dtype=np.int16)
    rxOld = 0
    ryOld = 0
    updateScene = False
    nDoubleCount = 0
    scanLineTiming = 456
    scanLineCycles = scanLineTiming
    MAXCYCLES = 70224
    CYCLES_PER_SECOND = 4194304
    cyclesThisUpdate = 0
    cycles = 0
    drawCounter = 0
    mode = 0
    
    print(format(2559, '08b'))
    print(format((2559 - (2559 & (1 << 8))), '08b'))
    memCntr.setCarry()    
 
    memCntr.setR8(R8ID.A, 127);
    print(format(memCntr.getR8(R8ID.A), '08b') + " - " + str(memCntr.getCarry()))
    rlX(memCntr, R8ID.A);
    memCntr.getR8(R8ID.A);
    print(format(memCntr.getR8(R8ID.A), '08b') + " - " + str(memCntr.getCarry()))
    
if __name__== "__main__":
    main()