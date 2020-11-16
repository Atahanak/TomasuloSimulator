from RegisterTable import RegisterTable as RT
#from CommonDataBus

class ReorderBuffer:
    
    __ROB_Entry = {"operation": None, "busy": None, "ready": False, "dest": None, "value": None}
    def __init__(self, size, register_table_size):
        self.register_table = RT(register_table_size)
        self.head = 0
        self.tail = 0
        self.size = size
        #self.CBD = cbd
        self.table = []
        for i in range(self.size):
            self.table.append(self.__ROB_Entry)

    def robid_2_str(self, rid):
        return "ROB"+str(rid)

    def printTable(self):
        print("Reorder Buffer")
        for index, r in enumerate(self.table):
            p = self.robid_2_str(index) + ":" 
            if r["operation"] is not None:
                p = p + " " + r["operation"] + " " + r["dest"] + " " + str(r["value"])
                if index == self.head:
                    p += " (H)"
                if index == self.tail:
                    p += " (T)"
            print(p)

    def get_instruction(self, operation, dest):
        if self.head == self.tail and self.table[self.head]["operation"] is not None: #check if rob is available
            return False #table is full
        else:
            self.table[self.tail]["operation"] = operation
            self.table[self.tail]["dest"] = dest
            self.tail = (self.tail + 1) % self.size #update tail in a circular fashion
            return True

    def update(self, rob_id, value): #CBD?
        self.table[rob_id]["value"] = value

    def commit(self, rob_id):
        self.register_table.updateRegister(self.table[rob_id]["dest"], self.table[rob_id]["value"])
        self.table[rob_id] = self.__ROB_Entry
        self.head = (self.head + 1) % self.size #update head in a circular fashion

if __name__=="__main__":
    rob = ReorderBuffer(4, 4)
    rob.printTable()