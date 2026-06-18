import pygame
import sys

import modelo.configuracoes as c
import modelo.assets as a
import modelo.ranking as rnk
import view.telas as t
import view.hud as h

from controller.inimigos import criar_onda


def iniciar_jogo():
    a.parar_todas_as_musicas()
    a.tocar_musica_tema()

    c.estado["vitoria_exibida"] = False
    c.estado["mostrar_mensagem_darth"] = False
    c.estado["pause"] = False
    c.estado["score"] = 0
    c.estado["wave"] = 0
    c.estado["vader_ativo"] = False
    c.estado["motivo_morte"] = ""

    # Posicionamento inicial do Boss
    c.vader.x = c.WIDTH // 2 - c.vader.width // 2
    c.vader.y = 50
    c.estado["vader_acertos"] = 0

    c.controle_estado()

    # Define a velocidade inicial dos inimigos conforme a dificuldade ativa
    c.velocidade_inimigos = c.config_dificuldade[c.estado["nivel_dificuldade_ativa"]][
        "veloc_inicial"
    ]

    # Reseta a posição do quadrado do jogador
    c.player.x = c.WIDTH // 2 - c.player.width // 2
    c.player.y = c.HEIGHT - 80


def limpar_tela():
    c.inimigos.clear()
    c.tiros.clear()
    c.tiros_inimigos.clear()
    c.bactas.clear()
    c.coracoes.clear()
    c.escudo_defletor.clear()
    c.explosoes_ativas.clear()

    criar_onda(c.estado["wave"])


def exibir_mensagem_darth():
    clock = pygame.time.Clock()
    while True:
        clock.tick(30)
        c.screen.fill(h.PRETO)
        msg = a.assets["fonte_titulo"].render(
            "DARTH VADER SE APROXIMA!", True, h.VERMELHO
        )
        instr = a.assets["fonte_hud"].render(
            "Pressione ENTER para Enfrentá-lo", True, h.VERDE_MUSGO
        )
        c.screen.blit(msg, (c.WIDTH // 2 - msg.get_width() // 2, c.HEIGHT // 3))
        c.screen.blit(
            instr, (c.WIDTH // 2 - instr.get_width() // 2, c.HEIGHT // 3 + 60)
        )
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    c.estado["mostrar_mensagem_darth"] = False

                    limpar_tela()

                    c.estado["vader_ativo"] = True
                    return


def verificar_e_atualizar_ranking():
    ranking = rnk.load_ranking()

    if len(ranking) < 10 or c.estado["score"] > ranking[-1]["pontuacao"]:
        nome_salvo = rnk.obter_nome_jogador()
        rnk.update_ranking(nome_salvo, c.estado["score"])
        rnk.exibir_ranking()


def capturar_evento_e_reiniciar_jogo(permitir_voltar_ao_menu=False):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r:
                iniciar_jogo()  # já cuida da troca de música e do reset de estado
                limpar_tela()
                return "reiniciar"
            elif e.key == pygame.K_ESCAPE:
                a.parar_todas_as_musicas()
                if permitir_voltar_ao_menu:
                    a.tocar_musica_menu()
                    return "menu"
                pygame.quit()
                sys.exit()
    return None


def game_over():
    a.parar_todas_as_musicas()
    if a.assets["sfx_gameover"]:
        a.assets["sfx_gameover"].play()

    verificar_e_atualizar_ranking()

    clock = pygame.time.Clock()
    while True:
        clock.tick(30)
        t.tela_game_over()
        if capturar_evento_e_reiniciar_jogo() == "reiniciar":
            return


def game_vitoria():
    a.parar_todas_as_musicas()
    if a.assets["sfx_vitoria"]:
        a.assets["sfx_vitoria"].play()

    verificar_e_atualizar_ranking()

    clock = pygame.time.Clock()
    while True:
        clock.tick(30)
        t.tela_vitoria()
        resultado = capturar_evento_e_reiniciar_jogo(permitir_voltar_ao_menu=True)
        if resultado:
            return resultado