class RegisterTable:
    def __init__(self, size):
        self.size = size
        self.table = []
        for _ in range(self.size):
            self.table.append({"reorder": None, "value": None})

    def rid_2_str(self, rid):
        return "R" + str(rid)

    def rid_2_int(self, rid):
        return int(rid.split("R")[1])

    def printTable(self):
        print("Registers")
        for index, r in enumerate(self.table):
            value = "-"
            if r["value"] is not None:
                value = str(r["value"])
            robid = "-"
            if r["reorder"] is not None:
                robid = str(r["reorder"])
            p = self.rid_2_str(index) + " " + value + " " + robid
            print(p)  # needs update
        # print(self.table)

    def updateRegister(self, register_id, val, rob_id):
        self.table[self.rid_2_int(register_id)]["value"] = val
        if rob_id == self.table[self.rid_2_int(register_id)]["reorder"]:
            self.table[self.rid_2_int(register_id)]["reorder"] = None

    def reserveRegister(self, register_id, rob_id):
        self.table[self.rid_2_int(register_id)]["reorder"] = rob_id

    def __getitem__(self, rid):
        return self.table[self.rid_2_int(rid)]


if __name__ == "__main__":
    registers = RegisterTable(4)
    registers.printTable()
    registers.reserveRegister(2, "ROB1")
    registers.printTable()
    registers.printTable()
