operations = ['ADD', 'SUB', 'MUL','DIV', 'LD', 'BG']
class FunctionalUnit:
    def __init__(self, cycles):
        self.ID = None
        self.type = None
        self.Executing = False
        self.cycles_left = cycles
        self.total_cycles = cycles
    
    def begin_executing(self, typ, o1, o2, NextAddress = False):
        if self.Executing == True:
            raise 'trying to begin execution twice'
        self.type = typ
        self.operand1 = o1
        self.operand2 = o2
        self.total_cycles = self.cycles_left-1
        self.result = 0
        if (self.type == operations[0]): self.result = self.operand1+self.operand2
        if (self.type == operations[2]): self.result = self.operand1-self.operand2
        if (self.type == operations[3]): self.result = self.operand1*self.operand2
        if (self.type == operations[4]): self.result = self.operand1/self.operand2
        if (self.type == operations[5]): self.result = self.operand1
        if (self.type == operations[6]): self.result = self.operand1 >= self.operand2
        self.Executing = True

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
    