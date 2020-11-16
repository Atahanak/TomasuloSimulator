from RegisterTable import RegisterTable as RT
#from CommonDataBus

class ReorderBuffer:
    
    __ROB_Entry = {"operation": None, "busy": None, "ready": False, "dest": None, "value": None}
    def __init__(self, size, register_table, cbd):
        self.register_table = register_table
        self.head = 0
        self.tail = 0
        self.size = size
        self.CBD = cbd
        self.table = []
        for i in range(self.size):
            self.table.append(self.__ROB_Entry)

    def robid_2_str(self, rid):
        return "ROB"+str(rid)

    def robid_2_idx(self, rid):
        return int(rid.split("ROB")[1])

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
            return None #table is full
        else:
            self.table[self.tail]["operation"] = operation
            self.table[self.tail]["dest"] = dest
            self.register_table.reserveRegister(dest, self.robid_2_str(self.tail))
            self.tail = (self.tail + 1) % self.size #update tail in a circular fashion
            return self.robid_2_str(self.tail-1)

    def update(self):
        if self.CBD.Full:
            self.table[self.robid_2_idx(self.CBD.ROB_ID)]["value"] = self.CBD.Value

    def commit(self):
        if self.table[self.head]["value"] is not None:
            self.register_table.updateRegister(self.table[self.head]["dest"], self.table[self.head]["value"])
            self.table[self.head] = self.__ROB_Entry
            self.head = (self.head + 1) % self.size #update head in a circular fashion

    def flush(self):
        pass


if __name__=="__main__":
    rob = ReorderBuffer(4)
    rob.printTable()