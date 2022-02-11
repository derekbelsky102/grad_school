def convertToInt(value):
   if value[0:2] == "0x":
      constant = int(value[2:], 16) 
   else:
      constant = int(value, 16)
   return constant


opcodes = { 
# Integer operations
"padd"        : 0,
"padd8"       : 1,
"padd16"      : 2,
"paddreg"     : 3,
"psub"        : 4,
"psub8"       : 5,
"psub16"      : 6,
"psubreg"     : 7,
"pmult"       : 8,
"pmult8"      : 9,
"pmult16"     : 10,
"pmultreg"    : 11,
"pdiv"        : 12,
"pdiv8"       : 13,
"pdiv16"      : 14,
"pdivreg"     : 15,

# Set Operations
"pset8"       : 33, #TODO Fix this!
"pset16lwr"   : 16,
"pset16upr"   : 17,
"pfset16lwr"  : 18,
"pfset16upr"  : 19,

# Float operations
"pfadd"       : 20,
"pfaddreg"    : 21,
"pfsub"       : 22,
"pfsubreg"    : 23,
"pfmult"      : 24,
"pfmultreg"   : 25,
"pfdiv"       : 26,
"pfdivreg"    : 27,

# Memory Access
"plw"         : 28,
"pflw"        : 29,
"psw"         : 30,
"pfsw"        : 31,

# Control Datapath
"pctl"        : 32

# 33-63 for future instructions like branch operations. 
}

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
"pset8 $0 $0 2 64",
"pset16lwr $62 0xAAAAAAAA 1",
"pset16upr $62 0xAAAAAAAA 1",
"pset16lwr $63 0xAAAAAAAA 1",
"pset16upr $63 0xAAAAAAAA 1",
"pctl 1",
"padd8 $0 $0 8 0",
"pctl 0",
"padd8 $0 $0 8 32"
]

count = 0
ctrl_en=0
for code in program:
   print("\n\n------ Running Instruction #",count,'------')
   print("------",code,'------\n\n')
   x = code.split()

   command=x[0]
   
   opcode=0
   result=0
   source1=0
   source2=0
   constant=0
   elements=0
   
   # Register Type
   ALU_Reg = ["padd", "psub", "pmult", "pdiv", "pfadd", "pfsub", "pfmult", "pfdiv", "paddreg", "psubreg", "pmultreg", "pdivreg", "pfaddreg", "pfsubreg", "pfmultreg", "pfdivreg"]
   if x[0] in ALU_Reg :
      opcode = opcodes[x[0]]
      if x[0] == "padd" or x[0] == "psub" or x[0] == "pmult" or x[0] == "pdiv":
         result = int(x[1][1:]) % 2**6 # strip $ and treat as only 6 bits. 
         source1 = int(x[2][1:]) % 2**6 # strip $ and treat as only 6 bits.
         source2 = int(x[3][1:]) % 2**6 # strip $ and treat as only 6 bits. 
      # TODO Add floating point. 
      elements = (int(x[4])-1) % 2**6
      
      code_32bit = opcode | result << 6 | source1 << 12 | source2 << 16 | elements << 24
      print("Hex Format: "+hex(code_32bit)) 
      print("Bin Format: "+bin(code_32bit)) 
   
   # 8 bit immediate type
   ALU_Const = ["padd8", "psub8", "pmult8", "pdiv8", "pset8"]
   if x[0] in ALU_Const :
      opcode = opcodes[x[0]]
      if x[0] == "padd8" or x[0] == "psub8" or x[0] == "pmult8" or x[0] == "pdiv8" or x[0] == "pset8":
         result = int(x[1][1:]) % 2**6 # strip $ and treat as only 6 bits. 
         source = int(x[2][1:]) % 2**6 # strip $ and treat as only 6 bits.
         # Handle constant as both hex and decimal
         constant = convertToInt(x[3]) % 2**8 # treat as only 8 bits. 
      # TODO Add floating point. 
      elements = (int(x[4])-1) % 2**6
      
      code_32bit = opcode | result << 6 | source1 << 12 | constant << 18 | elements << 26
      print("Hex Format: "+hex(code_32bit)) 
      print("Bin Format: "+bin(code_32bit)) 
   
   # 16 bit immediate type
   ALU_Ext_Const = ["padd16", "psub16", "pmult16", "pdiv16", "pset16lwr", "pset16upr", "pctl"]
   if x[0] in ALU_Ext_Const :
      opcode = opcodes[x[0]]
      if x[0] == "padd16" or x[0] == "psub16" or x[0] == "pmult16" or x[0] == "pdiv16" or x[0] == "pset16lwr":
         result = int(x[1][1:]) % 2**6 # strip $ and treat as only 6 bits. 
         # Handle constant as both hex and decimal
         constant = convertToInt(x[2]) % 2**16 # treat as only 16 bits. 
         elements = (int(x[3])-1) % 2**4
      elif x[0] == "pset16upr":
         result = int(x[1][1:]) % 2**6 # strip $ and treat as only 6 bits. 
         constant = int(int(x[2][2:], 16) / 2**16) # only upper 16 bits.
         elements = (int(x[3])-1) % 2**4
      elif x[0] == "pctl":
         result = int(x[1])
         ctrl_en = result
      # TODO Add floating point. 
      
      # Form 32bit code
      code_32bit = opcode | result << 6 | constant << 12 | elements << 26
      print("Hex Format: "+hex(code_32bit))
      print("Bin Format: "+bin(code_32bit)) 
   
   if ctrl_en == 1:
      control = ((registers[62] % 2**32) << 32) | (registers[63] % 2**32)
      ctrl_bits = list(map(int, list(bin(control)[2:])[::-1]))
      print(ctrl_bits)
      elements=len(ctrl_bits)-1
   # Do operation
   for i in range(0, elements+1):
      if ctrl_en == 0 or (ctrl_en == 1 and ctrl_bits[i] == 1):
         index = result+i % 2**6 # Make sure index does not overflow
         if x[0] == "padd" or x[0] == "pfadd": 
            registers[index] = registers[source1+i] + registers[source2+i]
         elif x[0] == "psub" or x[0] == "pfsub":
            registers[index] = registers[source1+i] - registers[source2+i]
         elif x[0] == "pmult" or x[0] == "pfmult":
            registers[index] = registers[source1+i] * registers[source2+i]
         elif x[0] == "pdiv" or x[0] == "pfdiv":
            registers[index] = int(registers[source1+i] / registers[source2+i])
         elif x[0] == "padd8" or x[0] == "pfadd8": 
            registers[index] = registers[source+i] + constant
         elif x[0] == "psub8" or x[0] == "pfsub8":
            registers[index] = registers[source+i] - constant
         elif x[0] == "pmult8" or x[0] == "pfmult8":
            registers[index] = registers[source+i] * constant
         elif x[0] == "pdiv8" or x[0] == "pfdiv8":
            registers[index] = int(registers[source+i] / constant)
         elif x[0] == "padd16": 
            registers[index] = registers[result+i] + constant
         elif x[0] == "psub16":
            registers[index] = registers[result+i] - constant
         elif x[0] == "pmult16":
            registers[index] = registers[result+i] * constant
         elif x[0] == "pdiv16":
            registers[index] = int(registers[result+i] / constant)
         elif x[0] == "pset8":
            registers[index] = constant
         elif x[0] == "pset16lwr":
            registers[index] = constant
         elif x[0] == "pset16upr":
            registers[index] = (constant << 16) + registers[result+i] % 2**16
         elif x[0] == "paddreg" or x[0] == "pfaddreg": 
            registers[index] = registers[result+i] + registers[source2]
         elif x[0] == "psubreg" or x[0] == "pfsubreg":
            registers[index] = registers[result+i] - registers[source2]
         elif x[0] == "pmultreg" or x[0] == "pfmultreg":
            registers[index] = registers[result+i] * registers[source2]
         elif x[0] == "pdivreg" or x[0] == "pfdivreg":
            registers[index] = int(registers[result+i] / registers[source2])
   print("Registers: ",registers)
   count = count + 1


