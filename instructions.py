InstructionSet= {
    "add": {"opcode": "0110011", "funct7":"0000000", "funct3": "000", "type": "R"},
    "sub": {"opcode": "0110011", "funct7":"0100000", "funct3": "000", "type": "R"},
    "slt": {"opcode": "0110011", "funct7":"0000000", "funct3": "010", "type": "R"},
    "srl": {"opcode": "0110011", "funct7":"0000000", "funct3": "101", "type": "R"},
    "or": {"opcode": "0110011", "funct7":"0000000", "funct3": "110", "type": "R"},
    "and": {"opcode": "0110011", "funct7":"0000000", "funct3": "111", "type": "R"},
    "lw": {"opcode": "0000011", "funct3": "010", "type":"I"},
    "addi": {"opcode": "0010011", "funct3": "000", "type":"I"},
    "jalr": {"opcode": "1100111", "funct3": "000", "type":"I"},
    "sw": {"opcode":"0100011", "funct3": "010", "type":"S"},
    "beq": {"opcode":"1100011", "funct3":"000", "type":"B"},
    "bne": {"opcode":"1100011", "funct3":"001", "type":"B"},
    "blt": {"opcode":"1100011", "funct3":"010", "type":"B"},
    "jal": {"opcode":"1101111", "type":"J" }
}

