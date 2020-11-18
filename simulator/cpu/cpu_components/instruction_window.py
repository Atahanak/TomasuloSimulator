from simulator.cpu.common.instruction import Instruction


class InstructionWindow:
    def __init__(self, size):
        self.instructions = []
        self.size = size

    # returns False if addition was succesful, and true otherwise
    def add_to_window(self, instruction):
        if not isinstance(instruction, Instruction):
            raise "INS-W: attempting to add an object to instruction window that isn't an instruction"
        if len(self.instructions) >= self.size:
            return False
        else:
            self.instructions.append(instruction)
            return True

    def top_of_window(self):
        if len(self.instructions) <= 0:
            return None
        else:
            return self.instructions[0]

    def remove_from_instruction_window(self):
        if len(self.instructions) <= 0:
            raise "INS-W: attempting to remove items from an empty window"
        self.instructions = self.instructions[1:]

    def flush_instruction_window(self):
        self.instructions = []

    def printInstructionWindow(self):
        print("Instruction Window")
        for instruction in self.instructions:
            o = instruction.operation
            if instruction.destination:
                o = o + " " + instruction.destination + ","
            if instruction.operand1:
                o = o + " " + instruction.operand1 + ","
            if instruction.operand2:
                o = o + " " + instruction.operand2

            print(o)
