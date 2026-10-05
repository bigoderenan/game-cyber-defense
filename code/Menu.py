import pygame

from code.Const import BACKGROUND, CYAN, TARGET, WHITE, WIN_WIDTH


class Menu:
    def __init__(self):
        self.title_font = pygame.font.Font(None, 64)
        self.font = pygame.font.Font(None, 29)

    def draw(self, window, state, destroyed=0):
        window.fill(BACKGROUND)
        if state == 'menu':
            title = 'CYBER DEFENSE'
            lines = [
                f'Proteja o servidor e neutralize {TARGET} ameaças.',
                'Ameaças vermelhas: 1 tiro | amarelas: 2 tiros',
                'Contato ou invasão do servidor: perde 1 de integridade.',
                '',
                'Setas ou WASD - mover',
                'Espaço - atirar (pode manter pressionado)',
                'Enter - iniciar | Esc - sair',
            ]
        else:
            title = 'REDE PROTEGIDA' if state == 'victory' else 'REDE COMPROMETIDA'
            lines = [
                f'Ameaças neutralizadas: {destroyed}',
                '',
                'Enter - jogar novamente',
                'Esc - voltar ao menu',
            ]
        heading = self.title_font.render(title, True, CYAN)
        window.blit(heading, heading.get_rect(center=(WIN_WIDTH // 2, 150)))
        for index, line in enumerate(lines):
            text = self.font.render(line, True, WHITE)
            window.blit(text, text.get_rect(center=(WIN_WIDTH // 2, 250 + index * 38)))
