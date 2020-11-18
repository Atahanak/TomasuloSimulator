from Instruction import Instruction as Instruction


class Program:
    def __init__(self, instruction_dictionary):
        print(instruction_dictionary)
        self.instruction_stream = self.construct_stream(instruction_dictionary)
        self.max_address = max(list(self.instruction_stream.keys()))

    def construct_stream(self, instruction_dictionary):
        stream = {}
        for instruction in instruction_dictionary.values():

            address = int(instruction["AF"])
            operation = instruction["INST"]
            operand1 = None if "OP1" not in instruction.keys() else instruction["OP1"]
            operand2 = None if "OP2" not in instruction.keys() else instruction["OP2"]
            destination = (
                None if "DEST" not in instruction.keys() else instruction["DEST"]
            )
            leap_address = (
                None if "ADDR" not in instruction.keys() else instruction["ADDR"]
            )
            stream[address] = Instruction(
                address,
                operation=operation,
                operand1=operand1,
                operand2=operand2,
                destination=destination,
                leap_address=leap_address,
            )

        return stream

    def get_max_address(self):
        return self.max_address

    def get_instruction(self, index):
        if index > self.max_address:
            raise "PRG: attempting to get an instruction out of the boundaries of the program"
        return self.instruction_stream[index]

    def __getitem__(self, index):
        return self.get_instruction(index)
