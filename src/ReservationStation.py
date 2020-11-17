import CommonDataBus
import FunctionalUnit 

class ReservationStation:
    def __init__(self, name, typ, cycles, cdb):
        self.ID = name
        self.Types = typ
        self.FU = FunctionalUnit.FunctionalUnit(cycles)
        self.CDB = cdb # the common data bus object to broadcast information to
        self.reset_RS()
    
    def get_types(self):
        return self.Types
    
    def is_empty(self):
        return not self.Busy
    
    def is_executing(self):
        return self.Busy
    
    def is_writing_back(self):
        return self.writing_back
    
    def reset_RS(self):
        self.Op = None
        self.Qj = None
        self.Qk = None
        self.Vj = None
        self.Vk = None
        self.Des = None
        self.result = None
        self.Busy = False
        self.writing_back = False
    
    def issue_to_RS(self, Op, Qj, Qk, Vj, Vk, Des):
        if self.writing_back == True:
            raise 'Trying to issue to an RS that\'s writing back'
        if self.Busy == True:
            raise "Trying to issue to an RS that's executing"
        self.Busy = True
        self.Op = Op
        self.Qj = Qj
        self.Qk = Qk
        self.Vj = Vj
        self.Vk = Vk
        self.Des = Des
    
    def execute(self):
        if self.writing_back:
            raise 'trying to execute an RS that\'s executing'
        if self.Busy == None:
            raise 'trying to execute an RS that\'s free'
        # If awaiting data bus, will start by trying to broadcast output 
        if self.FU.is_executing():
            # We must execute an additional cycle
            result = self.FU.execute_cycle()
            #if done executing
            if result[0] !=None:
                self.result = result[1]
                self.FU.reset_FU()
                self.writing_back = True
        # if the RS is busy and isn't executing, it means that it was awaiting one of its parameters
        else:
            if (self.Qj != None):
                value = self.CDB.get_result(self.Qj)
                if value != None: self.Vj = value
                self.Qj = None
            if (self.Qk != None):
                value = self.CDB.get_result(self.Qk)
                if value != None: self.Vk = value
                self.Qk = None
            if self.Qj != None and self.Qk != None:
                self.FU.begin_executing(self.Op, self.Vj, self.Vk)

    def write_back(self):
        if self.Busy == None:
            raise 'Trying to write back from an empty RS'
        if self.writing_back == None:
            raise 'Trying to write back from an RS that\'s executing'
        if self.CDB.is_empty() == None:
            self.writing_back = True
        else:
            self.CDB.add_result(self.Des, self.result)
            self.reset_RS()

        # checks if the reservation station is done executing
        # if it is, the RS will populate its results to the CDB
