from constants import ISA 
#operations = ['ADD', 'SUB', 'MUL','DIV', 'LD', 'BGE']
class FunctionalUnit:
    def __init__(self, cycles):
        self.ID = None
        self.type = None
        self.Executing = False
        self.cycles_left = int(cycles)
        self.total_cycles = int(cycles)
    
    def begin_executing(self, typ, o1, o2, NextAddress = False):
        if self.Executing == True:
            raise 'trying to begin execution twice'
        self.type = typ
        self.operand1 = o1
        self.operand2 = o2
        self.cycles_left = self.total_cycles-1
        self.result = 0
        self.result = ISA[self.type](self.operand1, self.operand2, NextAddress)
        self.Executing = True
        if self.cycles_left == 0:
            return [True, self.result]
        else:
            return [False, False]

    def execute_cycle(self):
        if self.cycles_left == 0:
            return [True, self.result]
        else:
            self.cycles_left-=1
            return [False,False]
        
    def reset_FU(self):
        self.cycles_left = self.total_cycles
        self.Executing = False

    
    def is_executing(self):
        return self.Executing
    