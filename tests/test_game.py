import os
import random
import unittest

os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

from code.Const import PLAYER_SPEED, SERVER_HEALTH, SERVER_TOP, SHOT_INTERVAL, TARGET
from code.Game import Game
from code.Level import Level
from code.Malware import Malware


class GameTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.display.init()
        pygame.font.init()
        pygame.display.set_mode((900, 640))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.level = Level()

    def add_threat(self, armored=False):
        threat = Malware(100, 0, armored)
        threat.position.y = 200
        threat.rect.y = 200
        self.level.malware.append(threat)
        return threat

    def test_player_stays_inside_bounds(self):
        player = self.level.player
        player.update(10, -1, -1)
        self.assertEqual(player.rect.topleft, player.bounds.topleft)
        player.update(10, 1, 1)
        self.assertEqual(player.rect.bottomright, player.bounds.bottomright)

    def test_diagonal_speed_equals_horizontal_speed(self):
        player = self.level.player
        start = player.position.copy()
        player.update(0.1, 1, -1)
        self.assertAlmostEqual(player.position.distance_to(start), PLAYER_SPEED * 0.1)

    def test_shot_has_cooldown_and_starts_at_player(self):
        player = self.level.player
        self.assertEqual(player.shoot(), pygame.Vector2(player.rect.midtop))
        self.assertIsNone(player.shoot())
        player.update(SHOT_INTERVAL, 0, 0)
        self.assertIsNotNone(player.shoot())

    def test_one_shot_removes_normal_threat(self):
        threat = self.add_threat()
        self.level.shots.append(pygame.Vector2(threat.rect.center))
        self.level.update(0, 0, 0, False)
        self.assertEqual(self.level.destroyed, 1)
        self.assertEqual(self.level.malware, [])
        self.assertEqual(self.level.shots, [])

    def test_armored_threat_requires_two_shots(self):
        threat = self.add_threat(armored=True)
        self.level.shots.append(pygame.Vector2(threat.rect.center))
        self.level.update(0, 0, 0, False)
        self.assertEqual(threat.health, 1)
        self.assertEqual(self.level.destroyed, 0)
        self.level.shots.append(pygame.Vector2(threat.rect.center))
        self.level.update(0, 0, 0, False)
        self.assertEqual(self.level.destroyed, 1)

    def test_one_shot_cannot_hit_two_overlapping_threats(self):
        threat = self.add_threat()
        self.add_threat()
        self.level.shots.append(pygame.Vector2(threat.rect.center))
        self.level.update(0, 0, 0, False)
        self.assertEqual(self.level.destroyed, 1)
        self.assertEqual(len(self.level.malware), 1)

    def test_server_breach_causes_damage_once(self):
        threat = self.add_threat()
        threat.position.y = SERVER_TOP - threat.rect.height
        self.level.update(0, 0, 0, False)
        self.level.update(0, 0, 0, False)
        self.assertEqual(self.level.integrity, SERVER_HEALTH - 1)
        self.assertEqual(self.level.destroyed, 0)
        self.assertEqual(self.level.malware, [])

    def test_contact_causes_damage(self):
        threat = self.add_threat()
        threat.rect.topleft = self.level.player.rect.topleft
        threat.position = pygame.Vector2(threat.rect.topleft)
        self.level.update(0, 0, 0, False)
        self.assertEqual(self.level.integrity, SERVER_HEALTH - 1)
        self.assertEqual(self.level.malware, [])

    def test_target_causes_victory_and_freezes_level(self):
        self.level.destroyed = TARGET - 1
        threat = self.add_threat()
        self.level.shots.append(pygame.Vector2(threat.rect.center))
        self.level.update(0, 0, 0, False)
        self.assertEqual(self.level.state, 'victory')
        position = self.level.player.position.copy()
        self.level.update(1, 1, -1, True)
        self.assertEqual(self.level.player.position, position)
        self.assertEqual(self.level.malware, [])

    def test_zero_integrity_causes_defeat_before_victory(self):
        self.level.integrity = 1
        self.level.destroyed = TARGET - 1
        shot_target = self.add_threat()
        invader = self.add_threat()
        invader.position.y = SERVER_TOP
        self.level.shots.append(pygame.Vector2(shot_target.rect.center))
        self.level.update(0, 0, 0, False)
        self.assertEqual(self.level.destroyed, TARGET)
        self.assertEqual(self.level.integrity, 0)
        self.assertEqual(self.level.state, 'defeat')

    def test_idle_player_eventually_loses_to_real_spawns(self):
        for frame in range(60 * 30):
            self.level.update(1 / 60, 0, 0, False)
            if self.level.state == 'defeat':
                break
        self.assertEqual(self.level.state, 'defeat')
        self.assertEqual(self.level.integrity, 0)

    def test_offscreen_shots_are_removed(self):
        self.level.shots.append(pygame.Vector2(200, -30))
        self.level.update(0, 0, 0, False)
        self.assertEqual(self.level.shots, [])

    def test_simulated_player_wins_against_real_spawns(self):
        random.seed(8)
        for frame in range(60 * 60):
            horizontal = 0
            if self.level.malware:
                target = max(self.level.malware, key=lambda threat: threat.rect.y)
                distance = target.rect.centerx - self.level.player.rect.centerx
                horizontal = 1 if distance > 5 else -1 if distance < -5 else 0
            self.level.update(1 / 60, horizontal, 0, True)
            if self.level.state != 'playing':
                break
        self.assertEqual(self.level.state, 'victory')
        self.assertEqual(self.level.destroyed, TARGET)
        self.assertGreater(self.level.integrity, 0)

    def test_menu_start_return_and_restart(self):
        game = Game()
        enter = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
        escape = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
        game.handle_event(enter)
        self.assertEqual(game.state, 'playing')
        previous_level = game.level
        game.handle_event(enter)
        self.assertIs(game.level, previous_level)
        game.handle_event(escape)
        self.assertEqual(game.state, 'menu')
        game.handle_event(enter)
        self.assertIsNot(game.level, previous_level)
        self.assertEqual(game.level.integrity, SERVER_HEALTH)
        game.state = 'defeat'
        game.handle_event(enter)
        self.assertEqual(game.state, 'playing')
        game.handle_event(escape)
        game.handle_event(escape)
        self.assertFalse(game.running)

    def test_close_window_ends_game(self):
        game = Game()
        game.handle_event(pygame.event.Event(pygame.QUIT))
        self.assertFalse(game.running)

    def test_every_screen_renders(self):
        game = Game()
        for state in ('menu', 'victory', 'defeat'):
            game.menu.draw(game.window, state, TARGET)
        self.level.draw(game.window)
        pygame.display.flip()


if __name__ == '__main__':
    unittest.main()
