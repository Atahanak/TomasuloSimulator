ISA = {'ADD': lambda x,y,z: x+y, 'SUB':lambda x,y,z: x-y, 'MUL':lambda x,y,z: x*y,'DIV':lambda x,y,z: x/y, 'LD':lambda x,y,z: x, 'BGE': lambda x,y,z: True if x>=y else z}

BRANCH_OPERATIONS = ["BGE", "BLE"]
LOAD_OPERATIONS = ['LD']
FP_OPERATIONS = ['SUB','MUL','DIV']
