from .register_table import RegisterTable as RT
from simulator.cpu.common.constants import BRANCH_OPERATIONS

class ReorderBuffer:
    # dest: register ID i am writing to
    rob_entry = {"operation": None, "ready": False, "dest": None, "value": None}

    def __init__(self, size, register_table, CDB):
        self.register_table = register_table
        self.head = 0
        self.tail = 0
        self.size = size
        self.CDB = CDB
        self.table = []
        for _ in range(self.size):
            self.table.append(dict(self.rob_entry))

    def is_full(self):
        return self.head == self.tail and self.table[self.head]["operation"] is not None

    def is_empty(self):
        return self.head == self.tail and self.table[self.head]["operation"] is None

    def robid_2_str(self, rid):
        return "ROB" + str(rid)

    def robid_2_idx(self, rid):
        return int(rid.split("ROB")[1])

    def printTable(self):
        print("Reorder Buffer")
        for index, r in enumerate(self.table):
            p = self.robid_2_str(index) + ":"
            if r["operation"] is not None:
                p = (
                    p
                    + " "
                    + r["operation"]
                    + " "
                    + str(r["dest"])
                    + " "
                    + str(r["value"])
                )
            if index == self.head:
                p += " (H)"
            if index == (self.tail) % self.size:
                p += " (T)"
            print(p)

    def get_instruction(self, operation, dest):
        if self.is_full():  # check if rob is available
            raise "you messed up"
        else:
            self.table[self.tail]["operation"] = operation
            if operation not in BRANCH_OPERATIONS:
                self.table[self.tail]["dest"] = dest
                self.register_table.reserveRegister(dest, self.robid_2_str(self.tail))
            else:
                self.table[self.tail]["dest"] = None
            self.tail = (self.tail + 1) % self.size  # update tail in a circular fashion
            return self.robid_2_str((self.tail - 1) % self.size)

    def update(self):
        if self.CDB.Full:
            curr_rob = self.robid_2_idx(self.CDB.ROB_ID)
            if self.table[curr_rob]["operation"] in BRANCH_OPERATIONS:
                self.table[curr_rob]["value"] = self.CDB.Value
                if (
                    self.table[curr_rob]["value"] != True
                ):  # flush entries between head and tail
                    flushed = self.flush((curr_rob + 1) % self.size)
                    return (self.CDB.Value, flushed)
            else:
                self.table[curr_rob]["value"] = self.CDB.Value
        return (None, None)

    def commit(self):
        if self.table[self.head]["value"] is not None: #check if head is empty
            if self.table[self.head]["operation"] not in BRANCH_OPERATIONS:
                self.register_table.updateRegister(
                    self.table[self.head]["dest"],
                    self.table[self.head]["value"],
                    self.robid_2_str(self.head),
                )
            self.table[self.head] = dict(self.rob_entry)
            self.head = (self.head + 1) % self.size  # update head in a circular fashion

    def flush(self, start):
        flushed = []
        end = self.tail
        if end < start:
            end += self.size - self.head + 1
        for i in range(start, end):
            flushed.append(self.robid_2_str(i % self.size))
            if self.table[i % self.size]["dest"] is not None: 
                if self.register_table[self.table[i % self.size]["dest"]][
                    "reorder"
                ] == self.robid_2_str(i % self.size): #check if register is reserved by this rob entry
                    self.register_table[self.table[i % self.size]["dest"]][
                        "reorder"
                    ] = None
            self.table[i % self.size] = dict(self.rob_entry) #flush entry
        self.tail = start
        return flushed

    def __getitem__(self, rid):
        return self.table[self.robid_2_idx(rid)]
