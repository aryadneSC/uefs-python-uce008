import pygame
import sys
import os

pygame.init()

import modelo.configuracoes as c
import modelo.assets as a
import modelo.ranking as rnk
import view.telas as t
import view.hud as h
import controller.ciclo_jogo as cj
import controller.loop_principal as lp

c.screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
pygame.display.set_caption("O Despertar do Guardião")
screen = c.screen

try:
    caminho_icone = os.path.join("assets", "player", "0.png")
    img_icone = pygame.image.load(caminho_icone)
    pygame.display.set_icon(img_icone)
except Exception as e:
    print(f"Não foi possível carregar o ícone: {e}")

a.inicializar_assets()


def menu_principal():
    a.tocar_musica_menu()
    clock = pygame.time.Clock()

    while True:
        clock.tick(30)
        t.tela_menu_principal()
        h.desenhar_botao_pausar_msc()
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_m:
                    c.alternar_pausar_musica()

                elif e.key == pygame.K_RETURN:
                    cj.iniciar_jogo()
                    lp.main_loop()
                    # Ao voltar de uma partida (vitória->menu, ou fim de jogo),
                    # a tela é o menu de novo: retoma a música deste 'galho'.
                    a.tocar_musica_menu()

                elif e.key == pygame.K_d:
                    if c.estado["nivel_dificuldade_ativa"] == "facil":
                        c.estado["nivel_dificuldade_ativa"] = "medio"
                    elif c.estado["nivel_dificuldade_ativa"] == "medio":
                        c.estado["nivel_dificuldade_ativa"] = "dificil"
                    else:
                        c.estado["nivel_dificuldade_ativa"] = "facil"

                elif e.key == pygame.K_h:
                    rnk.exibir_ranking()

                elif e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


if __name__ == "__main__":
    a.tocar_musica_menu()
    t.tela_narrativa()
    menu_principal()