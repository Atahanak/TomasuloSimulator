from RegisterTable import RegisterTable as RT
from ReorderBuffer import ReorderBuffer as RB
from CommonDataBus import CommonDataBus as CDB
from ReservationStation import ReservationStation as RS
from constants import BRANCH_OPERATIONS
INSTRUCTION_SIZE = 4
class CPU:
    def __init__(self, params, units):
        self.cdb = CDB()
        self.RS = []
        self.construct_reservation_stations(units)
        self.RT = RT(params['number_of_registers'])
        self.RB = RB(len(self.RS), self.RT,self.cdb)
        self.program_counter = 0
        self.instruction_window = []
        self.instruction_window_size = int(params['instruction_window_size'])

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

    def run(self, program):
        # fetch the next instruction from the program
        # TODO FIGURE OUT LOOP
        #while (some condition telling us program is done):
        # - go over all the RS 
        #       - ask them to read the CBD 
        #       - ask them to execute or update cdb
        # TODO FINISH LOOP
        self.program_counter = 0
        self.program = program
        end_of_program = self.get_end_of_program(program)
        cycle = 0
        while self.program_counter <= end_of_program:

            instruction = self.program[self.program_counter]
            self.program_counter+= INSTRUCTION_SIZE
            # try to add it to the instruction window
            added_succesfully = self.add_to_instruction_window(instruction)
            if not added_succesfully:
                self.program_counter-= INSTRUCTION_SIZE
            elif instruction['INST'] in BRANCH_OPERATIONS:
                self.program_counter = int(instruction['DEST']) - INSTRUCTION_SIZE

            instruction = self.top_instruction_window()
            rs_empty = None
            if instruction is not None and not self.RB.is_full():
                operation = instruction['INST'] 
                rs_empty = self.find_empty_rs(operation)
            
            for rs in self.RS: # EXCEPT THE GUY WHO JUST GOT ISSUED
                if rs is rs_empty:
                    #- get the register values (or ROB values) from RT, RB
                    self.remove_from_instruction_window()
                    operation = instruction['INST'] 
                    issue_object = {'op': operation}
                    if 'OP1' in list(instruction.keys()):
                        op1 = instruction['OP1']
                        if self.RT[op1]['reorder'] is not None:
                            issue_object['Qj'] = self.RT[op1]['reorder']
                            issue_object['Vj'] = None
                        else:
                            issue_object['Vj'] = self.RT[op1]['value']
                            issue_object['Qj'] = None
                    if 'OP2' in list(instruction.keys()):
                        op2 = instruction['OP2'] 
                        if self.RT[op2]['reorder'] is not None:
                            issue_object['Qk'] = self.RT[op2]['reorder']
                            issue_object['Vk'] = None
                        else:
                            issue_object['Vk'] = self.RT[op2]['value']
                            issue_object['Qk'] = None
                    if 'DEST' in list(instruction.keys()):
                        dest = instruction['DEST']
                        rob_dest = self.RB.get_instruction(operation, dest) # using the register ID to write to, will reserve an ROB entry
                        issue_object['Des'] = rob_dest
                    else : 
                        issue_object['Dest'] = None
                    if operation in BRANCH_OPERATIONS:
                        issue_object['Addr'] = self.program_counter
                    else:
                        issue_object['Addr'] = None

                    #       - tell register which ROB it is assigned / handled by ROB
                    #       - Issue the instruction to the RS
                    rs.issue_to_RS(issue_object['op'], issue_object['Qj'], issue_object['Qk'], issue_object['Vj'], issue_object['Vk'], issue_object['Des'], issue_object['Addr'])
                elif rs.is_executing() and not rs.is_writing_back(): #execute rs.is_executing():
                    rs.execute()
                elif rs.is_writing_back(): #write back
                    rs.write_back()
            
            jump_location = self.RB.update() #if flushed return back to branch address
            if jump_location is not None:
                self.program_counter = jump_location
            self.RB.commit()
            self.printReport(cycle)
            cycle+=1
    
    def printInstructionWindow(self):
        print("Instruction Window")
        for instruction in self.instruction_window:
            o = instruction["INST"]
            if 'OP1' in list(instruction.keys()):
                o = o + " " + instruction["OP1"] + ","
            if 'OP2' in list(instruction.keys()):
                o = o + " " + instruction["OP2"] + ","
            if 'DEST' in list(instruction.keys()):
                o = o + " " + instruction["DEST"]
            print(o)

    def printReport(self, cycle):
        print("------------------------")
        cs = "CYCLE " + str(cycle)
        print(cs)
        self.printInstructionWindow()
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
