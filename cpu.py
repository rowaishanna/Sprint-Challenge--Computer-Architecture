"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # store the filename given in the command line
        self.filename = sys.argv[1]
        # ram stores the istructions
        self.ram = [0] * 256
        # stores the values
        self.reg = [0] * 8
        # has a pointer that points to our ram address
        self.pc = 0
        # halter
        self.halt = False
        # stack pointer
        self.sp = 0xf4
        # store stack pointer in reg7
        self.reg[7] = self.sp
        # flags
        self.flag = 0b00000000

        self.instructions = {
                                'LDI': 0b10000010, 
                                'PRN': 0b01000111,
                                'HLT': 0b00000001,
                                'MULT': 0b10100010,
                                'PUSH': 0b01000101,
                                'POP': 0b01000110,
                                'CALL': 0b01010000,
                                'RET': 0b00010001,
                                'ADD': 0b10100000,
                                'CMP': 0b10100111,
                                'JEQ': 0b01010101,
                                'JNE': 0b01010110,
                                'JMP': 0b01010100,
                                'AND': 0b10101000,
                                'OR': 0b10101010,
                                'XOR': 0b10101011,
                                'NOT': 0b01101001,
                                'SHL': 0b10101100,
                                'SHR': 0b10101101,
                                'MOD': 0b10100100
                            }

    def load(self, filename = 'No File'):
        """Load a program into memory."""
        # load the file given in the command line
        filename = self.filename
        # create a set of numbers
        nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        # nums = set(nums)
        address = 0
        # get the file type
        file_type = filename.split('.')[1]

        if file_type != 'ls8':
            print(f'ERROR: {filename} is not an ls8 file')
        else:
            # read in the instructions into ram
            with open(filename, 'r') as f:
                for line in f:
                    # get rid of leading and trailing spaces
                    line = line.strip()
                    # if the first value is a number
                    if len(line) > 0:
                        if line[0] in nums:
                            # get the number by itself
                            line = line.split(' ')
                            value = int(line[0], 2)
                            # add it to the ram
                            self.ram[address] = value
                            address += 1      

        


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")
    
    # read a value from ram
    def ram_read(self, pc):
        return self.ram[pc]

    # write a value to ram
    def ram_write(self, pc, value):
        self.ram[pc] = value

    # write a value to reg
    def ldi(self):
        '''
        LDI register immediate
        Set the value of a register to an integer.
        '''
        # get the register
        register = self.ram[self.pc+1]
        # get the value
        value = self.ram[self.pc+2]
        # store value in register
        self.reg[register] = value
        # move up 3 indexes in ram
        self.pc += 3
    
    # print a value from reg
    def prn(self):
        '''
        PRN register pseudo-instruction
        Print numeric value stored in the given register.
        Print to the console the decimal integer value that is stored in the given register.
        '''
        # get the index to print from ram
        index = self.ram[self.pc+1]
        # print the value at index in reg
        print(self.reg[index])
        # move up 2 indexes in ram
        self.pc += 2

    # multiply two values stored in the register
    def mult(self):
        idx_a = self.ram[self.pc+1]
        idx_b = self.ram[self.pc+2]
        product = self.reg[idx_a] * self.reg[idx_b]
        self.reg[idx_a] = product
        self.pc += 3

    def add(self):
        idx_a = self.ram[self.pc+1]
        idx_b = self.ram[self.pc+2]
        total = self.reg[idx_a] + self.reg[idx_b]
        self.reg[idx_a] = total
        self.pc += 3

    # cmp
    def cmp(self):
        '''
        Compare the values in two registers.
        If they are equal, set the Equal E flag to 1, otherwise set it to 0.
        If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.
        If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.
        '''
        # get the indexes of the registers
        idx_a = self.ram[self.pc+1]
        idx_b = self.ram[self.pc+2]
        # get the values from the registers
        val_a = self.reg[idx_a]
        val_b = self.reg[idx_b]
        # L
        if val_a < val_b:
            # set the flag
            self.flag = 0b00000100
        # G
        elif val_a > val_b:
            self.flag = 0b00000010
        # E
        elif val_a == val_b:
            self.flag = 0b00000001

        # increment the ram pointer by 3
        self.pc += 3

    def jeq(self):
        '''
        If equal flag is set (true), jump to the address stored in the given register.
        '''
        if self.flag == 0b00000001:
            # get the register index
            index = self.ram[self.pc+1]
            # use it to get the address
            address = self.reg[index]
            # set the pc to the address
            self.pc = address
        else:
            self.pc += 2

    def jne(self):
        '''
        If E flag is clear (false, 0), jump to the address stored in the given register.
        '''
        if self.flag != 0b00000001:
            # get the register index
            index = self.ram[self.pc+1]
            # use it to get the address
            address = self.reg[index]
            # set the pc to the address
            self.pc = address
        else:
            self.pc += 2
    
    def jmp(self):
        '''
        Jump to the address stored in the given register.
        Set the PC to the address stored in the given register.
        '''
        # get the register index
        index = self.ram[self.pc+1]
        # use it to get the address
        address = self.reg[index]
        # Set the pc to the address
        self.pc = address

    def bit_and(self):
        '''
        Bitwise-AND the values in registerA and registerB, then store the result in registerA.
        '''
        # get the indexes of the registers from ram
        idx_a = self.ram[self.pc+1]
        idx_b = self.ram[self.pc+2]
        # get the values held in the registers
        value_a = self.reg[idx_a]
        value_b = self.reg[idx_b]
        # convert them to binary strings
        bin_a = bin(value_a)[2:]
        bin_b = bin(value_b)[2:]
        # zeroes value
        z = ''
        # combined value
        c = ''
        # make sure the binary numbers are the same length
        # if b is shorter than a
        if len(bin_a) > len(bin_b):
            for i in range(0, (len(bin_a)-len(bin_b))):
                z = z + '0'
            # add zeroes to the front of b
            bin_b = z + bin_b

        # if a is shorter than b
        if len(bin_a) < len(bin_b):
            for i in range(0, (len(bin_b)-len(bin_a))):
                z = z + '0'
            # add zeroes to the front of a
            bin_a = z + bin_a
        
        # once a and b have equal lengths
        if len(bin_a) == len(bin_b):   
            # loop through each value
            for i in range(0, len(bin_a)):
                if bin_a[i] == '1' and bin_b[i] == '1':
                    c = c + '1'
                else:
                    c = c + '0'

        # cast the binary string to binary int
        c = int(c, 2)
        # store the result in register idx_a
        self.reg[idx_a] = c
        # increment the ram pointer
        self.pc += 3
    
    def bit_or(self):
        '''
        Perform a bitwise-OR between the values in registerA and registerB, 
        storing the result in registerA.
        '''
        # get the indexes of the registers from ram
        idx_a = self.ram[self.pc+1]
        idx_b = self.ram[self.pc+2]
        # get the values held in the registers
        value_a = self.reg[idx_a]
        value_b = self.reg[idx_b]
        # convert them to binary strings
        bin_a = bin(value_a)[2:]
        bin_b = bin(value_b)[2:]
        # zeroes value
        z = ''
        # combined value
        c = ''
        # make sure the binary numbers are the same length
        # if b is shorter than a
        if len(bin_a) > len(bin_b):
            for i in range(0, (len(bin_a)-len(bin_b))):
                z = z + '0'
            # add zeroes to the front of b
            bin_b = z + bin_b

        # if a is shorter than b
        if len(bin_a) < len(bin_b):
            for i in range(0, (len(bin_b)-len(bin_a))):
                z = z + '0'
            # add zeroes to the front of a
            bin_a = z + bin_a
        
        # once a and b have equal lengths
        if len(bin_a) == len(bin_b):   
            # loop through each value
            for i in range(0, len(bin_a)):
                if bin_a[i] == '1' or bin_b[i] == '1':
                    c = c + '1'
                else:
                    c = c + '0'

        # cast the binary string to binary int
        c = int(c, 2)
        # store the result in register idx_a
        self.reg[idx_a] = c
        # increment the ram pointer
        self.pc += 3

    def xor(self):
        '''
        Perform a bitwise-XOR between the values in registerA and registerB, 
        storing the result in registerA.
        '''
        # get the indexes of the registers from ram
        idx_a = self.ram[self.pc+1]
        idx_b = self.ram[self.pc+2]
        # get the values held in the registers
        value_a = self.reg[idx_a]
        value_b = self.reg[idx_b]
        # convert them to binary strings
        bin_a = bin(value_a)[2:]
        bin_b = bin(value_b)[2:]
        # zeroes value
        z = ''
        # combined value
        c = ''
        # make sure the binary numbers are the same length
        # if b is shorter than a
        if len(bin_a) > len(bin_b):
            for i in range(0, (len(bin_a)-len(bin_b))):
                z = z + '0'
            # add zeroes to the front of b
            bin_b = z + bin_b

        # if a is shorter than b
        if len(bin_a) < len(bin_b):
            for i in range(0, (len(bin_b)-len(bin_a))):
                z = z + '0'
            # add zeroes to the front of a
            bin_a = z + bin_a
        
        # once a and b have equal lengths
        if len(bin_a) == len(bin_b):   
            # loop through each value performing xor logic
            for i in range(0, len(bin_a)):
                if bin_a[i] == '1' and bin_b[i] == '0':
                    c = c + '1'
                elif bin_a[i] == '0' and bin_b[i] == '1':
                    c = c + '1'
                else:
                    c = c + '0'

        # cast the binary string to binary int
        c = int(c, 2)
        # store the result in register idx_a
        self.reg[idx_a] = c
        # increment the ram pointer
        self.pc += 3
    
    def bit_not(self):
        '''
        Perform a bitwise-NOT on the value in a register, 
        storing the result in the register.
        '''
        # get the register index
        index = self.ram[self.pc+1]
        # get the value from the register index
        value = self.reg[index]
        # set the value to its compliment
        value = ~value
        # store it in the same register
        self.reg[index] = value
        # increment the ram pointer
        self.pc += 2

    def shl(self):
        '''
        Shift the value in registerA left by the number of bits specified in registerB,
        filling the low bits with 0.
        '''
        # get indices
        idx_a = self.ram[self.pc+1]
        idx_b = self.ram[self.pc+2]
        # get values
        a = self.reg[idx_a]
        b = self.reg[idx_b]
        # turn a into a binary string
        a = bin(a)[2:]
        # create an empty string to hold 0's
        c = ''
        d = ''
        # loop through range of b adding 0's to c
        for i in range(0, 8-len(a)):
            c = c + '0'
        for i in range(0, b):
            d = d + '0'
        # combine a and c
        a = c + a
        # cut off the right end of a
        a = a + d
        a = a[b:]
        # store it in register a as a binary int
        self.reg[idx_a] = int(a, 2)
        # increment ram pointer
        self.pc += 3
    
    def shr(self):
        '''
        Shift the value in registerA right by the number of bits specified in registerB,
        filling the high bits with 0.
        '''
        # get indices
        idx_a = self.ram[self.pc+1]
        idx_b = self.ram[self.pc+2]
        # get values
        a = self.reg[idx_a]
        b = self.reg[idx_b]
        # turn a into a binary string
        a = bin(a)[2:]
        # create an empty string to hold 0's
        c = ''
        d = ''
        # loop through range of b adding 0's to c
        for i in range(0, 8-(len(a))):
            c = c + '0'
        for i in range(0, b):
            d = d + '0'
        # combine a and c
        a = c + a
        # cut off the right end of a
        a = d + a
        a = a[:-b]
        # store it in register a binary int
        self.reg[idx_a] = int(a, 2)
        # increment ram pointer
        self.pc += 3

    def mod(self):
        '''
        Divide the value in the first register by the value in the second, 
        storing the remainder of the result in registerA.
        If the value in the second register is 0, 
        the system should print an error message and halt.
        '''
        # get the indices
        idx_a = self.ram[self.pc+1]
        idx_b = self.ram[self.pc+2]
        # get the values
        a = self.reg[idx_a]
        b = self.reg[idx_b]
        # check exceptions
        if b == 0:
            print('ERROR: value b = 0')
            self.hlt()
        # get the modulus
        c = a % b
        # store it at index a in register
        self.reg[idx_a] = c
        # increment the ram pointer
        self.pc += 3

    # push
    def push(self):
        '''
        PUSH register
        Push the value in the given register on the stack.
        Decrement the SP.
        Copy the value in the given register to the address pointed to by SP.
        '''
        ### HANDLE EXCEPTIONS ###
        ### STACK OVERFLOW?? ###
        # get the stack pointer minus 1
        pointer = self.sp-1
        # get the register index holding the value
        index = self.ram[self.pc+1]
        # get the value from the register
        value = self.reg[index]
        # write to ram
        self.ram_write(pointer, value)
        # decrement stack pointer
        self.sp-=1
        # increment ram pointer
        self.pc+=2
    
    # helper function push_value
    def push_value(self, value):
        # get the stack pointer minus 1
        pointer = self.sp-1
        # write to ram
        self.ram_write(pointer, value)
        # decrement stack pointer
        self.sp-=1


    # pop
    def pop(self):
        '''
        POP register
        Pop the value at the top of the stack into the given register.
        Copy the value from the address pointed to by SP to the given register.
        Increment SP.
        '''
        ### HANDLE EXCEPTIONS ###
        # get the stack pointer
        pointer = self.sp
        # get the register index that WILL hold the value
        index = self.ram[self.pc+1]
        # get the value from ram
        value = self.ram[pointer]
        # store it in reg
        self.reg[index] = value
        # increment stack pointer
        self.sp+=1
        # increment ram pointer 
        self.pc+=2
    
    # helper function for ret
    def pop_value(self):
        # get the stack pointer
        pointer = self.sp
        # get the value 
        value = self.ram[pointer]

        # increment the stack pointer
        self.sp += 1

        return value
        

    def call(self):
        '''
        Calls a subroutine (function) at the address stored in the register.
        The address of the instruction directly after CALL is pushed onto the stack. 
        This allows us to return to where we left off when the subroutine finishes executing.
        The PC is set to the address stored in the given register. 
        We jump to that location in RAM and execute the first instruction in the subroutine. 
        The PC can move forward or backwards from its current location.
        '''
        # get address of the next instruction after call
        return_add = self.pc + 2

        # push it on the stack
        self.push_value(return_add)

        # get subroutine address from register
        reg_num = self.ram[self.pc + 1]
        subroutine_add = self.reg[reg_num]

        # jump to the subroutine
        self.pc = subroutine_add
    
    def ret(self):
        # get return address from top of stack
        return_add = self.pop_value()

        # store it in as the ram pointer
        self.pc = return_add


    
    # stop the run of the CPU
    def hlt(self):
        '''
        Halt the CPU (and exit the emulator).
        '''
        self.halt = True

    # useful for debugging
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X %02X | %02X %02X %02X |" % (
            self.pc,
            self.flag,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        while self.halt == False:
            self.trace()
            # get the command
            instruction = self.ram[self.pc]

            # LDI
            if instruction == self.instructions['LDI']:
                self.ldi()

            # PRN
            elif instruction == self.instructions['PRN']:
                self.prn()
            
            # MULT
            elif instruction == self.instructions['MULT']:
                self.mult()
            
            # ADD
            elif instruction == self.instructions['ADD']:
                self.add()

            # CMP
            elif instruction == self.instructions['CMP']:
                self.cmp()
            
            # JEQ
            elif instruction == self.instructions['JEQ']:
                self.jeq()

            # JNE
            elif instruction == self.instructions['JNE']:
                self.jne()

            # JMP
            elif instruction == self.instructions['JMP']:
                self.jmp()

            # AND
            elif instruction == self.instructions['AND']:
                self.bit_and()

            # OR
            elif instruction == self.instructions['OR']:
                self.bit_or()

            # XOR
            elif instruction == self.instructions['XOR']:
                self.xor()
            
            # NOT
            elif instruction == self.instructions['NOT']:
                self.bit_not()

            # SHL
            elif instruction == self.instructions['SHL']:
                self.shl()

            # SHR
            elif instruction == self.instructions['SHR']:
                self.shr()

            # MOD
            elif instruction == self.instructions['MOD']:
                self.mod()

            # PUSH
            elif instruction == self.instructions['PUSH']:
                self.push()

            # POP
            elif instruction == self.instructions['POP']:
                self.pop()

            # CALL
            elif instruction == self.instructions['CALL']:
                self.call()

            # RET
            elif instruction == self.instructions['RET']:
                self.ret()

            # HLT    
            elif instruction == self.instructions['HLT']:
                # print(self.sp - 1)
                self.hlt()

            else:
                print(f'unrecognized instruction: {bin(instruction)}')
                break