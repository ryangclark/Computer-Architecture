"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0b00000000] * 32
        self.reg = [0] * 8

    def load(self):
        """Load a program into memory."""

        address = 0

        with open(sys.argv[1]) as f:
            line = f.readline()
            while line and address < 32:
                if (line[0] == '0' or line[0] == '1'):
                    self.ram[address] = int(line[0:8], base=2)
                    address += 1

                line = f.readline()

        # print('self.ram', self.ram)


    def h(self):
        return sys.exit()


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""

        ops = {
            0b01000111: self.PRN,
            0b10000010: self.LDI,
            0b10100010: self.MUL,
        }

        while self.pc < 32:
            # self.trace()
            instructional_register = self.ram_read(self.pc)

            if (instructional_register == 0b00000001):
                break
            # print('instructional_register', instructional_register, self.pc)
            ops[instructional_register]()

        return self.h()


    def LDI(self):
        '''Set the value of a register to an integer.'''

        # Get Operands
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        # Set Requested Register to Value
        self.reg[operand_a] = operand_b
        # Increment PC
        self.pc += 3


    def MUL(self):
        ''' Multiply the values in two registers together 
            and store the result in registerA.'''

        # Get Operands
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        # Call `alu()` function
        self.alu('MUL', operand_a, operand_b)
        # Increment PC
        self.pc += 3
        # print(self.pc)


    def PRN(self):
        '''Print numeric value stored in the given register.'''

        # Get Operand
        register_address = self.ram_read(self.pc + 1)
        # Get Register
        register_value = self.reg[register_address]
        # Print
        print(register_value)
        # Increment PC
        self.pc += 2

