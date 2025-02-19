from instructions import InstructionSet
from registers import RegisterMap

# For Handling Immediate Values
def label(imm,pc):
    if imm in labels:
        imm= int(labels[imm])
        return (imm- pc)/2
    else:
        return int(imm)/2

def immManager(imm, bitcount):
    imm= int(imm)
    if imm < 0:
        imm = (1 << bitcount) + imm 
    imm= format(imm & 2**bitcount-1, f'0{bitcount}b')
    return imm

# -------------------------------

# Instruction type encoding
def Rtype(inst):
    instruction= inst[0]
    regs= inst[1].split(",")

    funct7 = InstructionSet[instruction]["funct7"]
    funct3 = InstructionSet[instruction]["funct3"]
    opcode = InstructionSet[instruction]["opcode"]

    try: 
        rd= RegisterMap[regs[0]]
        rs2= RegisterMap[regs[1]]
        rs1= RegisterMap[regs[2]]
    except KeyError as e:
        raise SyntaxError(f"Invalid register name {e}")

    Binary= funct7+ rs1 + rs2 + funct3 + rd + opcode + "\n"

    return Binary

def Itype(inst, pc):
    instruction= inst[0]

    funct3 = InstructionSet[instruction]["funct3"]
    opcode = InstructionSet[instruction]["opcode"]

    if instruction== "lw":
        temp1= inst[1].split(",")
        temp2= temp1[1].split("(")
        
        

        imm= label(temp2[0], pc)
        imm= immManager(temp2[0], 12)

        try: 
            rs1= RegisterMap[temp2[1][:-1]]
            rd= RegisterMap[temp1[0]]
        except KeyError as e:
            raise SyntaxError(f"Invalid register name {e}")

        Binary= imm+ rs1 + funct3 + rd + opcode + "\n"
        return Binary
    
    regs= inst[1].split(",")
    
    rd= RegisterMap[regs[0]]
    rs1= RegisterMap[regs[1]]
    imm= immManager(regs[2], 12)

    Binary= imm+ rs1 + funct3 + rd + opcode + "\n"
    return Binary

def Stype(inst, pc):
    instruction= inst[0]

    funct3 = InstructionSet[instruction]["funct3"]
    opcode = InstructionSet[instruction]["opcode"]

    temp1= inst[1].split(",")
    temp2= temp1[1].split("(")

    imm= label(temp2[0], pc)*2
    imm= immManager(imm, 12)

    try: 
        rs2= RegisterMap[temp1[0]]
        rs1= RegisterMap[temp2[1][:-1]]
    except KeyError as e:
        raise SyntaxError(f"Invalid register name {e}")
    
    Binary= imm[:7]+rs2+rs1+funct3+ imm[7:] + opcode + "\n"
    return Binary

def Btype(inst, pc):
    instruction= inst[0]
    regs= inst[1].split(",")

    funct3 = InstructionSet[instruction]["funct3"]
    opcode = InstructionSet[instruction]["opcode"]

    try:
        rs1= RegisterMap[regs[0]]
        rs2= RegisterMap[regs[1]]
    except KeyError as e:
        raise SyntaxError(f"Invalid register name {e}")

    imm1= regs[2]
    imm= label(imm1, pc)
    imm= immManager(imm, 12)


    Binary= imm[0]+ imm[2:8] + rs2 + rs1 + funct3+ imm[8:]+ imm[1] +opcode + "\n"
    return Binary

def Jtype(inst, pc):
    instruction= inst[0]
    opcode = InstructionSet[instruction]["opcode"]
    regs= inst[1].split(",")
    
    try:
        rd= RegisterMap[regs[0]]
    except KeyError as e:
        raise SyntaxError(f"Invalid register name {e}")
    
    imm= label(regs[1], pc)
    imm= immManager(imm, 20)

    imm= imm[0] + imm[10:] + imm[9] + imm[1:9]
    Binary= imm+ rd+ opcode + "\n"
    return Binary

#--------------------------------
# File handling and writing
def GetInstructions(filename):
    Instructions= []
    with open(filename, "r") as assembly:
        for line in assembly:
            Instructions.append(line.strip().split())
    
    if Instructions[-1] != ['beq', 'zero,zero,0']:
        raise SyntaxError(f"Missing Virtual Halt")
    
    return Instructions

def FirstPass(lst):
    labels= {}
    ProgCount=0

    for i, inst in enumerate(lst):
        if inst[0].endswith(":"):
            labels[inst[0][:-1]]= ProgCount
            lst[i]= inst[1:]
        ProgCount += 4
    
    return labels

def SecondPass(lst, outfile):
    out= open(outfile, "w")
    labels= FirstPass(lst)
    pc=0

    for inst in lst:
        instruction= inst[0]
        
        if InstructionSet[instruction]["type"] == "R":
            Binary= Rtype(inst)
            out.write(Binary)
            pc += 4
        
        if InstructionSet[instruction]["type"] == "I":
            Binary= Itype(inst, pc)
            out.write(Binary)
            pc += 4
        
        if InstructionSet[instruction]["type"] == "S":
            Binary= Stype(inst,pc)
            out.write(Binary)
            pc += 4
        
        if InstructionSet[instruction]["type"] == "B":
            Binary= Btype(inst,pc)
            out.write(Binary)
            pc += 4

        if InstructionSet[instruction]["type"] == "J":
            Binary= Jtype(inst, pc)
            out.write(Binary)
            pc += 4
        
        else:
            continue

# main for all test cases

for i in range(3):
    Instructions= GetInstructions(f"Ex_test_{i}.txt")
    labels= FirstPass(Instructions)
    SecondPass(Instructions, f"out_{i}.txt")

for i in range(4,11):
    Instructions= GetInstructions(f"Ex_test_{i}.txt")
    labels= FirstPass(Instructions)
    SecondPass(Instructions, f"out_{i}.txt")