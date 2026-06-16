import pygame 
import sys 
import time 

import modelo.configuracoes as c 
import modelo.assets as a 
import view.hud as h 
import view.renderizacao as r 


def tela_narrativa ():
    """Exibe a introdução de Star Wars. Retorna apenas quando ENTER for pressionado."""
    while True :
        c.screen.fill (h.PRETO )
        h.desenhar_botao_pausar_msc ()

        titulo_narrativa = a.assets ["fonte_titulo"].render ("O IMPÉRIO GALÁCTICO CONTRA-ATACA",True,h.AMARELO )
        c.screen.blit (titulo_narrativa,(c.WIDTH //2 -titulo_narrativa.get_width ()//2,70 ))

        texto = [
        "A terrível Frota Imperial avança",
        "contra a base secreta",
        "do Planeta Aliado Kashyyyk!",
        "Nossas forças estão quase no fim...",
        "",
        "Guardião! Você é nossa única esperança",
        "de expulsar as tropas inimigas.",
        "Que a Força esteja com você...","",
        ]

        instrucao = a.assets ["fonte_titulo"].render ("Pressione ENTER para iniciar",True,h.VERDE_MUSGO )
        c.screen.blit (instrucao,(c.WIDTH //2 -instrucao.get_width ()//2,c.HEIGHT -70 ))

        for i,linha in enumerate (texto ):
            txt = a.assets ["fonte_titulo"].render (linha,True,h.BRANCO )
            c.screen.blit (txt,(c.WIDTH //2 -txt.get_width ()//2,c.HEIGHT //4 +i *40 ))

        pygame.display.flip ()

        for e in pygame.event.get ():
            if e.type == pygame.QUIT :
                pygame.quit ()
                sys.exit ()
            if e.type == pygame.KEYDOWN :
                if e.key == pygame.K_m :
                    c.alternar_pausar_musica ()
                elif e.key == pygame.K_RETURN :
                    return # Sai da tela narrativa de forma limpa


def tela_menu_principal ():
    c.screen.fill (h.PRETO )

    titulo = a.assets ["fonte_titulo"].render ("O DESPERTAR DO GUARDIÃO",True,h.AMARELO )
    start_txt = a.assets ["fonte_titulo"].render ("[ENTER] Iniciar",True,h.BRANCO )
    dificuldade_txt = a.assets ["fonte_titulo"].render ("[D] Dificuldade: "+c.estado ["nivel_dificuldade_ativa"].capitalize (),True,h.BRANCO )
    ranking_txt = a.assets ["fonte_titulo"].render ("[H] Hall da Fama",True,h.BRANCO )
    sair_txt = a.assets ["fonte_titulo"].render ("[ESC] Sair",True,h.BRANCO )

    c.screen.blit (titulo,(c.WIDTH //2 -titulo.get_width ()//2,c.HEIGHT //4 ))
    c.screen.blit (start_txt,(c.WIDTH //2 -start_txt.get_width ()//2,c.HEIGHT //2 -40 ))
    c.screen.blit (dificuldade_txt,(c.WIDTH //2 -dificuldade_txt.get_width ()//2,c.HEIGHT //2 +10 ))
    c.screen.blit (ranking_txt,(c.WIDTH //2 -ranking_txt.get_width ()//2,c.HEIGHT //2 +60 ))
    c.screen.blit (sair_txt,(c.WIDTH //2 -sair_txt.get_width ()//2,c.HEIGHT //2 +110 ))


def tela_partida (inicio_tempo,tempo_pausado_total ):
    """Renderiza todos os atores do gameplay camada por camada na Arena."""
    if a.assets ["img_fundo"]:
        c.screen.blit (a.assets ["img_fundo"],(0,0 ))
    else :
        c.screen.fill (h.PRETO )

    r.renderizar_player ()
    r.renderizar_aura_protecao ()
    r.renderizar_tie_fighters ()
    r.renderizar_bactas ()
    r.renderizar_escudos ()
    r.renderizar_inimigos_explodindo ()
    r.renderizar_botao_msc ()
    r.renderizar_projeteis ()
    r.renderizar_vader ()

    h.desenhar_elementos_hud (inicio_tempo,tempo_pausado_total )


def tela_menu_pausa ():
    c.screen.fill (h.PRETO )
    titulo = a.assets ["fonte_titulo"].render ("JOGO PAUSADO",True,h.AMARELO )
    continuar_txt = a.assets ["fonte_hud"].render ("Pressione P para Continuar",True,h.BRANCO )
    sair_txt = a.assets ["fonte_hud"].render ("Pressione ESC para Sair",True,h.VERMELHO_PASTEL )

    c.screen.blit (titulo,(c.WIDTH //2 -titulo.get_width ()//2,c.HEIGHT //3 ))
    c.screen.blit (continuar_txt,(c.WIDTH //2 -continuar_txt.get_width ()//2,c.HEIGHT //2 ))
    c.screen.blit (sair_txt,(c.WIDTH //2 -sair_txt.get_width ()//2,c.HEIGHT //2 +50 ))
    pygame.display.flip ()


def gerenciar_pausa ():
    inicio_pausa = time.time ()
    while c.estado ["pause"]:
        tela_menu_pausa ()

        for e in pygame.event.get ():
            if e.type == pygame.QUIT :
                pygame.quit ()
                sys.exit ()
            if e.type == pygame.KEYDOWN :
                if e.key == pygame.K_p or e.key == pygame.K_ESCAPE :
                    c.estado ["pause"] = False 

    return time.time ()-inicio_pausa 


def tela_game_over ():
    c.screen.fill (h.PRETO )
    msg = a.assets ["fonte_titulo"].render ("GAME OVER",True,h.VERMELHO )
    instr = a.assets ["fonte_hud"].render ("R para Reiniciar - ESC para Sair",True,h.BRANCO )

    h.desenhar_texto_centralizado (msg,c.HEIGHT //3 )
    h.desenhar_texto_centralizado (instr,c.HEIGHT //3 +60 )
    pygame.display.flip ()


def tela_vitoria ():
    c.screen.fill (h.PRETO )
    msg = a.assets ["fonte_titulo"].render ("VOCÊ VENCEU! A GALÁXIA ESTÁ SALVA!",True,h.VERDE )
    instr = a.assets ["fonte_hud"].render ("Pressione R para Reiniciar ou ESC para voltar ao menu",True,h.BRANCO )

    h.desenhar_texto_centralizado (msg,c.HEIGHT //3 )
    h.desenhar_texto_centralizado (instr,c.HEIGHT //3 +60 )
    pygame.display.flip ()
