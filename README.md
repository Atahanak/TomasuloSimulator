# Tomasula Simulator

TomasuloSimulator is a runnable Python package for displaying the state of the CPU components in each cycle. 

## Usage

### Number of Registers & Instruction Window Size
Configure the size of the instruction window and the number of registers under **Parameters.txt**.

**Example:**
number_of_registers: 4
instruction_window_size: 4

### Functional Units
Configure the functional units and how many cycles it takes to execute under **Units.txt**.

**Example:**
0: ADD,SUB 1 # ADD/SUB UNIT
1: MUL 4     # MUL UNIT
2: MUL 4     # MUL UNIT
3: DIV 4     # DIV UNIT
4: LD,BGE 1  # INTEGER UNIT

### The program
Put the assembly program you want to execute in **Program.txt**.

**Example:**
0:  LD  R0, 0
4:  MUL R2, R0, 2
8:  MUL R1, R0, R0
12: SUB R3, R1, R2
16: DIV R1, 1, 16
20: SUB R2, R2, 2
24: ADD R3, R3, 1
28: DIV R2, R3, R2
32: SUB R0, R0, R2 
36: BGE R3, R1, 4

### How to run

```bash
python -m simulator
```