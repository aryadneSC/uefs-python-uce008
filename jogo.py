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
a.tocar_musica_tema()


def menu_principal():
    while True:
        if not pygame.mixer.music.get_busy() and not c.estado["musica_pausada"]:
            a.tocar_musica_tema()

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
    t.tela_narrativa()
    menu_principal()
