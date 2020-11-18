from ..common.constants import BRANCH_OPERATIONS, ISA, FP_OPERATIONS, LOAD_OPERATIONS


class Instruction:
    def __init__(
        self, address, operation, operand1, operand2, destination, leap_address
    ):
        self.address = int(address)
        self.operation = operation
        self.operand1 = operand1
        self.operand2 = operand2
        self.destination = destination
        self.leap_address = leap_address
        self.confirm_standard()
        if self.leap_address is not None:
            self.leap_address = int(self.leap_address)

    def confirm_standard(self):
        if self.operation not in ISA.keys():
            raise "INS: attempting to create an instruction with an invalid operation"
        if self.operation in BRANCH_OPERATIONS:
            if (
                self.operand1 is None
                or self.operand2 is None
                or self.leap_address is None
                or self.destination is not None
            ):
                raise "INS: passed incorrect parameters to create a branch"
        elif self.operation in FP_OPERATIONS:
            if (
                self.operand1 is None
                or self.operand2 is None
                or self.destination is None
                or self.leap_address is not None
            ):
                raise "INS: passed incorrect parameters to create an FP"
        elif self.operation in LOAD_OPERATIONS:
            if (
                self.operand1 is None
                or self.destination is None
                or self.leap_address is not None
                or self.operand2 is not None
            ):
                raise "INS: passed incorrect parameters to create a load "

    def has_op1(self):
        return self.operand1 != None

    def has_op2(self):
        return self.operand2 != None

    def has_leap_address(self):
        return self.leap_address != None

    def has_destination(self):
        return self.destination != None
