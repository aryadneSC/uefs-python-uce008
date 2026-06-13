"""assets: Gerenciamento do inventário de recursos multimídia."""

import os
import sys
import pygame
from os.path import join

from modelo.configuracoes import WIDTH, HEIGHT

"""Antigamente, os assets dependiam do diretório de execução da IDE...
...Isso gerava erros de FileNotFoundError."""
"""Centraliza a construção dos caminhos dos assets."""
"""Ele localização a pasta independentemente de onde o programa seja executado."""
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def montar_caminho(pasta, arquivo):
    return os.path.join(ASSETS_DIR, pasta, arquivo)

def caminho_fonte(pasta, arquivo, tamanho):
    caminho = montar_caminho(pasta, arquivo)
    if os.path.exists(caminho):
        return pygame.font.Font(caminho, tamanho)
    else:
        return pygame.font.SysFont('Arial', 18)

def caminho_img(pasta, arquivo, tamanho=None):
    caminho = montar_caminho(pasta, arquivo)
    if os.path.exists(caminho):
        try:
            img = pygame.image.load(caminho).convert_alpha()
            if tamanho:
                img = pygame.transform.scale(img, tamanho)
                return img
        except:
            return "Não foi possível localizar imagem em ", caminho 
    return None    

def carregar_som(pasta, arquivo, is_music=False):
    caminho = montar_caminho(pasta, arquivo)
    if os.path.exists(caminho):
        try:
            if is_music:
                pygame.mixer.music.load(caminho)
                return True
            else:
                return pygame.mixer.Sound(caminho)
        except:
            return "Não foi possível carregar som em ", caminho
    return None

assets = {
    "img_fundo": None,
    "img_vader": None,
    "img_bacta": None,
    "img_inimigo": None,
    "img_icone_msc": None,
    "img_player_frames": [],
    "img_explosao_frames": [],
    "fonte_titulo": None,
    "fonte_hud": None,
    "sfx_laser": None,
    "sfx_explosao": None,
    "sfx_dano": None,
    "sfx_bacta": None,
    "sfx_gameover": None,
    "sfx_vitoria": None,
}

def inicializar_assets():
    """Aloca na memória todas as imagens, fontes e efeitos sonoros do jogo.
    Executada APÓS a inicialização do display no main.py.
    """
    print(os.getcwd())
    print(montar_caminho('space', 'space-2.png'))

    assets["img_fundo"] = caminho_img('space', 'space-2.png', (WIDTH, HEIGHT))
    assets["img_bacta"] = caminho_img('space', 'bacta.png', (32, 32))
    assets["img_vader"] = caminho_img('space', 'vader.png', (60, 60))
    assets["img_inimigo"] = caminho_img('space', 'tie fighter.png',(40, 40))

    # animação do Caça do Guardião
    p0 = caminho_img('player', '0.png', (40, 40))
    p1 = caminho_img('player', '1.png', (40, 40))
    assets["img_player_frames"] = [f for f in [p0, p1] if f]

    # Animação de explosão dos Tie Fighters (5 frames numerados de 0 a 4)
    assets["img_explosao_frames"] = []  # garante lista limpa a cada inicialização
    for i in range(5):
        frame = caminho_img('explosion', f'{i}.png', (45, 45))
        if frame:
            assets["img_explosao_frames"].append(frame)

    # Ícones do botão de som
    msc0 = caminho_img('icone', 'som on.png', (32, 32))
    msc1 = caminho_img('icone', 'som off.png', (32, 32))
    assets["img_icone_msc"] = [msc0, msc1] if msc0 and msc1 else None

    # Fontes
    assets["fonte_titulo"] = caminho_fonte('fonts', 'PressStart2P-Regular.ttf', 18)
    assets["fonte_hud"]    = caminho_fonte('fonts', 'Silkscreen-Regular.ttf', 20)

    # Efeitos sonoros
    assets["sfx_laser"]    = carregar_som('audio/sfx', 'laser.wav')
    assets["sfx_explosao"] = carregar_som('audio/sfx', 'explosao.wav')
    assets["sfx_dano"]     = carregar_som('audio/sfx', 'dano.wav')
    assets["sfx_bacta"]    = carregar_som('audio/sfx', 'bacta.wav')
    assets["sfx_gameover"] = carregar_som('audio/sfx', 'gameover.wav')
    assets["sfx_vitoria"]  = carregar_som('audio/sfx', 'vitoria.wav')

    # Volume homogêneo para todos os SFX
    volume = 0.2
    chaves_sfx = ["sfx_laser", "sfx_explosao", "sfx_dano", "sfx_bacta", "sfx_gameover", "sfx_vitoria"]
    for chave in chaves_sfx:
        sfx = assets[chave]
        if sfx:
            sfx.set_volume(volume)
    
def tocar_musica_tema():
    """Gerencia a ativação em looping da trilha sonora principal."""
    if carregar_som('audio', 'meteorstheme_v1.wav', is_music=True):
        try:
            pygame.mixer.music.set_volume(0.4) # Calibra o volume em 40%
            pygame.mixer.music.play(-1)        # -1 executa a repetição infinita
        except: pass