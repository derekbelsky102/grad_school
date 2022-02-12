def convertToInt(value):
   if value[0:2] == "0x":
      constant = int(value[2:], 16) 
   else:
      constant = int(value, 10)
   return constant

def searchInstruction(string):
   for i in range(0, len(instructions)):
      if string == instructions[i].arg1:
         return i

class Instruction:
   def __init__(self, arg1, opcode, type, intOrFloat):
      self.arg1 =  arg1
      self.opcode = opcode
      self.type = type
      self.intOrFloat = intOrFloat

instructions = {}
# Integer operations
instructions[0]  = Instruction("padd",       0,   'register',  'int')
instructions[1]  = Instruction("padd8",      1,   '8bitImm',   'int')
instructions[2]  = Instruction("padd16",     2,   '16bitImm',  'int')
instructions[3]  = Instruction("paddreg",    3,   'register',  'int')
instructions[4]  = Instruction("psub",       4,   'register',  'int')
instructions[5]  = Instruction("psub8",      5,   '8bitImm',   'int')
instructions[6]  = Instruction("psub16",     6,   '16bitImm',  'int')
instructions[7]  = Instruction("psubreg",    7,   'register',  'int')
instructions[8]  = Instruction("pmult",      8,   'register',  'int')
instructions[9]  = Instruction("pmult8",     9,   '8bitImm',   'int')
instructions[10] = Instruction("pmult16",    10,  '16bitImm',  'int')
instructions[11] = Instruction("pmultreg",   11,  'register',  'int')
instructions[12] = Instruction("pdiv",       12,  'register',  'int')
instructions[13] = Instruction("pdiv8",      13,  '8bitImm',   'int')
instructions[14] = Instruction("pdiv16",     14,  '16bitImm',  'int')
instructions[15] = Instruction("pdivreg",    15,  'register',  'int')
# Set Operations
instructions[16] = Instruction("pset8",      16,  '8bitImm',   'int')
instructions[17] = Instruction("pset16lwr",  17,  '16bitImm',  'int')
instructions[18] = Instruction("pset16upr",  18,  '16bitImm',  'int')
instructions[19] = Instruction("pfset16lwr", 19,  '16bitImm',  'float')
instructions[20] = Instruction("pfset16upr", 20,  '16bitImm',  'float')
# Float operations
instructions[21] = Instruction("pfadd",     21,  'register',  'float')
instructions[22] = Instruction("pfaddreg",  22,  'register',  'float')
instructions[23] = Instruction("pfsub",     23,  'register',  'float')
instructions[24] = Instruction("pfsubreg",  24,  'register',  'float')
instructions[25] = Instruction("pfmult",    25,  'register',  'float')
instructions[26] = Instruction("pfmultreg", 26,  'register',  'float')
instructions[27] = Instruction("pfdiv",     27,  'register',  'float')
instructions[28] = Instruction("pfdivreg",  28,  'register',  'float')
# Memory Access
instructions[29] = Instruction("plw",       29,  '8bitImm',   'int')
instructions[30] = Instruction("psw",       30,  '8bitImm',   'int')
instructions[31] = Instruction("pflw",      31,  '8bitImm',   'float')
instructions[32] = Instruction("pfsw",      32,  '8bitImm',   'float')
# Control                                                     
instructions[33] = Instruction("pctl",      33,  '16bitImm',  'none')
# 34-63 for future instructions like branch operations. 

# Register section
registers = [0] * 64

# Data section
data = [0] * 2048

# To set all 64 register to 0-255, it takes one instructions
# To set all 64 register to255-2^16-1, it takes four instructions
# To set all 64 register to 2^16-1 - 2^32-1, it takes eight instructions

program=[
"pset8 $0 $0 2 64",
"pset16lwr $0 2048 16",
"pset16lwr $16 2048 16",
"pset16lwr $32 2048 16",
"pset16lwr $48 2048 16",
"padd $0 $0 $0 64",
"pmult $0 $0 $0 64",
"pset16lwr $0 500077 16",
"pset16upr $0 500077 16",
"pset16lwr $16 500077 16",
"pset16upr $16 500077 16",
"pset16lwr $32 500077 16",
"pset16upr $32 500077 16",
"pset16lwr $48 500077 16",
"pset16upr $48 500077 16",
"pset8 $63 $0 0 1",
"psw $0 $63 0 63",
"pset8 $0 $0 2 64",
"pset16lwr $62 0xAAAAAAAA 1",
"pset16upr $62 0xAAAAAAAA 1",
"pset16lwr $63 0xAAAAAAAA 1",
"pset16upr $63 0xAAAAAAAA 1",
"pctl 1",
"padd8 $0 $0 8 0",
"pctl 0",
"padd8 $0 $0 8 32",
"pset8 $63 $0 0 1",
"psw $0 $63 63 62",
"plw $0 $63 0 62"
]

mode=int(input("Enter mode. \n 1: Run All \n 2: Step Through\n"))

count = 0
ctrl_en=0
for code in program:
   # This printing scheme could be cleaner. If there is time this can be improved. 
   print("\n---------------------- Running Instruction #",count,"---------------------------")
   print("----------------------",code,'-'*(50-int(len(code)))+'-'*(len(str(count))-1),'\n')
   x = code.split()
   
   result=0
   source1=0
   source2=0
   constant=0
   elements=0
   
   currentInstruction = instructions[searchInstruction(x[0])]
   
   # Register Type
   if currentInstruction.type == 'register':
      if currentInstruction.intOrFloat == 'int':
         result = int(x[1][1:]) % 2**6 # strip $ and treat as only 6 bits. 
         source1 = int(x[2][1:]) % 2**6 # strip $ and treat as only 6 bits.
         source2 = int(x[3][1:]) % 2**6 # strip $ and treat as only 6 bits. 
      # TODO Add floating point. 
      elements = (int(x[4])-1) % 2**6
      
      code_32bit = currentInstruction.opcode | result << 6 | source1 << 12 | source2 << 16 | elements << 24
      print("Hex Format: "+hex(code_32bit)) 
      print("Bin Format: "+bin(code_32bit)) 
   
   # 8 bit immediate type
   if currentInstruction.type == '8bitImm':
      if currentInstruction.intOrFloat == 'int':
         result = int(x[1][1:]) % 2**6 # strip $ and treat as only 6 bits. 
         source = int(x[2][1:]) % 2**6 # strip $ and treat as only 6 bits.
         # Handle constant as both hex and decimal
         constant = convertToInt(x[3]) % 2**8 # treat as only 8 bits. 
      # TODO Add floating point. 
      elements = (int(x[4])-1) % 2**6
      
      code_32bit = currentInstruction.opcode | result << 6 | source1 << 12 | constant << 18 | elements << 26
      print("Hex Format: "+hex(code_32bit)) 
      print("Bin Format: "+bin(code_32bit)) 
   
   # 16 bit immediate type
   if currentInstruction.type == '16bitImm':
      if currentInstruction.intOrFloat == 'int':
         result = int(x[1][1:]) % 2**6 # strip $ and treat as only 6 bits. 
         # Handle constant as both hex and decimal
         constant = convertToInt(x[2]) % 2**16 # treat as only 16 bits. 
         elements = (int(x[3])-1) % 2**4
      elif currentInstruction.intOrFloat == 'none':
         result = int(x[1])
         ctrl_en = result

      if currentInstruction.arg1 == "pset16upr":
         constant = int(convertToInt(x[2]) / 2**16) # only upper 16 bits.

      # TODO Add floating point. 
      
      # Form 32bit code
      code_32bit = currentInstruction.opcode | result << 6 | constant << 12 | elements << 26
      print("Hex Format: "+hex(code_32bit))
      print("Bin Format: "+bin(code_32bit)) 
   
   if ctrl_en == 1:
      control = ((registers[62] % 2**32) << 32) | (registers[63] % 2**32)
      ctrl_bits = list(map(int, list(bin(control)[2:])[::-1]))
      elements=len(ctrl_bits)-1
   # Do operation
   for i in range(0, elements+1):
      if ctrl_en == 0 or (ctrl_en == 1 and ctrl_bits[i] == 1):
         index = result+i % 2**6 # Make sure index does not overflow
         if currentInstruction.arg1 == "padd" or currentInstruction.arg1 == "pfadd": 
            registers[index] = registers[source1+i] + registers[source2+i]
         elif currentInstruction.arg1 == "psub" or currentInstruction.arg1 == "pfsub":
            registers[index] = registers[source1+i] - registers[source2+i]
         elif currentInstruction.arg1 == "pmult" or currentInstruction.arg1 == "pfmult":
            registers[index] = registers[source1+i] * registers[source2+i]
         elif currentInstruction.arg1 == "pdiv" or currentInstruction.arg1 == "pfdiv":
            registers[index] = int(registers[source1+i] / registers[source2+i])
         elif currentInstruction.arg1 == "padd8" or currentInstruction.arg1 == "pfadd8": 
            registers[index] = registers[source+i] + constant
         elif currentInstruction.arg1 == "psub8" or currentInstruction.arg1 == "pfsub8":
            registers[index] = registers[source+i] - constant
         elif currentInstruction.arg1 == "pmult8" or currentInstruction.arg1 == "pfmult8":
            registers[index] = registers[source+i] * constant
         elif currentInstruction.arg1 == "pdiv8" or currentInstruction.arg1 == "pfdiv8":
            registers[index] = int(registers[source+i] / constant)
         elif currentInstruction.arg1 == "padd16": 
            registers[index] = registers[result+i] + constant
         elif currentInstruction.arg1 == "psub16":
            registers[index] = registers[result+i] - constant
         elif currentInstruction.arg1 == "pmult16":
            registers[index] = registers[result+i] * constant
         elif currentInstruction.arg1 == "pdiv16":
            registers[index] = int(registers[result+i] / constant)
         elif currentInstruction.arg1 == "pset8":
            registers[index] = constant
         elif currentInstruction.arg1 == "pset16lwr":
            registers[index] = constant
         elif currentInstruction.arg1 == "pset16upr":
            registers[index] = (constant << 16) + registers[result+i] % 2**16
         elif currentInstruction.arg1 == "paddreg" or currentInstruction.arg1 == "pfaddreg": 
            registers[index] = registers[result+i] + registers[source2]
         elif currentInstruction.arg1 == "psubreg" or currentInstruction.arg1 == "pfsubreg":
            registers[index] = registers[result+i] - registers[source2]
         elif currentInstruction.arg1 == "pmultreg" or currentInstruction.arg1 == "pfmultreg":
            registers[index] = registers[result+i] * registers[source2]
         elif currentInstruction.arg1 == "pdivreg" or currentInstruction.arg1 == "pfdivreg":
            registers[index] = int(registers[result+i] / registers[source2])
         elif currentInstruction.arg1 == "plw":
            registers[index] = data[registers[source]+constant+i]
         elif currentInstruction.arg1 == "psw":
            data[registers[source]+constant+i] = registers[index]
   print("\nRegisters: ",registers)
   
   print("\nData: ",data[0:256])
   count = count + 1
   if mode == 2:
      input("\nHit Enter for Next Instruction\n")


