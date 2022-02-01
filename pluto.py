line="pfsub $0 $1 $2 4"

x = line.split()

command=x[0]

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

ALU_Reg = ["padd", "psub", "pmult", "pdiv", "pfadd", "pfsub", "pfmult", "pfdiv"]
if x[0] in ALU_Reg :
   opcode = opcodes[x[0]]
   result = int(x[1][1]) << 6
   source1 = int(x[2][1]) << 12
   source2 = int(x[3][1]) << 18
   elements = int(x[4]) << 24
   print("Hex Format: "+hex(opcode | result | source1 | source2 | elements)) 
   print("Bin Format: "+bin(opcode | result | source1 | source2 | elements)) 
   
ALU_Const = ["paddc", "psubc", "pmultc", "pdivc", "pfaddc", "pfsubc", "pfmultc", "pfdivc"]
if x[0] in ALU_Const :
   opcode = opcodes[x[0]]
   result = int(x[1][1]) << 6
   source1 = int(x[2][1]) << 12
   constant = int(x[3]) << 18
   elements = int(x[4]) << 26
   print("Hex Format: "+hex(opcode | result | source1 | constant | elements)) 
   print("Bin Format: "+bin(opcode | result | source1 | constant | elements)) 
   
ALU_Ext_Const = ["paddce", "psubce", "pmultce", "pdivce", "pfaddce", "pfsubce", "pfmultce", "pfdivce"]
if x[0] in ALU_Ext_Const :
   opcode = opcodes[x[0]]
   result = int(x[1][1]) << 6
   constant = int(x[2][1]) << 12
   elements = int(x[4]) << 26
   print("Hex Format: "+hex(opcode | result | constant | elements)) 
   print("Bin Format: "+bin(opcode | result | constant | elements)) 
   
ALU_Reg_Source2_Const = ["paddreg", "psubreg", "pmultreg", "pdivreg", "pfaddreg", "pfsubreg", "pfmultreg", "pfdivreg"]
if x[0] in ALU_Reg_Source2_Const :
   opcode = opcodes[x[0]]
   result = int(x[1][1]) << 6
   source1 = int(x[2][1]) << 12
   source2_constant = int(x[3][1]) << 18
   elements = int(x[4]) << 24
   print("Hex Format: "+hex(opcode | result | source1 | source2_constant | elements)) 
   print("Bin Format: "+hex(opcode | result | source1 | source2_constant | elements)) 

