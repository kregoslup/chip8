import pygame


white = (255, 255, 255)
black = (0, 0, 0)


class Screen:
    BLANK_SCREEN = white

    def __init__(self, width=640, height=480):
        pygame.init()
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((width, height))
        self.font = pygame.font.SysFont('Arial', 25)
        pygame.display.set_caption('Chip8')
        self.screen = pygame.display.set_mode((600, 400), 0, 32)
        self.screen.fill((white,))
        pygame.display.update()

    def clear(self):
        self.screen.fill((white,))

    def is_pixel_set(self, height, width):
        return pygame.Color(*white) != self.display.get_surface().get_at((height, width))

    def set_pixel(self, height, width):
        self.display.get_surface().set_at((height, width), pygame.Color(*black))
        self.display.update()
