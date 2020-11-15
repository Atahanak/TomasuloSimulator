class CommonDataBus:
    def __init__(self, capacity=1):
        self.Capacity = capacity
        self.slots = []
    
    def check_availability(self):
        if len(self.slots) < self.Capacity:
            return True
        else:
            return False
    
    def add_result(self, rob_id, value):
        if len(self.slots) >= self.Capacity:
            raise 'trying to overfill cdb'
        self.slots.append([rob_id, value])
    
    def get_result(self, rob_id):
        for item in self.slots:
            if item[0] == rob_id:
                return item[1]
        return False
    
    def clear_cbd(self):
        self.slots = []
