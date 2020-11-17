from RegisterTable import RegisterTable as RT
from Constants import BRANCH_OPERATIONS
#from CommonDataBus

class ReorderBuffer:
    
    rob_entry = {"operation": None, "ready": False, "dest": None, "value": None}
    def __init__(self, size, register_table, CDB):
        self.register_table = register_table
        self.head = 0
        self.tail = 0
        self.size = size
        self.CDB = CDB
        self.table = []
        for i in range(self.size):
            self.table.append(self.rob_entry)

    def is_full(self):
        return self.head == self.tail and self.table[self.head]["operation"] is not None

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
        if self.is_full(): #check if rob is available
            return None #table is full
        else:
            self.table[self.tail]["operation"] = operation
            self.table[self.tail]["dest"] = dest
            self.register_table.reserveRegister(dest, self.robid_2_str(self.tail))
            self.tail = (self.tail + 1) % self.size #update tail in a circular fashion
            return self.robid_2_str(self.tail-1)

    def update(self):
        if self.CDB.Full:
            self.table[self.robid_2_idx(self.CDB.ROB_ID)]["value"] = self.CDB.Value


    def commit(self):
        if self.table[self.head]["value"] is not None:
            if self.table[self.head]["operation"] in BRANCH_OPERATIONS and self.table[self.head]["value"] != True: #flush entries between head and tail
                self.flush(self.head + 1)
                return self.table[self.head]["value"]
            else:
                self.register_table.updateRegister(self.table[self.head]["dest"], self.table[self.head]["value"])
            self.table[self.head] = self.rob_entry
            self.head = (self.head + 1) % self.size #update head in a circular fashion
        return None

    def flush(self, start):
        end = self.tail
        if end < start:
            end += self.size - self.head
        for i in range(start, end):
            self.table[i % self.size] = self.rob_entry


if __name__=="__main__":
    rob = ReorderBuffer(4)
    rob.printTable()