# Cyber Defense

Jogo 2D feito em Python com Pygame para a atividade de Linguagem de Programação Aplicada.

O objetivo é proteger o servidor e eliminar 15 ameaças. A partida começa com 7 pontos de integridade. Cada ameaça que encosta no jogador ou chega ao servidor tira um ponto. As vermelhas precisam de um tiro, e as amarelas precisam de dois.

A partida termina com vitória ao atingir a meta ou com derrota quando a integridade chega a zero. Se as duas condições acontecerem ao mesmo tempo, vale a derrota.

Os controles aparecem no menu:

- Setas ou WASD para mover.
- Espaço para atirar. Pode manter a tecla pressionada.
- Enter para começar ou jogar novamente.
- Esc para voltar ao menu. No menu, Esc fecha o jogo.

## Executar

Os comandos devem ser executados na pasta que contém o arquivo `main.py`.

No Windows, com Python instalado:

```text
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python main.py
```

No WSL, com Python e suporte gráfico disponíveis:

```bash
python3 -m venv .venv-wsl
source .venv-wsl/bin/activate
python -m pip install -r requirements.txt
python main.py
```

O ambiente do WSL é separado do ambiente do Windows.

## Gerar o executável

No terminal do Windows, com o ambiente virtual ativado:

```text
python -m pip install -r requirements-build.txt
build_windows.bat
```

O executável fica em `dist/CyberDefense.exe`, e o ZIP fica em `dist/CyberDefense-Windows.zip`. É preciso extrair o ZIP para abrir o jogo.

Os desenhos são feitos pelo Pygame, com a fonte que acompanha a biblioteca. Não há imagens ou sons externos.

## Testes

Para executar os testes, com o ambiente virtual ativado:

```text
python -m unittest discover -s tests -v
```

Os testes verificam movimento, disparos, colisões, vitória, derrota e troca de telas sem abrir uma janela. Os controles e a dificuldade precisam ser conferidos durante uma partida.
