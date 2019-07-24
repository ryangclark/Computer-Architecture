"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ops = {
            0b00000000: self.NOP,  #   0
            0b00000001: self.h,    #   1
            0b00010001: self.RET,  #  17
            0b01000101: self.PUSH, #  69
            0b01000110: self.POP,  #  70
            0b01000111: self.PRN,  #  71
            0b01010000: self.CALL, #  80
            0b10000010: self.LDI,  # 130
            0b10100000: self.ADD,  # 160
            0b10100010: self.MUL,  # 162
        }
        self.pc = 0
        self.ram = [0b00000000] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4 # Initialize Stack Pointer

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


    def h(self, message=0):
        if (message):
            self.trace()
        return sys.exit(message)


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

        while self.pc < 256:
            # self.trace()
            instructional_register = self.ram_read(self.pc)

            try:
                self.ops[instructional_register]()
            except KeyError as e:
                self.h(f'Error in cpu.run(): Command not recognized: {e}')
            
        print('Ran through all 256!')
        self.trace()
        return self.h()

    def ADD(self):
        ''' Add the value in two registers and 
            store the result in registerA.'''

        # Get Operands
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        # Call `alu()` function
        self.alu('ADD', operand_a, operand_b)
        # Increment PC
        self.pc += 3
        

    def CALL(self):
        ''' Calls a subroutine (function) 
            at the address stored in the register.'''

        # Decrement the `SP`
        self.reg[7] -= 1
        # Push Next Instruction Address to Stack
        self.ram_write(self.reg[7], self.pc + 2)

        # Get Operand
        register_address = self.ram_read(self.pc + 1)
        # Get Register Value
        register_value = self.reg[register_address]
        # Set PC to Register Value
        self.pc = register_value

        try:
            instructional_register = self.ram_read(self.pc)
            self.ops[instructional_register]()
        except KeyError as e:
            self.h(f'ERROR in cpu.CALL(): Command not recognized: {e}')


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


    def NOP(self):
        return


    def POP(self):
        '''Pop the value at the top of the stack into the given register.'''

        # Get Operand
        register_address = self.ram_read(self.pc + 1)
        # Get Value in RAM at SP Address
        stack_value = self.ram_read(self.reg[7])
        # Assign Stack Value to Register
        self.reg[register_address] = stack_value
        # Increment SP
        self.reg[7] += 1
        # Increment PC
        self.pc += 2


    def PRN(self):
        '''Print numeric value stored in the given register.'''

        # Get Operand
        register_address = self.ram_read(self.pc + 1)
        # Get Register Value
        register_value = self.reg[register_address]
        # Print
        print(register_value)
        # Increment PC
        self.pc += 2


    def PUSH(self):
        '''Push the value in the given register on the stack.'''

        # Decrement the `SP`
        self.reg[7] -= 1
        # Get Operand
        register_address = self.ram_read(self.pc + 1)
        # Get Register Value
        register_value = self.reg[register_address]
        # Assign Value to RAM at SP Address
        self.ram_write(self.reg[7], register_value)
        # Increment PC
        self.pc += 2


    def RET(self):
        '''Return from subroutine.'''

        # Get Value in RAM at SP Address
        stack_value = self.ram_read(self.reg[7])
        # Increment SP
        self.reg[7] += 1

        # Store Address in PC
        self.pc = stack_value

