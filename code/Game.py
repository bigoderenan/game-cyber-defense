import pygame

from code.Const import FPS, WIN_HEIGHT, WIN_WIDTH
from code.Level import Level
from code.Menu import Menu


class Game:
    def __init__(self):
        pygame.display.init()
        pygame.font.init()
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption('Cyber Defense')
        self.clock = pygame.time.Clock()
        self.menu = Menu()
        self.level = None
        self.state = 'menu'
        self.running = True

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.state == 'menu':
                    self.running = False
                else:
                    self.state = 'menu'
            elif event.key == pygame.K_RETURN and self.state != 'playing':
                self.level = Level()
                self.state = 'playing'

    def run(self):
        while self.running:
            seconds = min(self.clock.tick(FPS) / 1000, 0.05)
            for event in pygame.event.get():
                self.handle_event(event)
            if not self.running:
                break
            if self.state == 'playing':
                keys = pygame.key.get_pressed()
                horizontal = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(
                    keys[pygame.K_LEFT] or keys[pygame.K_a])
                vertical = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(
                    keys[pygame.K_UP] or keys[pygame.K_w])
                self.level.update(seconds, horizontal, vertical, keys[pygame.K_SPACE])
                self.state = self.level.state
                self.level.draw(self.window)
            else:
                destroyed = self.level.destroyed if self.level is not None else 0
                self.menu.draw(self.window, self.state, destroyed)
            pygame.display.flip()
        pygame.quit()
