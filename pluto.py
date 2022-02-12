import struct

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
   def __init__(self, arg1, opcode, type, func):
      self.arg1 =  arg1
      self.opcode = opcode
      self.type = type
      self.func = func

instructions = {}
# Register Arithmetic operations
instructions[0]  = Instruction("padd",       0,   'register', 0)
instructions[1]  = Instruction("psub",       0,   'register', 1)
instructions[2]  = Instruction("pmult",      0,   'register', 2)
instructions[3]  = Instruction("pdiv",       0,   'register', 3)
instructions[4]  = Instruction("paddreg",    1,   'register', 0)
instructions[5]  = Instruction("psubreg",    1,   'register', 1)
instructions[6]  = Instruction("pmultreg",   1,   'register', 2)
instructions[7]  = Instruction("pdivreg",    1,   'register', 3)
# Constant Arithmetic operations
instructions[8]  = Instruction("padd8",      2,   '8bitImm',  0)
instructions[9]  = Instruction("padd16",     3,   '16bitImm', 0)
instructions[10] = Instruction("psub8",      4,   '8bitImm',  0)
instructions[11] = Instruction("psub16",     5,   '16bitImm', 0)
instructions[12] = Instruction("pmult8",     6,   '8bitImm',  0)
instructions[13] = Instruction("pmult16",    7,   '16bitImm', 0)
instructions[14] = Instruction("pdiv8",      8,   '8bitImm',  0)
instructions[15] = Instruction("pdiv16",     9,   '16bitImm', 0)
# Set Operations
instructions[16] = Instruction("pset8",      10,  '8bitImm',  0)
instructions[17] = Instruction("pset16lwr",  11,  '16bitImm', 0)
instructions[18] = Instruction("pset16upr",  12,  '16bitImm', 0)
# Memory Access
instructions[19] = Instruction("plw",        13,  '8bitImm',  0)
instructions[20] = Instruction("psw",        14,  '8bitImm',  0)
# Control
instructions[21] = Instruction("pctl",       15,  '16bitImm', 0)
# Bitwise Operations
instructions[22] = Instruction("pshiftl",    16,  '8bitImm',  0)
instructions[23] = Instruction("pshiftr",    17,  '8bitImm',  0)
instructions[24] = Instruction("pand16lwr",  18,  '16bitImm', 0)
instructions[25] = Instruction("pand16upr",  19,  '16bitImm', 0)
instructions[26] = Instruction("por16lwr",   20,  '16bitImm', 0)
instructions[27] = Instruction("por16upr",   21,  '16bitImm', 0)
instructions[26] = Instruction("pnot16lwr",  22,  '16bitImm', 0)
instructions[27] = Instruction("pnot16upr",  23,  '16bitImm', 0)

# 24-31 for future instructions like branch operations. 
# opcode is currently 5 bits. Exanding it to 6 bits will give 64 instructions, but
# 1 bit for elements will need to be dropped which would decrease number of parellel operations
# by a factor of 2. 

# Register section
registers = [0] * 64

# Data section
data = [0] * 2048

# To set all 64 register to 0-255, it takes one instructions
# To set all 64 register to255-2^16-1, it takes two instructions
# To set all 64 register to 2^16-1 - 2^32-1, it takes four instructions

program=[
"pset8 $0 $0 2 64",
"pset16lwr $0 2048 32",
"pset16lwr $32 2048 32",
"padd $0 $0 $0 64",
"pmult $0 $0 $0 64",
"pset16lwr $0 500077 32",
"pset16upr $0 500077 32",
"pset16lwr $32 500077 32",
"pset16upr $32 500077 32",
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
   opcode = currentInstruction.opcode & 0x1F # mask 5 lower bits 
   
   # Register Type
   if currentInstruction.type == 'register':
      result = int(x[1][1:]) & 0x3F  # strip $ and mask 6 lower bits
      source1 = int(x[2][1:]) & 0x3F # strip $ and mask 6 lower bits
      source2 = int(x[3][1:]) & 0x3F # strip $ and mask 6 lower bits
      elements = (int(x[4])-1) & 0x3F # mask 6 lower bits
      
      code_32bit = opcode | result << 6 | source1 << 12 | source2 << 16 | elements << 24 | currentInstruction.func << 30
      print("Hex Format: "+hex(code_32bit)) 
      print("Bin Format: "+bin(code_32bit)) 
   
   # 8 bit immediate type
   if currentInstruction.type == '8bitImm':
      result = int(x[1][1:]) & 0x3F 
      source = int(x[2][1:]) & 0x3F 
      # Handle constant as both hex and decimal
      constant = convertToInt(x[3]) & 0xFF 
      elements = (int(x[4])-1) & 0x3F 
      
      code_32bit = opcode | result << 6 | source1 << 12 | constant << 18 | elements << 26
      print("Hex Format: "+hex(code_32bit)) 
      print("Bin Format: "+bin(code_32bit)) 
   
   # 16 bit immediate type
   if currentInstruction.type == '16bitImm':
      if currentInstruction.arg1 == "pctl":
         result = int(x[1])
         ctrl_en = result
      else:
         result = int(x[1][1:]) & 0x3F
         elements = (int(x[3])-1) & 0x1F
         # Handle constant as both hex and decimal
         constant = convertToInt(x[2])
      
      # Masking 16 lower bits
      if currentInstruction.arg1 == "pset16lwr":
         constant = constant & 0x0000FFFF
         print(constant)

      # Masking 16 upper bits
      if currentInstruction.arg1 == "pset16upr":
         constant = constant & 0xFFFF0000

      # TODO Add floating point. 
      
      # Form 32bit code
      code_32bit = opcode | result << 6 | constant << 12 | elements << 26
      print("Hex Format: "+hex(code_32bit))
      print("Bin Format: "+bin(code_32bit)) 
   
   if ctrl_en == 1:
      control = ((registers[62] & 0xFFFFFFFF ) << 32) | (registers[63] & 0xFFFFFFFF)
      ctrl_bits = list(map(int, list(bin(control)[2:])[::-1]))
      elements=len(ctrl_bits)-1
   # Do operation
   for i in range(0, elements+1):
      if ctrl_en == 0 or (ctrl_en == 1 and ctrl_bits[i] == 1):
         index = result+i % 2**6 # Make sure index does not overflow
         if currentInstruction.arg1 == "padd": 
            registers[index] = registers[source1+i] + registers[source2+i]
         elif currentInstruction.arg1 == "psub":
            registers[index] = registers[source1+i] - registers[source2+i]
         elif currentInstruction.arg1 == "pmult":
            registers[index] = registers[source1+i] * registers[source2+i]
         elif currentInstruction.arg1 == "pdiv":
            registers[index] = int(registers[source1+i] / registers[source2+i])
         elif currentInstruction.arg1 == "padd8":
            registers[index] = registers[source+i] + constant
         elif currentInstruction.arg1 == "psub8":
            registers[index] = registers[source+i] - constant
         elif currentInstruction.arg1 == "pmult8":
            registers[index] = registers[source+i] * constant
         elif currentInstruction.arg1 == "pdiv8":
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
            registers[index] = constant + (registers[result+i]  & 0x0000FFFF)
         elif currentInstruction.arg1 == "paddreg": 
            registers[index] = registers[result+i] + registers[source2]
         elif currentInstruction.arg1 == "psubreg":
            registers[index] = registers[result+i] - registers[source2]
         elif currentInstruction.arg1 == "pmultreg":
            registers[index] = registers[result+i] * registers[source2]
         elif currentInstruction.arg1 == "pdivreg":
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


