potentialHazards = ["NA","NA"]

file="program1.asm"
spaces=""
insertStall=0
count=1
previousLines=0
previousInstruction="NA"
solution_type=input("Enter Solution Type 1, 2 or 3 ")
with open(file, 'r') as program:
    for code in program:
      
      # Not a huge fan of this solution but it split args by spaces and commas and should be robust. 
      a = [a.strip() for a in code.split(',')]
      list1=a[0].split()
      del a[0]
      list2=a
      x=list1+list2

      if x[0] == "add" or x[0] == "sub":
         
         result =  (x[1][1:])
         source1 = (x[2][1:])
         source2 = (x[3][1:])
      elif x[0] == "lw":
         result =  (x[1][1:])
         startIndex=x[2].index("$")+1
         endIndex=x[2].index(")")
         source1 = (x[2][startIndex:endIndex])
         source2=""
      elif x[0] == "sw":
         result=""
         source1 =  (x[1][1:])
         startIndex=x[2].index("$")+1
         endIndex=x[2].index(")")
         source2 = (x[2][startIndex:endIndex])
      else:
         result=""
         source1=""
         source2=""
         print("Invalid command")
      
      source1Flag=0
      if source1 in potentialHazards or source2 in potentialHazards:
         if source1 == potentialHazards[1] or source2 == potentialHazards[1]:
            if solution_type=='1':
               if source1 in potentialHazards:
                  print("Data dependency on line "+str(count)+" with register "+source1+" from line "+str(count-1))
               if source2 in potentialHazards:
                  print("Data dependency on line "+str(count)+" with register "+source2+" from line "+str(count-1))
            elif solution_type=='2':
               print(spaces+"F S S D X M W")
               spaces=spaces+"    "
               # There can be no dependency after two stalls
               potentialHazards[0]="NA"
               potentialHazards[1]="NA"
         elif source1 == potentialHazards[0] or source2 == potentialHazards[0]:
            if solution_type=='1':
               if source1 in potentialHazards:
                  print("Data dependency on line "+str(count)+" with register "+source1+" from line "+str(count-2))
               if source2 in potentialHazards:
                  print("Data dependency on line "+str(count)+" with register "+source2+" from line "+str(count-2))
            elif solution_type=='2':
               print(spaces+"F S D X M W")
               spaces=spaces+"  "
               # With a single stall added, this result can't be dependency anymore. 
               del potentialHazards[0]
               potentialHazards.append("NA")
         insertStall=1
      
      potentialHazards.append(result)
      del potentialHazards[0] 
      # Only Case we can see a stall... I think...
      if solution_type == '3' and previousInstruction == "lw" and (source1 == potentialHazards[1] or source2 == potentialHazards[1]):
         del potentialHazards[0]
         potentialHazards.append("NA")
         print(spaces+"F S D X M W")
         spaces=spaces+"  "
      elif (solution_type=='2' and insertStall == 0) or solution_type == '3':
         print(spaces+"F D X M W")

      spaces=spaces+"  "  
      insertStall=0
      count = count + 1
      previousInstruction = x[0]
   


