import sys
import logging


log = logging.getLogger()
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
out_hdlr.setLevel(logging.INFO)
log.addHandler(out_hdlr)
log.setLevel(logging.INFO)


MEMORY_SIZE = 4096
REGISTERS_SIZE = 16


class Cpu:
    def __init__(self):
        registers_ops = {
            0x0: self.assign_registers,
            0x1: self.bitwise_or,
            0x2: self.bitwise_and,
            0x3: self.bitwise_xor,
            0x4: self.add_with_carry,
            0x5: self.substract_with_borrow,
            0x6: self.shift_right,
            0x7: self.reversed_substraction,
            0xE: self.shift_left
        }

        codes = {
            0x00E0: self.clear_display,
            0x00EE: self.return_subroutine,
            0x1: self.jump_subroutine,
            0x2: self.call_subroutine,
            0x3: self.skip_next_if_equal_address,
            0x4: self.skip_next_if_not_equal_address,
            0x5: self.skip_next_if_equal_register,
            0x6: self.set_register,
            0x7: self.add_register,
            0x8: self.registers_ops,
            0x9: self.skip_if_registers_not_equal,
            0xA: self.set_i_to_address_plus,
            0xB: self.jump_to_address_plus_i,
            0xC: self.set_bitwise_and_random,
            0xE: self.add_i_to_register,
        }

        self.stack_pointer = None
        self.memory = [0] * MEMORY_SIZE
        self.registers = [0] * REGISTERS_SIZE
        self.program_counter = 0x200
        self.stack = []
        self.memory_index = 0
        self.vx = 0
        self.vy = 0
        self.op_code = None

    def cycle(self):
        while self.program_counter <= len(self.memory):
            self.op_code = self.memory[self.program_counter]
            log.info('Extracted command = {}'.format(self.op_code))
            try:
                method = self.codes[self.op_code & 0xf000]
            except KeyError:
                log.error('Unknown command')
                raise TypeError("Command not implemented")
            else:
                if callable(method):
                    method()
                else:
                    method[self.op_code & 0x000f]()
                log.info('Called method {} with vx = {} and vy {}'.format(method, self.vx, self.vy))
            self.program_counter += 2

    def return_subroutine(self):
        self.program_counter = self.stack.pop()

    def jump_subroutine(self):
        jump_address = self.op_code & 0x0fff
        self.program_counter = jump_address

    def call_subroutine(self):
        self.stack.append(self.program_counter)
        self.program_counter = self.op_code & 0x0fff

    def skip_next_if_equal_address(self):
        register = self.op_code & 0x0f00
        compare = self.op_code & 0x00ff
        if self.registers[register] == compare:
            self.program_counter += 2

    def skip_next_if_not_equal_address(self):
        register = self.op_code & 0x0f00
        compare = self.op_code & 0x00ff
        if self.registers[register] != compare:
            self.program_counter += 2

    def skip_next_if_equal_register(self):
        register = self.op_code & 0x0f00
        compare = self.op_code & 0x00f0
        if self.registers[register] == self.registers[compare]:
            self.program_counter += 2

    def skip_if_not_equal_register(self):
        pass

    def set_register(self):
        register = self.op_code & 0x0f00
        value = self.op_code & 0x00ff
        self.registers[register] = value

    def add_register(self):
        register = self.op_code & 0x0f00
        value = self.op_code & 0x00ff
        self.registers[register] += value

    def bitwise_or(self):
        register = self.op_code & 0x0f00
        compare_or = self.op_code & 0x00ff
        self.registers[register] |= compare_or

    def bitwise_and(self):
        register = self.op_code & 0x0f00
        compare_and = self.op_code & 0x00ff
        self.registers[register] &= compare_and

    def bitwise_xor(self):
        register = self.op_code & 0x0f00
        compare_xor = self.op_code & 0x00ff
        self.registers[register] ^= compare_xor

    def shift_right(self):
        pass

    def shift_left(self):
        pass

    def add_with_carry(self):
        pass

    def substract_with_borrow(self):
        pass

    def reversed_substraction(self):
        pass

    def set_i_to_address_plus(self):
        pass

    def set_bitwise_and_random(self):
        pass

    def add_i_to_register(self):
        pass

    def set_i_location_sprite(self):
        pass
