import pygame 
import sys 

import modelo.configuracoes as c 
import modelo.assets as a 
import modelo.ranking as rnk 
import view.telas as t 
import view.hud as h 

from controller.inimigos import criar_onda 


def iniciar_jogo ():
    """Tem a importante missão de limpar todas as listas da memória antes de inicializar a partida."""
    pygame.mixer.stop ()

    c.estado ["vitoria_exibida"] = False 
    c.estado ["mostrar_mensagem_darth"] = False 
    c.estado ["pause"] = False 
    c.estado ["score"] = 0 
    c.estado ["wave"] = 0 
    c.estado ["vader_ativo"] = False 

    # Posicionamento centralizado inicial do Boss
    c.vader.x = c.WIDTH //2 -c.vader.width //2 
    c.vader.y = 50 
    c.estado ["vader_acertos"] = 0 

    # Gerenciamento de dificuldade (vide modelo.configurações.py):
    # Define a vida conforme a escolha do menu principal
    c.controle_estado ()
    c.velocidade_inimigos = c.config_dificuldade [c.estado ["nivel_dificuldade_ativa"]]['inicial']

    # Reseta a posição do quadrado do jogador
    c.player.x = c.WIDTH //2 -c.player.width //2 
    c.player.y = c.HEIGHT -80 


def limpar_tela ():
    c.inimigos.clear ()
    c.tiros.clear ()
    c.tiros_inimigos.clear ()
    c.bactas.clear ()
    c.coracoes.clear ()
    c.explosoes_ativas.clear ()

    criar_onda (c.estado ["wave"])


def exibir_mensagem_darth ():
    while True :
        c.screen.fill (h.PRETO )
        msg = a.assets ["fonte_titulo"].render ("DARTH VADER SE APROXIMA!",True,h.VERMELHO )
        instr = a.assets ["fonte_hud"].render ("Pressione ENTER para Enfrentá-lo",True,h.VERDE_MUSGO )
        c.screen.blit (msg,(c.WIDTH //2 -msg.get_width ()//2,c.HEIGHT //3 ))
        c.screen.blit (instr,(c.WIDTH //2 -instr.get_width ()//2,c.HEIGHT //3 +60 ))
        pygame.display.flip ()

        for e in pygame.event.get ():
            if e.type == pygame.QUIT :
                pygame.quit ()
                sys.exit ()
            if e.type == pygame.KEYDOWN :
                if e.key == pygame.K_RETURN :
                    c.estado ["mostrar_mensagem_darth"] = False 

                    limpar_tela ()

                    c.estado ["vader_ativo"] = True 
                    return 


def verificar_e_atualizar_ranking ():
# Melhoria: elaborada função encapsulada pois foi aplicada em vários contextos.
    ranking = rnk.load_ranking ()

    if len (ranking )<10 or c.estado ["score"]>ranking [-1 ]['pontuacao']:
        nome_salvo = rnk.obter_nome_jogador ()
        rnk.update_ranking (nome_salvo,c.estado ["score"])
        rnk.exibir_ranking ()


"""O nome é autoexplicativo: garante inicialização limpa completa antes de
de engajar um evento ou tela, evitando empilhamento infinito"""
def capturar_evento_e_reiniciar_jogo ():
    for e in pygame.event.get ():
            if e.type == pygame.QUIT :
                pygame.quit ()
                sys.exit ()
            if e.type == pygame.KEYDOWN :
                if e.key == pygame.K_r :
                    pygame.mixer.stop ()# Corta a música de Game Over
                    a.tocar_musica_tema ()# Recarrega a trilha sonora de partida
                    iniciar_jogo ()         # Reseta os arrays da memória
                    limpar_tela ()
                    return 
                elif e.key == pygame.K_ESCAPE :
                    pygame.mixer.stop ()
                    pygame.quit ()
                    sys.exit ()


def game_over ():
    pygame.mixer.music.stop ()
    if a.assets ["sfx_gameover"]:
        a.assets ["sfx_gameover"].play ()

    verificar_e_atualizar_ranking ()

    clock = pygame.time.Clock ()
    while True :
        t.tela_game_over ()
        capturar_evento_e_reiniciar_jogo ()
        clock.tick (60)


def game_vitoria ():
    pygame.mixer.music.stop ()
    if a.assets ["sfx_vitoria"]:
        a.assets ["sfx_vitoria"].play ()

    verificar_e_atualizar_ranking ()

    clock = pygame.time.Clock ()
    while True :
        t.tela_vitoria ()
        capturar_evento_e_reiniciar_jogo ()
        clock.tick (60)