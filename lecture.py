import sys

# a simple data-driven machine that reads instructions out of memory
# and executes them

PRINT_HI = 1
HALT = 2
PRINT_NUM = 3
SAVE = 4 # save a value to a register
PRINT_REGISTER = 5 # prints the value of a register
ADD = 6 # adds values from two registers x, y and stores it in register x

pc = 0 # program counter - points to the instruction we're currently executing
running = True

memory = [
    PRINT_HI, # prints hi
    SAVE, # saves 65 into register 2
    65,
    2,
    SAVE, # saves 20 into register 3
    20,
    3,
    ADD, # take values in reg2 (65) and reg3 (20) and store the sum in reg2 (85)
    2,
    3,
    PRINT_REGISTER, # print 85
    2,
    HALT # stop the program
]

registers = [0] * 8

while running:
    commandToExecute = memory[pc]

    if commandToExecute == PRINT_HI:
        print("hi")
        pc += 1
    elif commandToExecute == HALT:
        running = False
    elif commandToExecute == PRINT_NUM:
        numToPrint = memory[pc + 1]
        print(numToPrint)
        pc += 2
    elif commandToExecute == PRINT_REGISTER:
        reg = memory[pc + 1]
        print(registers[reg])
        pc += 2
    elif commandToExecute == SAVE:
        numToSave = memory[pc + 1]
        registerToSaveItIn = memory[pc + 2]
        registers[registerToSaveItIn] = numToSave
        pc += 3
    elif commandToExecute == ADD:
        regA = memory[pc + 1]
        regB = memory[pc + 2]
        sumOfRegisters = registers[regA] + registers[regB]
        registers[regA] = sumOfRegisters
        pc += 3
    else:
        print("ehh idk what to do")
        sys.exit(1)
