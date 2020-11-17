class CommonDataBus:
    def __init__(self):
        #self.slots = []
        self.clear_cbd()

    def is_empty(self):
        return not self.Full
        #if len(self.slots) < self.Capacity:
        #    return True
        #else:
        #    return False
    
    def add_result(self, rob_id, value):
        if self.Full:
            raise 'trying to overfill cdb'
        self.Full = True
        self.ROB_ID = rob_id
        self.Value = value
        #if len(self.slots) >= self.Capacity:
        #    raise 'trying to overfill cdb'
        #self.slots.append([rob_id, value])
    
    def get_result(self, rob_id):
        #for item in self.slots:
        #    if item[0] == rob_id:
        #        return item[1]
        #return False
        if rob_id == self.ROB_ID:
            return self.Value
        return False
    
    def clear_cbd(self):
        self.Full = False
        self.ROB_ID = None
        self.Value = None
        #self.Capacity = capacity
        #self.slots = []
    def printCommonDataBus(self):
        if self.Full == True:
            print(str(float(self.Value))+"\t"+self.ROB_ID)