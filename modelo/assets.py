import os 
import sys 
import pygame 
from os.path import join 

from modelo.configuracoes import WIDTH,HEIGHT 

"""Antigamente, os assets dependiam do diretório de execução da IDE...
o que gerava erros de FileNotFoundError. Isto centraliza a localização 
da pasta 'assets' independentemente de onde o programa seja executado."""

BASE_DIR = os.path.dirname (os.path.dirname (os.path.abspath (__file__ )))
ASSETS_DIR = os.path.join (BASE_DIR,"assets")


assets = {
"img_fundo":None,
"img_vader":None,
"img_bacta":None,
"img_inimigo":None,
"img_icone_msc":None,
"img_player_frames":[],
"img_explosao_frames":[],
"img_coracao":None,
"img_escudo":None,
"fonte_titulo":None,
"fonte_hud":None,
"sfx_laser":None,
"sfx_explosao":None,
"sfx_dano":None,
"sfx_item":None,
"sfx_gameover":None,
"sfx_vitoria":None,
}


def montar_caminho (pasta,arquivo):
    return os.path.join (ASSETS_DIR,pasta,arquivo)


def caminho_fonte (pasta,arquivo,tamanho):
    caminho = montar_caminho (pasta,arquivo)
    if os.path.exists (caminho):
        return pygame.font.Font (caminho,tamanho)
    else:
        return pygame.font.SysFont ('Arial',18)


def caminho_img (pasta,arquivo,tamanho = None):
    caminho = montar_caminho (pasta,arquivo)
    if os.path.exists (caminho):
        try:
            img = pygame.image.load (caminho).convert_alpha()
            if tamanho:
                img = pygame.transform.scale (img,tamanho)
            return img
        except:
            return None
    return None 


def carregar_som (pasta,arquivo,is_music = False):
    caminho = montar_caminho (pasta,arquivo)
    if os.path.exists (caminho):
        try:
            if is_music:
                pygame.mixer.music.load (caminho)
                return True 
            else:
                return pygame.mixer.Sound (caminho)
        except:
            return "Não foi possível carregar som em ", caminho 
    return None 


def inicializar_assets():
    """Aloca na memória todas as imagens, fontes e efeitos sonoros do jogo.
    Executada APÓS a inicialização do display no jogo.py.
    """

    print (os.getcwd())
    print (montar_caminho ('space','space-2.png'))

    assets ["img_fundo"] = caminho_img ('space','space-2.png',(WIDTH,HEIGHT))
    assets ["img_bacta"] = caminho_img ('space','bacta.png',(32,32))
    assets ["img_coracao"] = caminho_img ('space','coracao.png',(32,32))
    assets ["img_escudo"] = caminho_img ('space','escudo.png',(32,32))
    assets ["img_vader"] = caminho_img ('space','vader.png',(60,60))
    assets ["img_inimigo"] = caminho_img ('space','tie fighter.png',(40,40))

    # animação do Caça do Guardião
    p0 = caminho_img ('player','0.png',(40,40 ))
    p1 = caminho_img ('player','1.png',(40,40 ))
    assets ["img_player_frames"] = [f for f in [p0,p1 ]if f]

    # Animação de explosão dos Tie Fighters (5 frames numerados de 0 a 4)
    assets ["img_explosao_frames"] = []
    for i in range (5):
        frame = caminho_img ('explosion',f'{i}.png',(45,45))
        if frame:
            assets ["img_explosao_frames"].append (frame)

    # Ícones do botão de som
    msc0 = caminho_img ('icone','som on.png',(32,32))
    msc1 = caminho_img ('icone','som off.png',(32,32))
    assets ["img_icone_msc"] = [msc0,msc1 ]if msc0 and msc1 else None 

    # Fontes
    assets ["fonte_titulo"] = caminho_fonte ('fonts','PressStart2P-Regular.ttf',18)
    assets ["fonte_hud"] = caminho_fonte ('fonts','Silkscreen-Regular.ttf',20)

    # Efeitos sonoros
    assets ["sfx_laser"] = carregar_som ('audio/sfx','laser.ogg')
    assets ["sfx_explosao"] = carregar_som ('audio/sfx','explosao.ogg')
    assets ["sfx_dano"] = carregar_som ('audio/sfx','dano.ogg')
    assets ["sfx_item"] = carregar_som ('audio/sfx','item.ogg')
    assets ["sfx_gameover"] = carregar_som ('audio/sfx','gameover.ogg')
    assets ["sfx_vitoria"] = carregar_som ('audio/sfx','vitoria.ogg')

    # Volume homogêneo para todos os SFX
    volume = 0.2 
    chaves_sfx = ["sfx_laser","sfx_explosao","sfx_dano","sfx_item","sfx_gameover","sfx_vitoria"]
    for chave in chaves_sfx:
        sfx = assets [chave]
        if sfx:
            sfx.set_volume (volume)


def tocar_musica_tema():
    if carregar_som ('audio','meteorstheme_v1.ogg',is_music = True):
        try:
            pygame.mixer.music.set_volume (0.4)
            pygame.mixer.music.play (-1)
        except: pass 
