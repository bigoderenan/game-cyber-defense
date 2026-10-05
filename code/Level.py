import random

import pygame

from code.Const import (BACKGROUND, CYAN, GRID, PLAY_TOP, RED, SERVER_HEALTH,
                        SERVER_TOP, SHOT_SPEED, SPAWN_INTERVAL, TARGET, WHITE,
                        WIN_HEIGHT, WIN_WIDTH)
from code.Malware import Malware
from code.Player import Player


class Level:
    def __init__(self):
        self.player = Player(pygame.Rect(20, PLAY_TOP, WIN_WIDTH - 40,
                                        SERVER_TOP - PLAY_TOP))
        self.malware = []
        self.shots = []
        self.integrity = SERVER_HEALTH
        self.destroyed = 0
        self.spawn_cooldown = SPAWN_INTERVAL
        self.font = pygame.font.Font(None, 27)
        self.state = 'playing'

    def update(self, seconds, horizontal, vertical, firing):
        if self.state != 'playing':
            return
        self.player.update(seconds, horizontal, vertical)
        if firing:
            shot = self.player.shoot()
            if shot is not None:
                self.shots.append(shot)

        self.spawn_cooldown -= seconds
        if self.spawn_cooldown <= 0:
            armored = random.randrange(4) == 0
            speed = 65 + min(self.destroyed, TARGET) * 2
            if armored:
                speed *= 0.8
            self.malware.append(Malware(random.randint(24, WIN_WIDTH - 58),
                                        speed, armored))
            self.spawn_cooldown += SPAWN_INTERVAL

        for threat in self.malware:
            threat.update(seconds)
        for shot in self.shots[:]:
            shot.y -= SHOT_SPEED * seconds
            shot_rect = pygame.Rect(round(shot.x) - 3, round(shot.y), 6, 16)
            for threat in self.malware[:]:
                if shot_rect.colliderect(threat.rect):
                    threat.health -= 1
                    self.shots.remove(shot)
                    if threat.health == 0:
                        self.malware.remove(threat)
                        self.destroyed += 1
                    break
            else:
                if shot.y + 16 < PLAY_TOP:
                    self.shots.remove(shot)

        for threat in self.malware[:]:
            if (threat.rect.bottom >= SERVER_TOP
                    or threat.rect.colliderect(self.player.rect)):
                self.malware.remove(threat)
                self.integrity = max(0, self.integrity - 1)

        if self.integrity == 0:
            self.state = 'defeat'
        elif self.destroyed >= TARGET:
            self.state = 'victory'

    def draw(self, window):
        window.fill(BACKGROUND)
        for x in range(0, WIN_WIDTH, 40):
            pygame.draw.line(window, GRID, (x, PLAY_TOP), (x, SERVER_TOP))
        for y in range(PLAY_TOP, SERVER_TOP, 40):
            pygame.draw.line(window, GRID, (0, y), (WIN_WIDTH, y))
        pygame.draw.rect(window, GRID, (0, SERVER_TOP, WIN_WIDTH, WIN_HEIGHT - SERVER_TOP))
        pygame.draw.line(window, CYAN, (0, SERVER_TOP), (WIN_WIDTH, SERVER_TOP), 2)
        for threat in self.malware:
            threat.draw(window)
        for shot in self.shots:
            pygame.draw.rect(window, CYAN, (round(shot.x) - 3, round(shot.y), 6, 16))
        self.player.draw(window)
        labels = [
            (f'Neutralizadas: {self.destroyed}/{TARGET}', (24, 22), WHITE),
            (f'Integridade: {self.integrity}/{SERVER_HEALTH}', (650, 22),
             RED if self.integrity <= 2 else CYAN),
            ('Setas/WASD: mover    Espaço: atirar    Esc: menu', (24, 57), WHITE),
            ('SERVIDOR - impeça que as ameaças alcancem esta linha', (155, 602), CYAN),
        ]
        for label, position, color in labels:
            window.blit(self.font.render(label, True, color), position)
