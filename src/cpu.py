from RegisterTable import RegisterTable as RT
from ReorderBuffer import ReorderBuffer as RB
from CommonDataBus import CommonDataBus as CDB
from ReservationStation import ReservationStation as RS
from constants import BRANCH_OPERATIONS
from Program import Program as Program
from InstructionWindow import InstructionWindow as InstructionWindow 
INSTRUCTION_SIZE = 4
class CPU:
    def __init__(self, params, units):
        self.cdb = CDB()
        self.RS = []
        self.construct_reservation_stations(units)
        self.RT = RT(params['number_of_registers'])
        self.RB = RB(len(self.RS), self.RT,self.cdb)
        self.program_counter = 0
        self.instruction_window_size = int(params['instruction_window_size'])
        self.instruction_window = InstructionWindow(self.instruction_window_size)

    def construct_reservation_stations(self, units):
        for unit in units:
            rs = RS(unit['id'], unit['OPS'], unit['cycles'], self.cdb)
            self.RS.append(rs)

    # can't add past size
    def add_to_instruction_window(self, instruction):
        if len(self.instruction_window) >=self.instruction_window_size:
            return False
        else:
            self.instruction_window.append(instruction)
            return True

    def top_instruction_window(self):
        if (len(self.instruction_window))<=0:
            return None
            # todo is this correct???
            #raise 'attempting to fetch an instruction from an empty window'
        else:
            instruction = self.instruction_window[0]
            return instruction

    def remove_from_instruction_window(self):
        if (len(self.instruction_window))<=0:
            return None
            # todo is this correct???
            #raise 'attempting to fetch an instruction from an empty window'
        else:
            instruction = self.instruction_window[0]
            self.instruction_window = self.instruction_window[1:]
            return instruction

    def find_empty_rs(self, op):
        for rs in self.RS:
            if op in rs.Types and rs.Busy == False:
                return rs
        return None

    def get_end_of_program(self, program):
        return max(program.keys())

    def is_ROB_empty(self):
        return self.RB.is_empty()

    def write_back_step(self, RS):
        for rs in RS: #write_back
            if rs.is_writing_back():
                rs.write_back()
    
    def execute_step(self, RS):
        for rs in RS: 
            if rs.is_executing() and not rs.is_writing_back(): #execute rs.is_executing():
                rs.execute()
        
    def instruction_window_append_step(self, program_counter, end_of_program, program, instruction_window):
        if program_counter <= end_of_program:
            instruction = program[program_counter]
            program_counter+= INSTRUCTION_SIZE
        # try to add it to the instruction window
            added_succesfully = instruction_window.add_to_window(instruction)
            if not added_succesfully:
                program_counter-= INSTRUCTION_SIZE
            elif instruction.operation in BRANCH_OPERATIONS:
                program_counter = instruction.leap_address
        return program_counter

    def update_ROB_step(self, program_counter, RB, instruction_window, RS):
        jump_location, flushed = RB.update() #if flushed return back to branch address
        if jump_location is not None:
            program_counter = jump_location + INSTRUCTION_SIZE
            instruction_window.flush_instruction_window()
            for rs in RS:
                if rs.Des in flushed:
                    rs.reset_RS()
        return program_counter, jump_location

    
    def run(self, program):
        # fetch the next instruction from the program
        # TODO FIGURE OUT LOOP
        #while (some condition telling us program is done):
        # - go over all the RS 
        #       - ask them to read the CBD 
        #       - ask them to execute or update cdb
        # TODO FINISH LOOP
        self.program_counter = 0
        self.program = Program(program)
        end_of_program = self.program.get_max_address()
        cycle = 0
        while (self.program_counter <= end_of_program or not self.RB.is_empty()):# and cycle < 81:
        
            # appending to instruction window
            self.program_counter = self.instruction_window_append_step(self.program_counter, end_of_program, self.program, self.instruction_window)

            # write back
            self.write_back_step(self.RS)


            # ROB update
            self.program_counter, jump_location = self.update_ROB_step(self.program_counter, self.RB, self.instruction_window, self.RS)
            
            # Execute
            self.execute_step(self.RS)

            rs_empty = None
            instruction = self.instruction_window.top_of_window() 
            if instruction is not None and not self.RB.is_full():
                operation = instruction.operation 
                rs_empty = self.find_empty_rs(operation)
            if jump_location is None:
                for rs in self.RS: # issue
                    if rs is rs_empty:
                        #- get the register values (or ROB values) from RT, RB
                        self.instruction_window.remove_from_instruction_window()
                        operation = instruction.operation
                        issue_object = {'op': operation}
                        op1 = instruction.operand1
                        op2 = instruction.operand2
                        destination = instruction.destination
                        leap_address = instruction.leap_address
                        address = instruction.address
                        if op1:
                            if op1.startswith('R'):
                                if self.RT[op1]['reorder'] is not None:
                                    if self.RB[self.RT[op1]['reorder']]["value"] != None:
                                        issue_object['Vj'] = self.RB[self.RT[op1]['reorder']]["value"]
                                        issue_object['Qj'] = None
                                    else:
                                        issue_object['Qj'] = self.RT[op1]['reorder']
                                        issue_object['Vj'] = None
                                else:
                                    issue_object['Vj'] = self.RT[op1]['value']
                                    issue_object['Qj'] = None
                            else:
                                issue_object['Vj'] = int(op1)
                                issue_object['Qj'] = None
                        else:
                                issue_object['Vj'] = None
                                issue_object['Qj'] = None

                        if op2:
                            if op2.startswith('R'):
                                if self.RT[op2]['reorder'] is not None:
                                    if self.RB[self.RT[op2]['reorder']]["value"] != None:
                                        issue_object['Vk'] = self.RB[self.RT[op2]['reorder']]["value"]
                                        issue_object['Qk'] = None
                                    else:
                                        issue_object['Qk'] = self.RT[op2]['reorder']
                                        issue_object['Vk'] = None
                                else:
                                    issue_object['Vk'] = self.RT[op2]['value']
                                    issue_object['Qk'] = None
                            else:
                                issue_object['Vk'] = int(op2)
                                issue_object['Qk'] = None
                        else:
                                issue_object['Vk'] = None
                                issue_object['Qk'] = None

                        if destination:
                            dest = destination
                        else : 
                            issue_object['Des'] = None    
                        rob_dest = self.RB.get_instruction(operation, dest) # using the register ID to write to, will reserve an ROB entry
                        issue_object['Des'] = rob_dest
                        if operation in BRANCH_OPERATIONS:
                            issue_object['Addr'] = address
                        else:
                            issue_object['Addr'] = None

                        #       - tell register which ROB it is assigned / handled by ROB
                        #       - Issue the instruction to the RS
                        rs.issue_to_RS(issue_object['op'], issue_object['Qj'], issue_object['Qk'], issue_object['Vj'], issue_object['Vk'], issue_object['Des'], issue_object['Addr'])

            self.RB.commit()
            self.printReport(cycle)
            cycle+=1
            self.cdb.clear_cbd()
    

    def printReport(self, cycle):
        print("------------------------")
        cs = "CYCLE " + str(cycle)
        print(cs)
        self.instruction_window.printInstructionWindow()
        print()
        self.RT.printTable()
        print()
        print("Reservation Stations")
        for rs in self.RS:
            rs.printReservationStation()
        print()
        self.RB.printTable()
        print()
        print("Common Data Bus")
        self.cdb.printCommonDataBus()
        print()
