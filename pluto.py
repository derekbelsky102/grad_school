opcodes = { 
# Integer operations
"padd"        : 0,
"paddc"       : 1,
"paddce"      : 2,
"paddreg"     : 3,

"psub"        : 5,
"psubc"       : 6,
"psubce"      : 7,
"psubreg"     : 8,

"pmult"       : 10,
"pmultc"      : 11,
"pmultce"     : 12,
"pmultreg"    : 13,

"pdiv"        : 15,
"pdivc"       : 16,
"pdivce"      : 17,
"pdivreg"     : 18,

# Float operations
"pfadd"       : 20,
"pfaddc"      : 21,
"pfaddce"     : 22,
"pfaddreg"    : 23,

"pfsub"       : 25,
"pfsubc"      : 26,
"pfsubce"     : 27,
"pfsubreg"    : 28,

"pfmult"      : 30,
"pfmultc"     : 31,
"pfmultce"    : 32,
"pfmultreg"   : 33,

"pfdiv"       : 35,
"pfdivc"      : 36,
"pfdivce"     : 37,
"pfdivreg"    : 38,

# Memory Access
"plw"         : 40,
"pflw"        : 41,
"psw"         : 42,
"pfsw"        : 43

}

# Register section
registers = [0] * 64

# Data section
data = [0] * 2048

program=["paddce $0 2 64", "pmultce $0 2 32", "pmultce $0 2 16", "pmultce $0 2 8", "pmultce $0 2 4", "pmultce $0 2 2", "pmultce $0 2 1"]

count = 0
for code in program:
   print("\n--------------------Running Instruction #",count,'----------------------------------\n')
   x = code.split()

   command=x[0]

   ALU_Reg = ["padd", "psub", "pmult", "pdiv", "pfadd", "pfsub", "pfmult", "pfdiv"]
   if x[0] in ALU_Reg :
      opcode = opcodes[x[0]]
      result = int(x[1][1:]) << 6
      source1 = int(x[2][1:]) << 12
      source2 = int(x[3][1:]) << 18
      elements = int(x[4]) << 24
      print("Hex Format: "+hex(opcode | result | source1 | source2 | elements)) 
      print("Bin Format: "+bin(opcode | result | source1 | source2 | elements)) 
      
   ALU_Const = ["paddc", "psubc", "pmultc", "pdivc", "pfaddc", "pfsubc", "pfmultc", "pfdivc"]
   if x[0] in ALU_Const :
      opcode = opcodes[x[0]]
      result = int(x[1][1:]) << 6
      source1 = int(x[2][1:]) << 12
      constant = int(x[3]) << 18
      elements = int(x[4]) << 26
      print("Hex Format: "+hex(opcode | result | source1 | constant | elements)) 
      print("Bin Format: "+bin(opcode | result | source1 | constant | elements)) 
      
   ALU_Ext_Const = ["paddce", "psubce", "pmultce", "pdivce", "pfaddce", "pfsubce", "pfmultce", "pfdivce"]
   if x[0] in ALU_Ext_Const :
      opcode = opcodes[x[0]]
      
      if x[0] == "paddce" or x[0] == "psubce" or x[0] == "pmultce" or x[0] == "pdivce":
         result = int(x[1][1:]) % 2**6 # strip $ and treat as only 6 bits. 
         constant = int(x[2]) % 2**14 # treat as only 14 bits. 
      # TODO Add floating point. 
      elements = (int(x[3])-1) % 2**6
      
      # Form 32bit code
      code_32bit = opcode | result << 6 | constant << 12 | elements << 26
      print("Hex Format: "+hex(code_32bit))
      print("Bin Format: "+bin(code_32bit)) 
      
      # Move constant into registers
      for i in range(0, elements):
         if x[0] == "paddce" or x[0] == "pfaddce": 
            registers[result+i] = registers[result+i] + constant
         elif x[0] == "psubce" or x[0] == "pfsubce":
            registers[result+i] = registers[result+i] - constant
         elif x[0] == "pmultce" or x[0] == "pfmultce":
            registers[result+i] = registers[result+i] * constant
         elif x[0] == "pdivce" or x[0] == "pfdivce":
            registers[result+i] = int(registers[result+i] / constant)

   print()
   ALU_Reg_Source2_Const = ["paddreg", "psubreg", "pmultreg", "pdivreg", "pfaddreg", "pfsubreg", "pfmultreg", "pfdivreg"]
   if x[0] in ALU_Reg_Source2_Const :
      opcode = opcodes[x[0]]
      result = int(x[1][1:]) << 6
      source1 = int(x[2][1:]) << 12
      source2_constant = int(x[3][1:]) << 18
      elements = int(x[4]) << 24
      print("Hex Format: "+hex(opcode | result | source1 | source2_constant | elements)) 
      print("Bin Format: "+hex(opcode | result | source1 | source2_constant | elements)) 
      
   print("Registers: ",registers)
   count = count + 1


