"""Jogo.py: 
Este módulo contém a main e atua como núcleo que inicializa a janela de hardware do SDL,
sincroniza os atalhos locais de vídeo e dita a sequência linear de boot do jogo.
"""

import pygame
import sys

# Explicação: depois de alguns testes, percebi que inicializar o pygame...
# ...antes de importar os demais packages impede erros de inicialização de recursos (como fontes e áudio), 
# isso será replicado também em outros módulos com lógica aplicada
pygame.init()

import modelo.configuracoes as c
import modelo.assets as a
import modelo.ranking as rnk
import view.menus as m
import controller.logica as l

img_icone = carregar_img("player", "0.png")

if img_icone:
    pygame.display.set_icon(img_icone)

c.screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
pygame.display.set_caption("O Despertar do Guardião")

# Explicação: Inicialmente, declarar 'screen = c.screen' antes do display.set_mode() 
# gerava um NameError ou atribuía None, pois o display ainda não existia. Ao mover esta linha para cá, 
# resultou em um atalho seguro e local que aponta perfeitamente para a superficie ativa da janela.
screen = c.screen 

a.inicializar_assets()
a.tocar_musica_tema()

def menu_principal():
    """Gerencia a navegação inicial baseada no teclado e delega o disparo da partida para o Controller."""
    while True:
        # Bug corrigido: Caso o jogador voltasse da tela de vitória/derrota via ESC, a música 
        # de fundo permanecia desligada. 
        # O get_busy() checa o canal de áudio e reativa a trilha caso esteja em silêncio.
        if not pygame.mixer.music.get_busy() and not c.estado["musica_pausada"]:
            a.tocar_musica_tema()

        c.screen.fill(m.PRETO)

        titulo = a.assets["fonte_titulo"].render("O DESPERTAR DO GUARDIÃO", True, m.AMARELO)
        start_txt = a.assets["fonte_titulo"].render("[ENTER] Iniciar", True, m.BRANCO)
        dificuldade_txt = a.assets["fonte_titulo"].render("[D] Dificuldade: " + c.estado["nivel_dificuldade_ativa"].capitalize(), True, m.BRANCO)
        ranking_txt = a.assets["fonte_titulo"].render("[H] Hall da Fama", True, m.BRANCO)
        sair_txt = a.assets["fonte_titulo"].render("[ESC] Sair", True, m.BRANCO)
        
        # Blitagem do Menu principal
        # Fórmula aplicada: (Largura_Total_Janela // 2) - (Largura_Superfície_Texto // 2) para alinhamento central.
        c.screen.blit(titulo, (c.WIDTH // 2 - titulo.get_width() // 2, c.HEIGHT // 4)) # posiciona no primeiro quadrante
        c.screen.blit(start_txt, (c.WIDTH // 2 - start_txt.get_width() // 2, c.HEIGHT // 2 - 40)) # início do grid vertical
        
        c.screen.blit(dificuldade_txt, (c.WIDTH // 2 - dificuldade_txt.get_width() // 2, c.HEIGHT // 2 + 10)) # Salto de 50px

        c.screen.blit(ranking_txt, (c.WIDTH // 2 - ranking_txt.get_width() // 2, c.HEIGHT // 2 + 60))
        c.screen.blit(sair_txt, (c.WIDTH // 2 - sair_txt.get_width() // 2, c.HEIGHT // 2 + 110))

        m.desenhar_botao_pausar_msc()
        
        pygame.display.flip()
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_m:
                    c.alternar_pausar_musica()
                        
                elif e.key == pygame.K_RETURN:
                    l.iniciar_jogo()
                    l.main_loop()   

                elif e.key == pygame.K_d:
                    if c.estado["nivel_dificuldade_ativa"] == 'facil': 
                        c.estado["nivel_dificuldade_ativa"] = 'medio'
                    elif c.estado["nivel_dificuldade_ativa"] == 'medio': 
                        c.estado["nivel_dificuldade_ativa"] = 'dificil'
                    else: 
                        c.estado["nivel_dificuldade_ativa"] = 'facil'
                        
                elif e.key == pygame.K_h:
                    rnk.exibir_ranking()
                    
                elif e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    while True:
        m.tela_narrativa()
        menu_principal()
