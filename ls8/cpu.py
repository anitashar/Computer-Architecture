"“”CPU functionality.“”"
import sys
#load “immediate”, store a value in a register, or “set this register to this value”.
LDI = 130 #10000010
#a pseudo-instruction that prints the numeric value stored in a register.
PRN = 71 #01000111
#halt the CPU and exit the emulator.
HLT = 1 #00000001
class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.running = True



    #_Memory Address Register_ (MAR)
    def ram_read(self, MAR):
        return self.ram[MAR]


    #_Memory Data Register_ (MDR)
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR
        return self.ram[MAR]

    def load(self):
        """Load a program into memory."""
        address = 0
        # For now, we’ve just hardcoded a program:
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]
        for instruction in program:
            self.ram[address] = instruction
            address += 1
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == “SUB”: etc
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
        while self.running:
        # Instruction Register - internal part of CPU that holds a value.  Special purpose part of CPU.
            IR = self.ram[self.pc]
            # Set the value of a register to an integer.
            if IR == LDI:
                operand_a = self.ram_read(self.pc +1)
                operand_b = self.ram_read(self.pc +2)
                self.reg[operand_a] = operand_b
                self.pc +=3
            elif IR == HLT:
                return False
            elif IR == PRN:
                operand_a = self.ram[self.pc +1]
                print(self.reg[operand_a])
                self.pc += 2
            else:
                print("ehh idk what to do")
                sys.exit(1)