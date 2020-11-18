import sys
from cpu import CPU


def parse_parameters(file_name):
    params = {}
    f = open(file_name, "r")
    for line in f:
        line_c = line.strip()
        if line_c != "":
            words = line.split(" ")
            params[words[0][:-1]] = int(words[1][:-1])
    return params


"""
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
"""


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
            ent["id"] = "RS" + str(counter)
            counter += 1
            units.append(ent)
    return units


def parse_program(file_name):
    program = {}
    with open(file_name, "r") as f:
        for line in f:
            cs = line.find("#")
            line_c = line[:cs].strip()
            if line_c != "":
                ls = line_c.split()
                inst = {}
                address = int(ls[0][:-1])
                inst["AF"] = address
                inst["INST"] = ls[1]
                if inst["INST"] == "LD":
                    inst["DEST"] = ls[2][:-1]  # remove comma
                    inst["OP1"] = ls[3]
                elif inst["INST"] == "BGE":  # add other branch instructions
                    inst["OP1"] = ls[2][:-1]
                    inst["OP2"] = ls[3][:-1]
                    inst["ADDR"] = ls[4]
                else:
                    inst["DEST"] = ls[2][:-1]
                    inst["OP1"] = ls[3][:-1]
                    inst["OP2"] = ls[4]
                program[address] = inst
    return program


def usage():
    print("Params Units Program")


if __name__ == "__main__":
    """
    if len(sys.argv) < 4:
        usage()
        exit()
        """

    # params = parse_parameters(sys.argv[1])
    params = parse_parameters("configuration/Parameters.txt")
    print("Params:")
    print(params)
    # instructions = parse_instructions(sys.argv[2])
    # print("Instructions:")
    # print(instructions)
    # units = parse_units(sys.argv[2])
    units = parse_units("configuration/Units.txt")
    print("Units:")
    print(units)
    print("Program:")
    program = parse_program("configuration/Program.txt")
    # program = parse_program(sys.argv[3])
    print(program)
    print()
    print()

    CPU = CPU(params, units)
    CPU.run(program)
# exit()
