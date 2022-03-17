potentialHazards = ["NA","NA"]

file="program1.asm"
spaces=""
count=1
with open(file, 'r') as program:
    for code in program:
      
      x = code.split()
      
      result =  (x[1][1:])
      source1 = (x[2][1:])
      source2 = (x[3][1:])
      if source1 in potentialHazards:
         print("Data dependency on line ",count, "Register ",source1)
      if source2 in potentialHazards:
         print("Data dependency on line ",count, "Register ",source2)
      potentialHazards.append(result)
      del potentialHazards[0] 
      spaces=spaces+"    "  
      count = count + 1
       


