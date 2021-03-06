import sys
import logging
from random import randint

import pygame
from pygame import locals as key

from chip8.screen import Screen, white, black

log = logging.getLogger()
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
out_hdlr.setLevel(logging.INFO)
log.addHandler(out_hdlr)
log.setLevel(logging.INFO)

MEMORY_SIZE = 4096
REGISTERS_SIZE = 16


KEY_MAPPINGS = {
        key.K_0: 0x0,
        key.K_1: 0x1,
        key.K_2: 0x2,
        key.K_3: 0x3,
        key.K_4: 0x4,
        key.K_5: 0x5,
        key.K_6: 0x6,
        key.K_7: 0x7,
        key.K_8: 0x8,
        key.K_9: 0x9,
        key.K_a: 0xA,
        key.K_b: 0xB,
        key.K_c: 0xC,
        key.K_d: 0xD,
        key.K_e: 0xE,
        key.K_f: 0xF
    }

SOUND = ""


class Cpu:
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
            0xD: self.draw_sprite,
            0xE: self.key_ops,
            0xF: self.mem_ops
        }

        self.registers_ops = {
            0x0: self.assign_registers,
            0x1: self.bitwise_or,
            0x2: self.bitwise_and,
            0x3: self.bitwise_xor,
            0x4: self.add_with_carry,
            0x5: self.subtract_with_borrow,
            0x6: self.shift_right,
            0x7: self.reversed_subtraction,
            0xE: self.shift_left
        }

        self.key_ops = {
            0xE: self.skip_if_vx_pressed,
            0x1: self.skip_if_not_vx_pressed,
        }

        self.mem_ops = {
            0x07: self.set_register_to_timer,
            0x0A: self.load_key_pressed,
            0x15: self.set_delay_timer,
            0x18: self.set_sound_timer,
            0x1E: self.add_to_memory_index,
            0x29: self.set_memory_index_to_sprite,
            0x33: self.store_binary_coded_decimal,
            0x55: self.dump_registers,
            0x65: self.load_registers
        }

        self.timers = {
            'delay': 0,
            'sound': 0
        }

        self.fonts = (0xF0, 0x90, 0x90, 0x90, 0xF0,
                      0x20, 0x60, 0x20, 0x20, 0x70,
                      0xF0, 0x10, 0xF0, 0x80, 0xF0,
                      0xF0, 0x10, 0xF0, 0x10, 0xF0,
                      0x90, 0x90, 0xF0, 0x10, 0x10,
                      0xF0, 0x80, 0xF0, 0x10, 0xF0,
                      0xF0, 0x80, 0xF0, 0x90, 0xF0,
                      0xF0, 0x10, 0x20, 0x40, 0x40,
                      0xF0, 0x90, 0xF0, 0x90, 0xF0,
                      0xF0, 0x90, 0xF0, 0x10, 0xF0,
                      0xF0, 0x90, 0xF0, 0x90, 0x90,
                      0xE0, 0x90, 0xE0, 0x90, 0xE0,
                      0xF0, 0x80, 0x80, 0x80, 0xF0,
                      0xE0, 0x90, 0x90, 0x90, 0xE0,
                      0xF0, 0x80, 0xF0, 0x80, 0xF0,
                      0xF0, 0x80, 0xF0, 0x80, 0x80
                      )

        self.stack_pointer = None
        self.memory = [0] * MEMORY_SIZE
        self.registers = [0] * REGISTERS_SIZE
        self.program_counter = 0x200
        self.stack = []
        self.memory_index = 0
        self.vx = 0
        self.vy = 0
        self.op_code = None

        for index, font in enumerate(self.fonts):
            self.memory[index] = self.fonts[index]

        self.display = Screen()
        pygame.mixer.music.load(SOUND)

    def load_rom(self, path):
        with open(path, 'rb') as rom:
            byte = rom.read()
            index = 0
            while byte is not None:
                self.memory[index] = byte
                byte = rom.read()
                index += 1

    def cycle(self):
        while self.program_counter <= len(self.memory):
            self.op_code = self.memory[self.program_counter]
            log.info('Extracted command = {}'.format(self.op_code))
            method = self.codes.get(self.op_code, None)
            if not method:
                try:
                    method_code = (self.op_code & 0xf000) >> 12
                    method = self.codes[method_code]
                except KeyError:
                    log.error('Unknown command')
                    raise TypeError("Command not implemented")
                else:
                    self.vx = (self.op_code & 0x0f00) >> 8
                    self.vy = (self.op_code & 0x00f0) >> 4
                    if callable(method):
                        method()
                    elif self.op_code & 0xf000 == 0xE:
                        method[method_code][self.op_code & 0x00ff]()
                    else:
                        method[method_code][self.op_code & 0x000f]()
                    log.info('Called method {} with vx = {} and vy {}'.format(method, self.vx, self.vy))
            elif callable(method):
                method()
            self.program_counter += 2
            for timer in self.timers:
                if self.timers[timer] > 0:
                    self.timers[timer] -= 1
                    if timer == 'sound' and self.timers[timer] == 0:
                        pygame.mixer.music.play(0)

    def clear_display(self):
        self.display.clear()

    def return_subroutine(self):
        self.program_counter = self.stack.pop()

    def jump_subroutine(self):
        jump_address = self.op_code & 0x0fff
        self.program_counter = jump_address

    def call_subroutine(self):
        self.stack.append(self.program_counter)
        self.program_counter = self.op_code & 0x0fff

    def skip_next_if_equal_address(self):
        compare = self.op_code & 0x00ff
        if self.registers[self.vx] == compare:
            self.program_counter += 2

    def skip_next_if_not_equal_address(self):
        compare = self.op_code & 0x00ff
        if self.registers[self.vx] != compare:
            self.program_counter += 2

    def skip_next_if_equal_register(self):
        if self.registers[self.vx] == self.registers[self.vy]:
            self.program_counter += 2

    def set_register(self):
        value = self.op_code & 0x00ff
        self.registers[self.vx] = value

    def add_register(self):
        value = self.op_code & 0x00ff
        self.registers[self.vx] += value

    def assign_registers(self):
        self.registers[self.vx] = self.registers[self.vy]

    def bitwise_or(self):
        compare_or = self.op_code & 0x00ff
        self.registers[self.vx] |= compare_or

    def bitwise_and(self):
        compare_and = self.op_code & 0x00ff
        self.registers[self.vx] &= compare_and

    def bitwise_xor(self):
        compare_xor = self.op_code & 0x00ff
        self.registers[self.vx] ^= compare_xor

    def shift_right(self):
        self.registers[0xf] = self.registers[self.vx] % 2
        self.registers[self.vx] <<= 1
        self.registers[self.vx] /= 2

    def shift_left(self):
        self.registers[0xf] = self.registers[self.vx] >> 8
        self.registers[self.vx] >>= 1
        self.registers[self.vx] *= 2

    def add_with_carry(self):
        if self.registers[self.vx] + self.registers[self.vy] > 0xff:
            self.registers[self.vx] = 0
            self.registers[0xf] = 1
        else:
            self.registers[self.vx] += self.registers[self.vy]

    def subtract_with_borrow(self):
        if self.registers[self.vx] - self.registers[self.vy] < 0:
            self.registers[self.vx] = 0
            self.registers[0xf] = 1
        else:
            self.registers[self.vx] -= self.registers[self.vy]

    def reversed_subtraction(self):
        if self.registers[self.vy] - self.registers[self.vx] < 0:
            self.registers[self.vy] = 0
            self.registers[0xf] = 1
        else:
            self.registers[self.vy] = self.registers[self.vx] - self.registers[self.vy]

    def skip_if_registers_not_equal(self):
        if self.registers[self.vx] != self.registers[self.vy]:
            self.program_counter += 2

    def set_i_to_address_plus(self):
        self.memory_index = self.op_code & 0x0fff

    def jump_to_address_plus_i(self):
        self.program_counter = self.op_code[0] + self.op_code & 0x0fff

    def set_bitwise_and_random(self):
        bitwise_and = self.op_code & 0x00ff
        self.registers[self.vx] = bitwise_and & randint(0, 255)

    def load_key_pressed(self):
        pressed = None
        while not pressed:
            event = pygame.event.poll()
            pressed = KEY_MAPPINGS.get(event.type, None)
        self.vx = pressed

    def set_memory_index_to_sprite(self):
        self.memory_index = 5 * (self.memory[self.vx]) & 0xfff

    def store_binary_coded_decimal(self):
        bcd = self.vx
        self.memory[self.memory_index] = self.vx // 100
        bcd -= self.memory[self.memory_index] * 100
        self.memory[self.memory_index + 1] = bcd // 10
        bcd -= self.memory[self.memory_index + 1] * 10
        self.memory[self.memory_index + 2] = bcd

    def draw_sprite(self):
        self.registers[0xf] = 0
        height = self.op_code & 0x000f
        for i in range(height):
            for bit in bin(self.memory_index + i)[:2]:
                if bit:
                    self.display.set_pixel(self.vx, self.vy)

    def skip_if_vx_pressed(self):
        event = pygame.event.poll()
        pressed = KEY_MAPPINGS.get(event.type, None)
        if self.vx == pressed:
            self.program_counter += 2

    def skip_if_not_vx_pressed(self):
        event = pygame.event.poll()
        pressed = KEY_MAPPINGS.get(event.type, None)
        if self.vx != pressed:
            self.program_counter += 2

    def set_register_to_timer(self):
        self.registers[self.vx] = self.timers['delay']

    def set_delay_timer(self):
        self.timers['delay'] = self.registers[self.vx]

    def set_sound_timer(self):
        self.timers['sound'] = self.registers[self.vx]

    def add_to_memory_index(self):
        self.memory_index += self.registers[self.vx]

    def dump_registers(self):
        for register in self.registers:
            self.memory[self.memory_index] = register
            self.memory_index += 1

    def load_registers(self):
        for register in range(len(self.registers)):
            self.registers[register] = self.memory[self.memory_index]
