
''' 


    x = 0x08
    print(hex(x))
    x = x & ~(1 << 3)
    #x = x | (1 << 0)
    print(hex(x))
    return
    
Vielleicht mal hilfreich :)

# DBG
for i in range(0, os.path.getsize(os.getcwd()+'\..\Resource\Bootloader.bin')):    
   print(hex(bBootloader[i]));

# Init PC to 0x00
registers[RegID.PC.value] = 0xFF;
registers[RegID.PC.value +1] = 0xFF;

print(base64.b16encode(mybytes))
print(int.from_bytes(bytearray([registers[RegID.PC.value], registers[RegID.PC.value+1]]), byteorder='big', signed=False));
print(int(0xFFFF))

print(pack('hl', registers[RegID.PC.value], registers[RegID.PC.value+1]));
mybytes = bytearray([registers[RegID.PC.value], registers[RegID.PC.value+1]])

print(getPC());
incrementPC(1);
print(getPC());
,
                                    bBootloader[pc+1], 
                                    bBootloader[pc+2],
                                    registers,
                                    register16Bit
def getPC():
    return int.from_bytes(
        bytearray([registers[RegID.PC.value], registers[RegID.PC.value+1]]),
        byteorder='big', signed=False);

def incrementPC(value):
    pc = getPC();

    if (pc + value) > 0xFFFF:
        pc = 0x0000;
        pc += value;
    
    mybytes = pc.to_bytes(2, byteorder='big', signed=False)
    registers[RegID.PC.value] = mybytes[0]
    registers[RegID.PC.value+1]  = mybytes[1]
'''