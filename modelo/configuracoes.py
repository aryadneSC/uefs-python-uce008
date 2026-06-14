"""Atua como o Banco de Dados e Gerenciador de Estados (Model).
Centraliza dimensões físicas, vetores de ondas, dicionários de dificuldades
e o estado atual do gameplay.
Centraliza estado e regras de negócios do jogo"""

import pygame

WIDTH, HEIGHT = 800, 600

# A moldura da tela começa vazia (None) porque é preenchida pelo main.py assim que a janela abre
screen = None  

# Dicionário para todas as variáveis mutáveis durante a partida, isso
# torna o gerenciamento muito mais simples e centralizado.
estado = {
    "score": 0,
    "vida": 3,
    "vida_maxima": 3,
    "nivel_dificuldade_ativa": "facil",
    "wave": 0,
    "vader_ativo": False,
    "vader_acertos": 0,
    "vader_direcao": 1,
    "vitoria_exibida": False,
    "pause": False,
    "mostrar_mensagem_darth": False,
    "musica_pausada" : False
}

msc_botao = pygame.Rect(WIDTH - 55, 15, 32, 32)

"""Explicação: utilizei funções nativas do pygame (pause e unpause)"""
def alternar_pausar_musica():
    """Inverte o booleano e aplica o estado no mixer do pygame."""
    estado["musica_pausada"] = not estado["musica_pausada"]
    
    if estado["musica_pausada"]:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()

# Explicação: Cada lista representa uma linha horizontal de spawn.
# 1 = Tie Fighter e 2 = Espaço vazio ... Modificável!
ondas = [
    [0, 1, 0, 1, 0, 1, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [1, 0, 0, 1, 0, 0, 1, 0],
]

# Define as velocidades iniciais, limites e acelerações para cada nível de dificuldade.
config_dificuldade = {
    'facil': {'inicial': 1.5, 'limite': 3.0, 'incremento': 0.2},
    'medio': {'inicial': 2.5, 'limite': 4.5, 'incremento': 0.3},
    'dificil': {'inicial': 3.0, 'limite': 5.0, 'incremento': 0.4}
}

velocidade_inimigos = 1.0 # Velocidade atual das naves na rodada, calculada pelo logica.py

# Posições iniciais
player = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 80, 40, 40)
vader = pygame.Rect(WIDTH // 2 - 30, 50, 60, 60)

# Listas que armazenam os objetos gerados em tempo real durante a partida.
tiros = []
inimigos = []
tiros_inimigos = []
bactas = []
explosoes_ativas = []

def controle_dificuldade():
    if estado["nivel_dificuldade_ativa"] == 'facil': 
        estado["vida"] = 3
    elif estado["nivel_dificuldade_ativa"] == 'medio': 
        estado["vida"] = 3
    elif estado["nivel_dificuldade_ativa"] == 'dificil': 
        estado["vida"] = 3
        
def chk_colisao_player_inimigos():
    for inimigo in inimigos[:]:
        if player.colliderect(inimigo['rect']):
            inimigos.remove(inimigo)
            return {'x': inimigo['rect'].x, 'y': inimigo['rect'].y}
    return None
