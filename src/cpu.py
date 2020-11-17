from RegisterTable import RegisterTable as RT
from ReorderBuffer import ReorderBuffer as RB
from CommonDataBus import CommonDataBus as CDB
from ReservationStation import ReservationStation as RS
INSTRUCTION_SIZE = 4
class CPU:
    def __init__(self, params, instructions, units, program):
        self.cdb = CDB()
        self.RS = []
        self.construct_reservation_stations(units)
        self.RT = RT(params['number_of_registers'])
        self.RB = RB(len(self.RS), self.RT,self.cdb)
        self.program = program
        self.program_counter = 0
        self.instruction_window = []
        self.instruction_window_size = int(units['instruction_window_size'])

    def construct_reservation_stations(self, units):
        for unit in units:
            rs = RS(unit['id'], unit['OPS'], unit['cycles'], self.cdb)
            self.RS.append(rs)

    # can't add past size
    def add_to_instruction_window(self, insturction):
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

    def run(self):
        # fetch the next instruction from the program
        # TODO FIGURE OUT LOOP
        while (some condition telling us program is done):
        instruction = self.program[self.program_counter]
        self.program_counter+= INSTRUCTION_SIZE
        # try to add it to the instruction window
        added_succesfully = self.add_to_instruction_window(instruction)
        if not added_succesfully:
            self.program_counter-= INSTRUCTION_SIZE
        # attempt to issue an instruction from the instruction window
        # - get instruction from window
        # - check if there's a free RS for this instruction
        instruction = self.top_instruction_window()
        if instruction is not None:
            operation = instruction['INST'] 
            rs = self.find_empty_rs(operation)
            if rs is not None:
        #       - get the register values (or ROB values) from RT, RB
                self.remove_from_instruction_window()
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
                # reserve an ROB
                    # using the register ID to write to, will reserve an ROB entry
                    rob_dest = self.RB.get_instruction(operation, dest)
                    issue_object['Des'] = rob_dest
                else : issue_object['Dest'] = None

        #       - tell register which ROB it is assigned / handled by ROB
        #       - Issue the instruction to the RS
                rs.issue_to_RS(issue_object['op'], issue_object['Qj'], issue_object['Qk'], issue_object['Vj'], issue_object['Vk'], issue_object['Des'])
            
        # - go over all the RS 
        #       - ask them to read the CBD 
        #       - ask them to execute or update cdb
        # TODO FINISH LOOP
        for rs in self.RS: # EXCEPT THE GUY WHO JUST GOT ISSUED
            if rs.is_executing():
                # either execute or write back
        self.RB.update() 
        self.RB.commit()
        # TODO FLUSH BOI
        # - tell the ROB to update from cbd
        # - tell the rob to commit to register file
        # - print out the cycle info
    # TODO PRINT FUNCTION
    def print(self):
        print('hello')