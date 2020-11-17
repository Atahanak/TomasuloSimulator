class RegisterTable:
    def __init__(self, size):
        self.size = size
        self.table = []
        for i in range(self.size):
            self.table.append({"reorder": None, "value": i})

    def rid_2_str(self, rid):
        return "R"+str(rid)
    
    def rid_2_int(self, rid):
        return int(rid.split("R")[1])

    def printTable(self):
        print("Registers")
        for index, r in enumerate(self.table):
            p = self.rid_2_str(index) + " " + str(r["value"]) + " " + str(r["reorder"])
            print(p) #needs update
        #print(self.table)

    def updateRegister(self, register_id, val):
        self.table[register_id]["value"] = val
        self.table[register_id]["reorder"] = None
    
    def reserveRegister(self, register_id, rob_id):
        self.table[self.rid_2_int(register_id)]["reorder"] = rob_id
    
    def __getitem__(self, rid):
        return self.table[self.rid_2_int(rid)]

if __name__=="__main__":
    registers = RegisterTable(4)
    registers.printTable()
    registers.reserveRegister(2, "ROB1")
    registers.printTable()
    registers.updateRegister(2, 1.2)
    registers.printTable()