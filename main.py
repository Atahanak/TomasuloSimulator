import sys

def parse_parameters(file_name):
    params = {}
    f = open(file_name, "r")
    for line in f:
        line_c = line.strip()
        if line_c != "":
            words = line.split(" ")
            params[words[0][:-1]] = int(words[1][:-1])
    return params

def parse_instructions(file_name):
    instructions = []
    f = open(file_name, "r")
    for line in f:
        cs = line.find("#")
        line_c = line[:cs].strip()
        if line_c != "":
            ls = line_c.split(" ")
            inst = {}
            inst["INST"] = ls[0]
            if inst["INST"] == "LD":
                inst["DEST"] = ls[1]
                inst["VALUE"] = ls[2]
            elif inst["INST"] == "BGE": #add other branch instructions
                inst["OP1"] = ls[1]
                inst["OP2"] = ls[2]
                inst["ADDR"] = ls[3]
            else:
                inst["DEST"] = ls[1]
                inst["OP1"] = ls[2]
                inst["OP2"] = ls[3]
            instructions.append(inst)
    return instructions

def parse_units(file_name):
    units = []
    f = open(file_name, "r")
    counter = 0
    for line in f:
        cs = line.find("#")
        line_c = line[:cs].strip()
        if line_c != "":
            ls = line_c.split(" ")
            ent = {}
            ent["OPS"] = []
            ops = ls[1].split(",")
            for op in ops:
                ent["OPS"].append(op)
            ent["cycles"] = ls[2]
            ent["id"] = counter
            counter+=1
            units.append(ent)
    return units

def parse_program(file_name):
    program = {}
    with  open(file_name, "r") as f:
        for line in f:
            cs = line.find("#")
            line_c = line[:cs].strip()
            if line_c != "":
                ls = line_c.split()
                inst = {}
                address = ls[0][:-1]
                inst["INST"] = ls[1]
                if inst["INST"] == "LD":
                    inst["DEST"] = ls[2][:-1] # remove comma
                    inst["VALUE"] = ls[3]
                elif inst["INST"] == "BGE": #add other branch instructions
                    inst["OP1"] = ls[2][:-1]
                    inst["OP2"] = ls[3][:-1]
                    inst["ADDR"] = ls[4]
                else:
                    inst["DEST"] = ls[2][:-1]
                    inst["OP1"] = ls[3][:-1]
                    inst["OP2"] = ls[4]
                program[address] = inst
    return program            

if __name__=="__main__":
    params = parse_parameters(sys.argv[1])
    print("Params:")
    print(params)
    instructions = parse_instructions(sys.argv[2])
    print("Instructions:")
    print(instructions)
    units = parse_units(sys.argv[3])
    print("Units:")
    print(units)
    print("Program:")
    program = parse_program(sys.argv[4])
    print(program)

    #CPU = CPU(params, instructions, units, program)
    #CPU.run()
    exit()

