import argparse

from chip8.cpu import Cpu


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run chip8 rom')
    parser.add_argument('path', nargs='*', help='rom path')
    args = parser.parse_args()
    cpu = Cpu()
    cpu.load_rom(args.path)
