# Cyber Defense

Demo 2D: proteja o servidor e neutralize 15 ameaças antes de perder os 7 pontos de integridade. Vermelhas precisam de um tiro, amarelas de dois. Contato com o jogador ou chegada ao servidor remove a ameaça e custa um ponto. Se vitória e derrota ocorrerem na mesma atualização, a derrota prevalece.

## Executar

Na pasta do projeto, com Python instalado:

```text
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python main.py
```

Setas ou WASD movem; Espaço dispara; Enter inicia ou reinicia; Esc retorna ao menu ou sai quando já está nele. Fechar a janela encerra o jogo.

## Build Windows

No Windows, com o ambiente acima ativado:

```text
python -m pip install -r requirements-build.txt
build_windows.bat
```

O script gera `dist/CyberDefense.exe` e `dist/CyberDefense-Windows.zip`. Extraia o ZIP antes de executar. Os gráficos e a fonte são fornecidos pelo próprio Pygame; não há arquivos externos de imagem ou som para copiar. O executável deve ser conferido na máquina de destino.

## Código e testes

`main.py` inicia `Game`, que controla janela, eventos e telas. `Menu` mostra comandos e resultados. `Level` concentra surgimento de ameaças, tiros, colisões e condições de fim. `Player` cuida de movimento e intervalo dos disparos; `Malware`, de movimento e resistência das ameaças. `Const.py` reúne medidas, cores e regras ajustáveis.

```text
python -m unittest discover -s tests -v
```

Os testes usam o driver de vídeo dummy do SDL, sem abrir janela, e exercitam a lógica real. Não substituem uma partida manual para conferir os controles e a dificuldade.

Ambiente verificado: Windows 11 de 64 bits, Python 3.12.14, Pygame 2.6.1 e PyInstaller 6.22.3. Outras versões de Python não foram testadas.

Implementação nova baseada na organização conceitual das aulas. O código-fonte do Mountain Shooter não estava disponível neste ambiente para comparação linha por linha. Revise, teste e adapte o projeto antes da entrega.
