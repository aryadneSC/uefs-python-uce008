import pygame

WIDTH, HEIGHT = 800, 600

# A moldura da tela começa vazia pois é preenchida pelo main.py assim que a janela abre
screen = None

# Objetos gerados em tempo real durante a partida.
tiros = []
inimigos = []
tiros_inimigos = []
bactas = []
coracoes = []
explosoes_ativas = []
escudo_defletor = []

# Rects fixos
msc_botao = pygame.Rect(WIDTH - 55, 15, 32, 32)

# Posições iniciais
player = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 80, 40, 40)
vader = pygame.Rect(WIDTH // 2 - 30, 50, 60, 60)

velocidade_inimigos = 1.0  # A velocidade é calculada pelo logica.py

# Delay de coleta de drops após seu spawn
DROP_PICKUP_DELAY_MS = 300


# Dicionário para todas as variáveis mutáveis durante a partida
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
    "musica_pausada": False,
    "motivo_morte": "",
    "escudo_ativo": False,
}

# Explicação: Cada lista representa uma linha horizontal de spawn.
# 1 = Tie Fighter e 0 = Espaço vazio
# Agora com ondas separadas por dificuldade :D
ondas = {
    "facil": [
        [0, 1, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 1, 0, 0, 1, 0],
    ],
    "medio": [
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 1, 0, 1, 1, 0, 1],
        [1, 1, 0, 1, 1, 0, 1, 1],
    ],
    "dificil": [
        [1, 1, 1, 0, 1, 1, 1, 0],
        [1, 1, 0, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 0, 1, 1, 1],
    ],
}

config_dificuldade = {
    "facil": {
        "veloc_inicial": 1.5,
        "veloc_limite": 3.0,
        "incremento": 0.2,
        "pontos_vader": 200,
    },
    "medio": {
        "veloc_inicial": 2.0,
        "veloc_limite": 3.5,
        "incremento": 0.3,
        "pontos_vader": 300,
    },
    "dificil": {
        "veloc_inicial": 3.0,
        "veloc_limite": 4.0,
        "incremento": 0.4,
        "pontos_vader": 400,
    },
}


def controle_estado():
    estado["vida_maxima"] = 3
    estado["vida"] = 3
    estado["escudo_ativo"] = False


def alternar_pausar_musica():
    estado["musica_pausada"] = not estado["musica_pausada"]

    if estado["musica_pausada"]:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
