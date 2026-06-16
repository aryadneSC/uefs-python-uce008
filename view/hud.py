import pygame 
import time 

import modelo.configuracoes as c 
import modelo.assets as a 

AMARELO = (255,255,0 )
AZUL = (0,0,255 )
BRANCO = (255,255,255 )
CIANO = (255,0,255 )
CINZA = (150,150,150 )
PRETO = (0,0,0 )
VERDE_MUSGO = (2,85,100 )
VERMELHO_PASTEL = (255,100,100 )
VERDE = (0,255,0 )
VERMELHO = (255,0,0 )
TURQUESA = (64,204,208 )


def desenhar_texto_centralizado (superficie_texto,altura_y ):
    posicao_x = c.WIDTH //2 -superficie_texto.get_width ()//2 
    c.screen.blit (superficie_texto,(posicao_x,altura_y ))


def desenhar_botao_pausar_msc ():
    img_msc = a.assets.get ("img_icone_msc",None )
    if img_msc :
        indice_imagem = 1 if c.estado ["musica_pausada"]else 0 
        c.screen.blit (img_msc [indice_imagem ],c.msc_botao )
    else :
        cor_botao = VERMELHO_PASTEL if c.estado ["musica_pausada"]else AMARELO 
        pygame.draw.rect (c.screen,cor_botao,c.msc_botao )

    txt_msc = a.assets ["fonte_hud"].render ("(M)",True,BRANCO )
    c.screen.blit (txt_msc,(c.msc_botao.x +(c.msc_botao.width //2 )-(txt_msc.get_width ()//2 ),c.msc_botao.y +35 ))


def desenhar_elementos_hud (inicio_tempo,tempo_pausado_total ):
    score_txt = a.assets ["fonte_hud"].render (f"Score: {c.estado ['score']}",True,BRANCO )
    vida_txt = a.assets ["fonte_hud"].render (f"Vida: {c.estado ['vida']}",True,BRANCO )

    # Explicação '% 3600': Desconta os segundos em que o jogo permaneceu pausado
    tempo_atual = int (time.time ()-inicio_tempo -tempo_pausado_total )%3600 

    # Formata a saída numérica em formato 00:00 (ex: 02:05) usando divisão inteira e resto
    tempo_txt = a.assets ["fonte_hud"].render (f"Tempo: {tempo_atual //60 :02d}:{tempo_atual %60 :02d}",True,BRANCO )

    # Grid da interface
    c.screen.blit (score_txt,(10,10 ))# Canto superior esquerdo (Margem de 10 pixels)
    c.screen.blit (vida_txt,(10,50 ))# Logo abaixo do score, com alinhamento vertical
    c.screen.blit (tempo_txt,(c.WIDTH -250,10 ))# Alinhado à direita subtraindo a largura do texto