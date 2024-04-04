import re
import os
import numpy as np
# Simplified RISC-V instruction set

def parse_riscv_assembly(file_path):
    instructions = []
    ctr=0
    with open(file_path, 'r') as file:
        for line in file:
            ctr+=1
            # Skip comments and empty lines
            if line.startswith('.') or line.startswith(';') or line.strip() == '':
                continue
            # Use regex to parse instructions
            match = re.match(r'(\w+)\s+(.*)', line.strip())
            if match:
                opcode, operands = match.groups()
                instructions.append((opcode, operands))
    #print(instructions)
    return instructions


def create_dictionary(instructions):
    numbers= ['1','2','3','4','5','6','7','8','9']
    registers=dict()

    for i in range(0,len(instructions)):
        a= instructions[i][1].split()
        #print(a) splits reg into its two registers along with the comma
        temp=[]
        for j in a:
            
            s=j.find("x") #s is the index
            q=j[s:s+2]
            if q not in numbers: #to prevent the integers in addi
                temp.append(q)
           
        registers[i]=instructions[i][0],temp

        if registers[i][0] in ["add","addi","sub","andi","and","xori","xor","or"]:
            dest=registers[i][1][0]

        elif registers[i][0] in ["lb","lbu","li","la","lw"]:
            dest=registers[i][1][1]  

        elif registers[i][0] in ["sw","sb"]:
            dest=registers[i][1][0]

        else:
            print("instruction not found")

        registers[i]=dest,instructions[i][0], temp
    print("The dictionary of line numbers and their list of registers looks like this: \n", registers,"\n")
    #print("number of lines in the program is: ", len(registers),"\n")
    return registers


def data_hazard_detection(arr,registers):
    iterations=len(arr)
    hazard=[]
    for i in range(0,iterations):
        arr[i]-=1
        for j in range(0,i):
            arr[j]-=1
        #print(arr) PRINTS THE COUNTER ARRAY
        for q in range(0,i):
            for k in registers[i][2]:
                if k==registers[q][0]:   
                    if registers[q][1] in ["lb","lbu","li","la","lw"]:
                        if arr[i]-arr[q]<2:
                            if [i,q] not in hazard:
                                hazard.append([i,q])
                    else:
                        if arr[i]-arr[q]<4:
                            if [i,q] not in hazard:
                                hazard.append([i,q])
    return hazard

def display_hazards(hazard,instructions):
    for i in hazard:
        m=i[0]
        n=i[1]
        print(m,":",instructions[m],"->",n,":",instructions[n]) 
    
relative_path = 'ripes_test.s'

instructions=parse_riscv_assembly(relative_path)

registers=create_dictionary(instructions)

arr=np.repeat(6,len(instructions))

hazard=data_hazard_detection(arr,registers)

display_hazards(hazard,instructions)

