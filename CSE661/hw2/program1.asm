pset8 $0 $0 2 64
pset16lwr $0 2048 32
pset16lwr $32 2048 32
padd $0 $0 $0 64
pmult $0 $0 $0 64
pset16lwr $0 500077 32
pset16upr $0 500077 32
pset16lwr $32 500077 32
pset16upr $32 500077 32
pset8 $63 $0 0 1
psw $0 $63 0 63
pset8 $0 $0 2 64
pset16lwr $62 0xAAAAAAAA 1
pset16upr $62 0xAAAAAAAA 1
pset16lwr $63 0xAAAAAAAA 1
pset16upr $63 0xAAAAAAAA 1
pctl 1
padd8 $0 $0 8 0
pctl 0
padd8 $0 $0 8 32
pset8 $63 $0 0 1
psw $0 $63 63 62
plw $0 $63 0 62
padd8 $62 $0 0 2
pand16lwr $0 0x00008000 32
pand16upr $0 0x00008000 32
por16lwr $0 0x0007A16D 32
por16upr $0 0x0007A16D 32
pnot $0 32