'''
    Stack notice:
    
    When pushing PC onto Stack it will be always
    the big value published and then the lower value
    
    When popping PC from Stack it will be always
    the lower value published and the the bigger value
    
    This has to stay in sync with Push and Pop commands!
    If it is not in sync this will result in
    unknown behaviour of jump commands.
    
    push BC
    99) B
    98) C
    
    pop C
    pop B
    => BC
    
    ##############################
    ## Try memory array as numpy
    ## Try Cython cdef stuff
    ## >> Try CFFI (better as from opcodesmodule import sayHelloFromC?) Timing: 0.009974369762135279
    ## Try PYPY3 with SDL2 (numpy no install!?)
    ##############################
'''
#import line_profiler
import os
import sys
import opcodes
import memoryController
import numpy as np
import pygame
from enumRegister import R8ID
import logging
import time
from pygame.locals import *

class emulatorAggregator:
    
    base_font = ""
    user_text = '0'
    # create rectangle
    input_rect = pygame.Rect(550, 550, 140, 32)
    color = pygame.Color('chartreuse4')
        
    biosUnmapped = False
    skipIT = False
    waitFor = 0
    thislist = [0x00]
     
    def main(self):
        self.emu()
        
    #@profile    
    def emu(self):  #loop, root, canvas
          
        logger = logging.getLogger() 
        logger.setLevel(0) # 0, 10, 20, ... 50
    
        pygame.init()
        pygame.font.init()
        self.base_font = pygame.font.Font(None, 32)
        pygame.display.set_caption("Gameboy classic emulator with pygame")
        font = pygame.font.Font(pygame.font.get_default_font(), 20)
         
        size = 800, 900
        screen = pygame.display.set_mode(size, pygame.DOUBLEBUF, 32)
        screen.fill( (128, 128, 128) )
         
        sfScreen = pygame.Surface((256, 256), pygame.HWSURFACE)
        sfScreen.fill((0, 0, 0), rect=None, special_flags=0)
        screenOffsetX = 130
        screenOffsetY = 120
        rectScreen = sfScreen.get_rect()
        rectScreen = rectScreen.move(screenOffsetX , screenOffsetY)
         
        sfTiles = pygame.Surface((250, 250), pygame.HWSURFACE) 
        sfTiles.fill((0, 0, 255), rect=None, special_flags=0)
        rectTiles = sfTiles.get_rect()
        rectTiles = rectTiles.move(552 , 0)
         
        sfSprite = pygame.Surface((250, 250), pygame.HWSURFACE) 
        sfSprite.fill((0, 255, 0), rect=None, special_flags=0)
        rectSfSprite = sfSprite.get_rect()
        rectSfSprite = rectSfSprite.move(552 , 260)
         
        sfBorder = pygame.Surface((160 , 144), pygame.SRCALPHA)
        sfBorder.fill((255, 255, 255, 0), rect=None, special_flags=0)
        rectBorder = sfBorder.get_rect()
        pygame.draw.rect(sfBorder, (128, 128, 128), (0, 0, 160, 144), 1)
        rectBorder = rectBorder.move(screenOffsetX, screenOffsetY)
         
        imgGB = pygame.image.load(os.path.join(os.getcwd()+'\\res\\' , 'gb.png'))
        
    #    asyncio.set_event_loop(loop)
    
        #===========================================================================
        # # #C0C0C0 #808080
        # for x in range(285):
        #     img.put("#C0C0C0", (x, 0))
        #         
        #===========================================================================
        
        #  Init
        memCntr = memoryController.MemCntr(os.path.join(os.getcwd()+'\\res\\' , 'Bootloader.bin'))
        tileArray = np.zeros(24576, dtype = np.int16); # 16384
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
        hold = False
        pcTargert = 0
        
        # Program cycle
        while(memCntr.getPC() < 0xFFFF):
    
            start_time = time.perf_counter()
            
            # PYGAME Event processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                
            if( memCntr.bHandleInterrupt ):
                memCntr.bHandleInterrupt = False
                splitPC = memCntr.getTwoR8FromR16(memCntr.getPC())
                memCntr.push(splitPC[1])
                memCntr.push(splitPC[0])
                
                iFlag = memCntr.getMemValue(0xFF0F)
     
                if( (iFlag & (1 << 0) == 1) ):
                    memCntr.setPC(0x0040) # V-Blank ISR
                    print("V-Blank ISR")
                    
                elif( (iFlag & (1 << 1) == 2) ):
                    memCntr.setPC(0x0048) # LCD ISR
                    print("LCD ISR")
                    
                elif( (iFlag & (1 << 2) == 4) ):
                    memCntr.setPC(0x0050) # Timer ISR
                    print("Timer ISR")
                    
                elif( (iFlag & (1 << 3) == 8) ):
                    memCntr.setPC(0x0060) # Joypad ISR   
                    print("Joypad ISR")
    
            '''
                CPU cycle
                
                Execute MAXCYCLES then update rest!
                60 * 65000 = 3.900.000 (60 Refresh)
                60 times = every 65000 cycles! :D
            '''
            while( MAXCYCLES >= cyclesThisUpdate ):
                
#           # DBG - Stop and Go
#                 #print(int(self.user_text, 16))
#                 
#                 for event in pygame.event.get():
#   
#                         # if user types QUIT then the screen will close
#                         if event.type == pygame.QUIT:
#                             pygame.quit()
#                             sys.exit()
#                   
#                         if event.type == pygame.KEYDOWN:
#                   
#                             # Check for backspace
#                             if event.key == pygame.K_BACKSPACE:
#                   
#                                 # get text input from 0 to -1 i.e. end.
#                                 self.user_text = self.user_text[:-1]
#                   
#                             # Unicode standard is used for string
#                             # formation
#                             else:
#                                 self.user_text += event.unicode   
#                                 
#                         if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
#                             hold = True
#                             pcTargert = int(self.user_text, 16)
#                             print("Hold state: " + str(hold))
#                                 
#                 if(memCntr.getPC() == pcTargert and hold):
#                     self.updateSceneFC(memCntr, screen, rxOld, ryOld, imgGB, sfScreen, rectScreen, sfBorder, rectBorder, sfSprite, rectSfSprite, 0, font)
#                     continue
                
#                 # DBG
#                 if((memCntr.getPC() > self.waitFor) and (self.skipIT == True)):
#                     self.thislist.clear()
#                     self.thislist.append(0x00)
#                     self.waitFor = 0
#                     self.skipIT = False
#                     print("Skipping stopped... waitFor: " + str(self.waitFor) + " " + str(self.skipIT))
#                     
#                 else:
#                         
#                     if((memCntr.getPC() >= 0x100) or self.biosUnmapped):                         
#                         if((self.thislist.count(self.thislist[0]) >= 3)):
#                             print("Skipping loop... for: " + str(self.thislist[0]) + " - " + str(self.thislist.count(self.thislist[0])))
#                             self.waitFor = self.thislist[0]
#                             self.skipIT = True
#                             
#                         else:
#                             
#                             print("waiting...")
#                             a = pygame.event.wait()
#                      
#                             if a.type != KEYDOWN:
#                                 pygame.event.clear()
#                                 self.biosUnmapped = True
#                                 print("continue")
#                                 continue
#                             else:
#                                 if(len(self.thislist) > 20):
#                                     self.thislist.clear()
#                                     
#                                 self.thislist.append(memCntr.getPC())
#                                 self.thislist.sort(reverse = True)
#                                 self.updateSceneFC(memCntr, screen, rxOld, ryOld, imgGB, sfScreen, rectScreen, sfBorder, rectBorder, sfSprite, rectSfSprite, memCntr.getMemValue(memCntr.getPC()), font)
                 
                '''
                    only opcodes 9 - 11 ms without cython
                '''
                opCode = memCntr.getMemValue(memCntr.getPC())
                start_timeX = time.perf_counter() # time.perf_counter() 
                
                result = opcodes.fetchOpCode(memCntr)
                
                             
                end_time = time.perf_counter() #time.perf_counter()
                executionTimeReal = end_time - start_timeX
                executionTimeReal *= 1000.0 * 1000.0 * 1000.0
                executionTimeShall = result * 0.2386 * 1000.0
    #             if(True): # executionTimeReal > executionTimeShall             
    #                 print("Timing opCode: " + str(executionTimeReal) + "/" + str(executionTimeShall) + " opCode: " + "%0.4X" % opCode )
    #             if( executionTimeReal > executionTimeShall ): #            
    #                 print("Timing error on: " + str(executionTimeReal) + "/" + str(executionTimeShall) )
    
                
                cyclesThisUpdate += result      
                cycles += result
             
                '''
                    LCD 15 - 17 ms (really bad lol)
                '''
                # LCD handling            
                if( memCntr.memory[0xFF40] & (1 << 7) != 0 ):
    
                    # Get LCD status
                    currentHorizontalLine = memCntr.memory[0xFF44]
                    status = memCntr.memory[0xFF41]
                    currentMode = status & 0x03
    
                    '''
                        The whole frame takes (154 * 456) 70224 clock cycles
                        Vertical blank period takes (10 * 456) 4560 clock cycles
                    '''
                    # (MODE 1) Vertical blank period started => set status to [... 0 1]
                    if( (currentHorizontalLine >= 144) & (currentMode != 1) ):
                        status = (status & 0xFC) | 1
                        # V blank interrupt enabled check
                        if( status & (1 << 4) != 0 ):
                            print("LCD requests interrupt (V-Blank)")
                    else:
                        '''
                            Speed things up! (There is no hardware)
                            It takes normally 456 clock cycles to go trough all stages
                            1. Searching OAM I do not care (80 clock cycles)
                            2. Data to LCD I do not care (172 clock cycles)
                            3. Horizontal blank I do not care (204 clock cycles)
                            
                            All the interrupts should not occur instantly
                            so just make a small difference between these,
                            so that not more than one gets called.
                            
                            Longest clock cycle for a command is 24.
                            3 * 24 = 72 clock cycles as buffer.
                            0   - 72:  1.
                            72  - 144: 2.
                            144 - 216: 3.
                            So I need only 216 clock cycles to build one scanline
                        '''
                        # (MODE 2) Searching OAM
                        if( (scanLineCycles > 144) & (currentMode != 2) ):
                            status = (status & 0xFC) | 2
                            if( status & (1 << 5) != 0 ):
                                print("LCD requests interrupt (OAM)")
                        # (MODE 3) Data to LCD driver
                        elif( (scanLineCycles > 72) & (currentMode != 3) ):
                            status = (status & 0xFC) | 3
                        # (MODE 0) Horizontal blank
                        else:
                            status = status & 0xFC
                            if( status & (1 << 3) != 0 ):
                                print("LCD requests interrupt (H-Blank)")
    
    
                    # LYC == LY check (set LYC == LY flag in stat register)
                    if( memCntr.memory[0xFF45] == currentHorizontalLine ):
                        status = status | 4
                        memCntr.memory[0xFF41] = status
                        if( status & (1 << 6) != 0 ):
                            print("LCD requests interrupt (LYC == LY)")  
                    else:
                        status = status & 0xFB
                        memCntr.memory[0xFF41] = status
    
                    # LY update
                    scanLineCycles -= result
                    
                    if( scanLineCycles <= 0 ):
                        scanLineCycles = 216
                          
                        # Vertical blank period at 144 to 153 (> 153 : Frame is complete)
                        if( currentHorizontalLine == 153 ):
                            memCntr.memory[0xFF44] = 0
                        else:
                            if( currentHorizontalLine == 144 ):
                                memCntr.setMemValue(0xFF0F, 0x01)
                                #print("Request vertical blank interrupt")
                            # Next scanline
                            memCntr.memory[0xFF44] = currentHorizontalLine + 1
                       
    
                # Display is off            
                else:
                    scanLineCycles = 216 
                    memCntr.memory[0xFF44] = 0
                    memCntr.memory[0xFF41] = (memCntr.memory[0xFF41] & 0xFE) | 0x01
                #########################################################
    
            # Check the execution timing of 16.6666 ms
            end_time = time.perf_counter() #time.perf_counter()
            executionTimeReal = end_time - start_time
            executionTimeReal *= 1000.0
            #print("Timing ms (" + str(drawCounter) +  "): " + str(executionTimeReal) + "/ 16.66")
                
            # Frame counter
            if( drawCounter > 60 ):
                drawCounter = 0
            drawCounter += 1
            updateScene = True
            cyclesThisUpdate = 0
            #sys.exit()
            
            if( cycles >= CYCLES_PER_SECOND ):
                cycles = 0
                end_time = time.perf_counter() #time.perf_counter()
                executionTimeReal = end_time - start_time
    #             print("Timing s: " + str(executionTimeReal) + "/ 1s")
    #             print("######### One second in GB finished #########")
                               
            # Render tiles memCntr.vRAMFlag == 1 
            if( ( updateScene ) and self.isLCDOn(memCntr) and (memCntr.vRAMFlag == 1) ):             
                #print("Updating tiles...")
                
                # Bit 4 - BG & Window Tile Data Select (0=8800-97FF, 1=8000-8FFF)
                nBGTileMapSelection = ( memCntr.getMemValue(0xFF40) & (1 << 4) )
                # Bit 6 - Window Tile Map Display Select (0=9800-9BFF, 1=9C00-9FFF)
                nWindowTileMapSelection = ( memCntr.getMemValue(0xFF40) & (1 << 6) )
                # Bit 1 - OBJ (Sprite) Display Enable (0=Off, 1=On)
                nSprite = ( memCntr.getMemValue(0xFF40) & (1 << 1) )
                
                if( nBGTileMapSelection == 16 ):
                    nStart = 0x8000
                    nStop = 0x8FFF
                else:
                    nStart = 0x8800
                    nStop = 0x97FF
    
                if( nWindowTileMapSelection == 64 ):
                    nWStart = 0x9C00
                    nWStop = 0x9FFF               
                else:
                    nWStart = 0x9800
                    nWStop = 0x9BFF
                    
    #             # DBG
    #             if(memCntr.getPC() > 0xC000):
    #                 for i in range(0x9800, 0x9BFF):
    #                     #print(memCntr.getMemValue(i))
    #                     memCntr.setMemValue(i, 70)
    #                 
    #                 # sys.exit()
                    
                print("Checking BG tiles in range: " + format(nStart, '04X') + " - " + format(nStop, '04X'))
                print("Checking W tiles in range: " + format(nWStart, '04X') + " - " + format(nWStop, '04X'))
                
                memCntr.vRAMFlag = 0
                self.getTileArray(memCntr, 0x8000, 0x97F0, tileArray)    # Tiles
                self.getTileArray(memCntr, nWStart, nWStop, tileArrayW) # Screen
                
                if( nSprite == 2 ):
                    
                    count = 0
                    
                    # Each sprite has 4 Bytes (160 Bytes / 4 Bytes = 40 Sprites)
                    for i in range(0xFE00, 0xFEA0, 4):
                        
                        spriteArray[count, 0] = memCntr.getMemValue(i)      # X
                        spriteArray[count, 1] = memCntr.getMemValue(i + 1)  # Y
                        spriteArray[count, 2] = memCntr.getMemValue(i + 2)  # Tilenumber
                        spriteArray[count, 3] = memCntr.getMemValue(i + 3)  # Attribute
                        
    #                     if( spriteArray[count, 2] != 0 ):
    #                         print( format(spriteArray[count, 2], '02X') )
                            
                        count += 1
                       
                self.drawSprites(sfSprite, spriteArray, tileArray)        
                self.drawTiles(sfTiles, tileArray)
                self.drawBG(sfScreen, tileArray, memCntr)
                screen.blit(sfTiles, rectTiles) 
    
            if( updateScene ):  
                self.updateSceneFC(memCntr, screen, rxOld, ryOld, imgGB, sfScreen, rectScreen, sfBorder, rectBorder, sfSprite, sfTiles, rectTiles, rectSfSprite, opCode, font)
                updateScene = False 
                        
    #         if( time.time() - start_time != 0):
    #             print("Time: ", (time.time() - start_time)) # FPS = 1 / time to process loop
        
    #         executionTimeReal = time.time() - start_time
    #         executionTimeShall = result * 0.0002386
    #         
    #         if( executionTimeReal > executionTimeShall ):            
    #             print("Timing er qs: " + str(executionTimeReal*1000.0) + "/" + str(executionTimeShall*1000.0) + " OpCode: " + format(memCntr.getLastOpCode(), '04X'))
    #         else:
    #             print("Timing ok " + str(executionTimeReal) + "/" + str(executionTimeShall))
            
            
        print('######## EXIT #####################')
        print(' A:\t', hex(memCntr.getR8(R8ID.A)))
        print(' F:\t', bin(memCntr.getR8(R8ID.F)),('\t Z N H C'))
        print(' B:\t', hex(memCntr.getR8(R8ID.B)))
        print(' C:\t', hex(memCntr.getR8(R8ID.C)))
        print('PC:\t', hex(memCntr.getPC()), '\t', memCntr.getPC())
        print('SP:\t', hex(memCntr.getSP()))
        print('HL:\t', hex(memCntr.getR16FromR8(R8ID.H)))
        print('DE:\t', hex(memCntr.getR16FromR8(R8ID.H)))
    
    def updateSceneFC(self, memCntr, screen, rxOld, ryOld, imgGB, sfScreen, rectScreen, sfBorder, rectBorder, sfSprite, sfTiles, rectTiles, rectSfSprite, opCode, font):
        #print("Updating scene...")  
        
        # Window    
        #nWindowX = memCntr.getMemValue(0xFF4B)
        #nWindowY = memCntr.getMemValue(0xFF4A)
        
        # Screen border    
        rx = memCntr.getMemValue(0xFF43)
        ry = memCntr.getMemValue(0xFF42)
        rxDelta = rx - rxOld
        ryDelta = ry - ryOld
        rectBorder = rectBorder.move(rxDelta, ryDelta)
        rxOld = rx
        ryOld = ry 
             
        screen.blit(imgGB, imgGB.get_rect())
        screen.blit(sfScreen, rectScreen)
        screen.blit(sfBorder, rectBorder)
        screen.blit(sfSprite, rectSfSprite)
        screen.blit(sfTiles, rectTiles)
        
        strArray = [str("IME: ")+str(format(memCntr.getMemValue(0xFFFF), "08b")),
                    str("LCD: ")+str(format(memCntr.getMemValue(0xFF41), "08b")),
                    str("LC: ")+str(format(memCntr.getMemValue(0xFF40), "08b")), 
                    str("SX: ")+str(format(memCntr.getMemValue(0xFF43), "08b")),
                    str("SY: ")+str(format(memCntr.getMemValue(0xFF42), "08b")),
                    str("WX: ")+str(format(memCntr.getMemValue(0xFF4B), "08b")),
                    str("WY: ")+str(format(memCntr.getMemValue(0xFF4A), "08b")),
                    str("OC: ")+str(format(opCode, "04X")+str(" PC: ")+format(memCntr.getPC(), "04X")),
                    str("AF: ")+str(format(memCntr.getR16FromR8(R8ID.A), "04X")),
                    str("BC: ")+str(format(memCntr.getR16FromR8(R8ID.B), "04X")),
                    str("DE: ")+str(format(memCntr.getR16FromR8(R8ID.D), "04X")),
                    str("HL: ")+str(format(memCntr.getR16FromR8(R8ID.H), "04X")),
                    str("SP: ")+str(format(memCntr.getSP(), "04X"))]
        
        pygame.draw.rect(screen, self.color, self.input_rect)
        text_surface = self.base_font.render(self.user_text, True, (255, 255, 255))   
        # render at position stated in arguments
        screen.blit(text_surface, (self.input_rect.x+5, self.input_rect.y+5)) 
        # set width of textfield so that text cannot get
        # outside of user's text input
        self.input_rect.w = max(100, text_surface.get_width() + 50)
                                
        for i in range(len(strArray)):
            sfInfo = font.render(strArray[i], 0, (0, 0, 0))
            sfInfoRect = sfInfo.get_rect()
            sfInfoRect = sfInfoRect.move(20, i*20 + 600)
            screen.blit(sfInfo, sfInfoRect)   
         
        pygame.display.flip()
              
    def isLCDOn(self, memCntr):
        
        # Bit 7 - LCD Display Enable (0=Off, 1=On)
        if( (memCntr.memory[0xFF40] & (1 << 7) == 0) ):
            return False
            # You can only write when H-Blank or V-Blank
        else:
            return True
            # You can write to video memory without restrictions
    
    # TODO: Check when it has to be monochrome    
    def getTileArray(self, memCntr, nStart, nStop, tileArray):
        
        count = 0
    
        for memAddr in range(nStart, nStop, 2):
            data1 = memCntr.getMemValue(memAddr)
            data2 = memCntr.getMemValue(memAddr + 1)
    
            #===============================================================
            # ## STRG+4 // +5
            # if( (memAddr >= 0x8270) & (memAddr < 0x8280) ):
            #     print("------------ Pixel: ", count)
            #     print("1: ", bin(data1))
            #     print("2: ", bin(data2))
            #     print("-- Be aware of LSB start position! -----------")
            #===============================================================
            for i in reversed(range(0, 8)):
                
                tileClr = (data1 & (1 << i)) + (data2 & (1 << i))
                
                if( tileClr == 0 ):
                    tileArray[count] = 1; 
                elif ( tileClr > 1 ):
                    tileArray[count] = 4;    
                else:
                    if(data1 & (1 << i) == 1):
                        tileArray[count] = 4;
                    else:
                        tileArray[count] = 4;
    
    #         for i in reversed(range(8)):
    #             if( (data1 & (1 << i)) and (data2 & (1 << i)) ):
    #                 # print('black')
    #                 tileArray[count] = 4; 
    #             elif ( (((data1 & (1 << i)) == 0) and ((data2 & (1 << i))) == 0) ):
    #                 # white
    #                 tileArray[count] = 1;    
    #             elif ( (data1 & (1 << i)) > 0 ): 
    #                 # print('ligth grey')
    #                 tileArray[count] = 3;
    #             elif ( (data2 & (1 << i)) > 0 ): 
    #                 # print('dark grey')
    #                 tileArray[count] = 2;
    #             else:
    #                 print("Color failure!")
                
                #===========================================================
                # if( (memAddr >= 0x8270) & (memAddr < 0x8280) ):
                #     print("D1: ", (data1 & (1 << i)) ) 
                #     print("D2: ", (data2 & (1 << i)) ) 
                #     print("Picked: ", tileArray[count]) 
                #===========================================================
                count += 1;   
                
        #print(str(count))
    
    def drawSprites(self, sf, spriteArray, tileArray):
        
        bgStartPointX = 0
        bgStartPointY = 0
        sf.lock()
        
        for i in range(40):
            tileID = spriteArray[i, 2]
            tilePosition = tileID * 64;
            
            for y in range(bgStartPointY, bgStartPointY + 8):
                for x in range(bgStartPointX, bgStartPointX + 8):
                    
                    color = (255, 0, 255) # Error color (Pink)
                    
                    if( tileArray[tilePosition] == 1 ):
                        color = (255, 255, 255)
                    elif( tileArray[tilePosition] == 2 ):
                        color = (128, 128, 128)
                    elif( tileArray[tilePosition] == 3 ):
                        color = (192, 192, 192)
                    elif( tileArray[tilePosition] == 4 ):
                        color = (0, 0, 0)
                     
                    sf.set_at((x, y), color)    
                    tilePosition += 1
                     
            bgStartPointX += 8;
            # 64 (8 Tiles in a row)
            # 128 (16 Tiles in a row)
            if( bgStartPointX == 256 ):
                bgStartPointX = 0;
                bgStartPointY += 8;
        
        sf.unlock()
        
    def drawBG(self, sf, tileArray, memCntr):
    
        bgStartPointX = 0
        bgStartPointY = 0
        sf.lock()
        
        # ToDo: FIX RANGE CHECK
        # BG mapping 0x9800 --> 0x9BFF
        for memAddr in range(0x9800, 0x9C00): # 0x9C00, 0x9FFF
             
            tileID = memCntr.getMemValue(memAddr)
            tilePosition = tileID * 64;
                
            for y in range(bgStartPointY, bgStartPointY + 8):
                for x in range(bgStartPointX, bgStartPointX + 8):
                    
                    color = (255, 0, 255) # Error color (Pink)
                    
                    if( tileArray[tilePosition] == 1 ):
                        color = (255, 255, 255)
                    elif( tileArray[tilePosition] == 2 ):
                        color = (128, 128, 128)
                    elif( tileArray[tilePosition] == 3 ):
                        color = (192, 192, 192)
                    elif( tileArray[tilePosition] == 4 ):
                        color = (0, 0, 0)
                     
                    sf.set_at((x, y), color)    
                    tilePosition += 1
                     
            bgStartPointX += 8;
            # 64 (8 Tiles in a row)
            # 128 (16 Tiles in a row)
            if( bgStartPointX == 256 ):
                bgStartPointX = 0;
                bgStartPointY += 8;       
    
        sf.unlock()
        
    def drawTiles(self, sf, tileArray):
    
        tileStartPointX = 0;
        tileStartPointY = 0;
        countPixels = 0;
        sf.lock()
         
        while(countPixels < len(tileArray)):
            for y in range(tileStartPointY, tileStartPointY + 8):
                for x in range(tileStartPointX, tileStartPointX + 8):
                     
                    color = (255, 0, 255) # Error color (Pink)
    
                    if( tileArray[countPixels] == 1 ):
                        color = (255, 255, 255)
                    elif( tileArray[countPixels] == 2 ):
                        color = (128, 128, 128)
                    elif( tileArray[countPixels] == 3 ):
                        color = (192, 192, 192)
                    elif( tileArray[countPixels] == 4 ):
                        color = (0, 0, 0)
                     
                    sf.set_at((x, y), color)    
                    countPixels += 1;
             
            tileStartPointX += 8;
            # 64 (10 Tiles in a row)
            # 128 (20 Tiles in a row)
            if( tileStartPointX == 128 ):
                tileStartPointX = 0;
                tileStartPointY += 8;
    
        sf.unlock()
        
if __name__== "__main__":
    emulatorAggregator = emulatorAggregator()
    emulatorAggregator.main()