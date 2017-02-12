import sys
import logging

from app import config


log = logging.getLogger(__name__)
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
out_hdlr.setLevel(logging.INFO)
log.addHandler(out_hdlr)
log.setLevel(logging.INFO)


class Chip8:

    def __init__(self):
        self.codes = {
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

        self.registers_ops = {
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

        self.stack_pointer = None
        self.memory = [0] * config.MEMORY_SIZE
        self.registers = [0] * config.REGISTERS_SIZE
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
        pass

    def jump_subroutine(self):
        pass

    def call_subroutine(self):
        pass

    def skip_next_if_equal_address(self):
        pass

    def skip_next_if_not_equal_address(self):
        pass

    def skip_next_if_equal_register(self):
        pass

    def skip_if_not_equal_register(self):
        pass

    def set_register(self):
        pass

    def add_register(self):
        pass

    def bitwise_or(self):
        pass

    def bitwise_and(self):
        pass

    def bitwise_xor(self):
        pass

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
