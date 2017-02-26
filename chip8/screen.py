import pygame


white = (255, 255, 255)
black = (0, 0, 0)


class Screen:
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
