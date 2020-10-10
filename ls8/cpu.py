"“”CPU functionality.“”"
import sys
# #load “immediate”, store a value in a register, or “set this register to this value”.
# LDI = 130 #10000010
# #a pseudo-instruction that prints the numeric value stored in a register.
# PRN = 71 #01000111
# #halt the CPU and exit the emulator.
# HLT = 1 #00000001
ADD = 0b10100000
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH =0b01000101   # Push in stack
POP = 0b01000110    # Pop from stack
CALL =0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.halted = False
        self.FL = 0b00000000

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, val):
        self.ram[address] = val



    def load(self):
        """Load a program into memory."""
     
        # # For now, we’ve just hardcoded a program:
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        # load an .ls8 file given the filename passed in as an argument
        file_name = sys.argv[1]

        try:
            address = 0
            with open(file_name) as file:
                for line in file:
                    split_line = line.split('#')[0]
                    command = split_line.strip()

                    if command == '':
                        continue

                    instruction = int(command, 2)
                    self.ram[address] = instruction
                    address += 1

        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} file was not found')
            sys.exit()


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.FL = 0b00000100
            if self.reg[reg_a] > self.reg[reg_b]:
                self.FL = 0b00000010
            if self.reg[reg_a] == self.reg[reg_b]:
                self.FL = 0b00000001
        
        else:
            raise Exception("Unsupported ALU operation")
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')
        for i in range(8):
            print(f"%02X" % self.reg[i], end='')
        print()
    def run(self):
        """Run the CPU."""
        
        while not self.halted:
            instruction_to_execute = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            self.execute_instruction(instruction_to_execute, operand_a, operand_b)

    def execute_instruction(self, instruction, operand_a, operand_b):
        if instruction == HLT:
            self.halted = True
            self.pc += 1
        elif instruction == LDI:
            self.reg[operand_a] = operand_b
            self.pc += 3
        elif instruction == PRN:
            print(self.reg[operand_a])
            self.pc += 2

        elif instruction == ADD:
            self.alu("ADD", operand_a, operand_b)
            self.pc += 3

        elif instruction == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

        elif instruction == PUSH:
                # decrement stack pointer
                self.reg[7] -= 1

                # get the value from a given register
                # reg_a = self.ram[self.pc+1]
                value = self.reg[operand_a]

                # put it on the stack pointer address
                sp = self.reg[7]
                self.ram[sp] = value

                # increment pc
                self.pc += 2

        elif instruction == POP:
                # get the stack pointer
                sp = self.reg[7]
                # get register number to put value in
                # reg_a = self.ram[self.pc+1]

                # use stack pointer to get the value
                value = self.ram[sp]
                # put the value into a given register
                self.reg[operand_a] = value

                # increment stack pointer
                self.reg[7] += 1
                # increment program counter
                self.pc += 2
        elif instruction == CALL:
                # get register number
                # reg_a = self.ram[self.pc + 1]
                # get the address to jump to, from the register
                address = self.reg[operand_a]
                # push command right after CALL onto the stack
                return_address = self.pc + 2
                # decrement stack pointer
                self.reg[7] -= 1
                sp = self.reg[7]
                # put return_address on the stack
                self.ram[sp] = return_address
                # then look at register, jump to that address
                self.pc = address
            
        elif instruction == RET:
                # pop the return address off the stack
                sp = self.reg[7]
                return_address = self.ram[sp]
                self.reg[7] += 1
                # go to return address: set the pc to return address
                self.pc = return_address

        elif instruction == CMP:
            self.alu("CMP", operand_a, operand_b)
            self.pc += 3

        elif instruction == JMP:
            #get the address from register
            register_number = self.ram_read(self.pc + 1)
            #set pc to address
            self.pc = self.reg[register_number]
        elif instruction == JEQ:
            if self.FL == 0b00000001:
                register_number = self.ram_read(self.pc +1)
                self.pc = self.reg[register_number]
            else:
                self.pc += 2

        elif instruction == JNE:
            if self.FL != 0b00000001:
                register_number = self.ram_read(self.pc +1)
                self.pc = self.reg[register_number]
            else:
                self.pc += 2
          
        else:
            print("ehh idk what to do")
            sys.exit(1)