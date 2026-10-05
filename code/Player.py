import pygame

from code.Const import CYAN, PLAYER_SPEED, SHOT_INTERVAL


class Player:
    def __init__(self, bounds):
        self.bounds = bounds
        self.rect = pygame.Rect(0, 0, 34, 38)
        self.rect.midbottom = (bounds.centerx, bounds.bottom - 12)
        self.position = pygame.Vector2(self.rect.topleft)
        self.shot_cooldown = 0.0

    def update(self, seconds, horizontal, vertical):
        direction = pygame.Vector2(horizontal, vertical)
        if direction.length_squared() > 0:
            direction = direction.normalize()
        self.position += direction * PLAYER_SPEED * seconds
        self.position.x = max(self.bounds.left, min(self.position.x,
                              self.bounds.right - self.rect.width))
        self.position.y = max(self.bounds.top, min(self.position.y,
                              self.bounds.bottom - self.rect.height))
        self.rect.topleft = (round(self.position.x), round(self.position.y))
        self.shot_cooldown = max(0.0, self.shot_cooldown - seconds)

    def shoot(self):
        if self.shot_cooldown > 0:
            return None
        self.shot_cooldown = SHOT_INTERVAL
        return pygame.Vector2(self.rect.centerx, self.rect.top)

    def draw(self, window):
        pygame.draw.polygon(window, CYAN, [self.rect.midtop,
                            self.rect.bottomleft, self.rect.bottomright])
        pygame.draw.rect(window, (10, 18, 30),
                         (self.rect.centerx - 5, self.rect.centery, 10, 10))
