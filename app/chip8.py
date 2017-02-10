from app import config


class Chip8:

    def __init__(self):
        self.flow_codes = {
            0x0: 'return_subroutine',
            0x1: 'jump_subroutine',
            0x2: 'call_subroutine'
        }
        self.cond_codes = {
            0x3: 'skip_next_if_equal_address',
            0x4: 'skip_next_if_not_equal',
            0x5: 'skip_next_if_equal_register',
            0x9: 'skip_if_not_equal_register'
        }
        self.const_codes = {
            0x6: 'set_register',
            0x7: 'add_register'
        }
        self.assign = {
            0x0: 'set_register_equal'
        }
        self.bit_ops = {
            0x1: 'bitwise_or',
            0x2: 'bitwise_and',
            0x3: 'bitwise_xor',
            0x6: 'shift_right',
            0xE: 'shift_left'
        }
        self.math = {
            0x4: 'add_with_carry',
            0x5: 'substract_with_borrow',
            0x7: 'reversed_substraction'
        }
        self.mem = {
            0xA: 'set_i_to_address_plus'
        }
        self.rand = {
            0xC: 'set_bitwise_and_random',
            0xE: 'add_i_to_register',
            0x29: 'set_i_location_sprite',
        }

        self.stack_pointer = None
        self.memory = bytearray(config.MEMORY_SIZE)
        self.registers = [0] * config.REGISTERS_SIZE
        self.program_counter = 0
        self.stack = []
        self.memory_index = 0

    def return_subroutine(self):
        pass

    def jump_subroutine(self):
        pass

    def call_subroutine(self):
        pass

    def skip_next_if_equal_address(self):
        pass

    def skip_next_if_not_equal(self):
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
