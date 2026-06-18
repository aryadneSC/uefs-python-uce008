import pygame 

WIDTH,HEIGHT = 800,600 

# A moldura da tela começa vazia (None) porque é preenchida pelo main.py assim que a janela abre
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
msc_botao = pygame.Rect (WIDTH -55,15,32,32 )
escudo_defletor_rect = pygame.Rect (0,0,60,20 )

# Posições iniciais
player = pygame.Rect (WIDTH //2 -20,HEIGHT -80,40,40 )
vader = pygame.Rect (WIDTH //2 -30,50,60,60 )

velocidade_inimigos = 1.0 # A velocidade é calculada pelo logica.py


# Dicionário para todas as variáveis mutáveis durante a partida
estado = {
"score":0,
"vida":3,
"vida_maxima":3,
"nivel_dificuldade_ativa":"facil",
"wave":0,
"vader_ativo":False,
"vader_acertos":0,
"vader_direcao":1,
"vitoria_exibida":False,
"pause":False,
"mostrar_mensagem_darth":False,
"musica_pausada":False 
}

#  Explicação: Cada lista representa uma linha horizontal de spawn.
# 1 = Tie Fighter e 2 = Espaço vazio
# Facilmente modificável :D
ondas = [
[0,1,0,1,0,1,0,0],
[0,0,1,0,1,0,0,1],
[1,0,0,1,0,0,1,0],
]

config_dificuldade = {
'facil':{'inicial':1.5,'limite':3.0,'incremento':0.2,'pontos_vader':200 },
'medio':{'inicial':2.0,'limite':3.5,'incremento':0.3,'pontos_vader':300 },
'dificil':{'inicial':3.0,'limite':4.0,'incremento':0.4,'pontos_vader':400 }
}


def controle_estado ():
    estado ["vida_maxima"] = 3 
    estado ["escudo_ativo"] = False 

    if estado ["nivel_dificuldade_ativa"] == 'facil':
        estado ["vida"] = 3 
    elif estado ["nivel_dificuldade_ativa"] == 'medio':
        estado ["vida"] = 3 
    elif estado ["nivel_dificuldade_ativa"] == 'dificil':
        estado ["vida"] = 3 


def alternar_pausar_musica ():
    estado ["musica_pausada"] = not estado ["musica_pausada"]

    if estado ["musica_pausada"]:
        pygame.mixer.music.pause()
    else :
        pygame.mixer.music.unpause()


def chk_colisao_player_inimigos():
    for inimigo in inimigos [:]:
        if player.colliderect (inimigo ['rect']):
            inimigos.remove (inimigo)
            return {'x':inimigo ['rect'].x,'y':inimigo ['rect'].y}
    return None 
