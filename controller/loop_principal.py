import pygame
import sys
import random
import time

import modelo.configuracoes as c
import modelo.assets as a
import view.telas as telas_view

from controller.inimigos import colisao_recuo_inimigos, criar_onda
from controller.projeteis import atualizar_projeteis
from controller.ciclo_jogo import (
    limpar_tela,
    exibir_mensagem_darth,
    game_over,
    game_vitoria,
)

def processar_fim_de_partida(resultado):
    if resultado == "reiniciar":
        main_loop()


def main_loop():
    inicio_tempo = time.time()
    tempo_pausado_total = 0
    clock = pygame.time.Clock()

    limpar_tela()

    while True:
        if c.estado["pause"]:
            tempo_pausado_total += telas_view.gerenciar_pausa()
            continue

        clock.tick(60)

        # 1) Captura de eventos únicos
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_m:
                    c.alternar_pausar_musica()
                if e.key == pygame.K_p or e.key == pygame.K_ESCAPE:
                    c.estado["pause"] = True
                if e.key == pygame.K_SPACE:
                    c.tiros.append(
                        pygame.Rect(c.player.centerx - 5, c.player.top - 10, 10, 20)
                    )
                    if a.assets["sfx_laser"]:
                        a.assets["sfx_laser"].play()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    if c.msc_botao.collidepoint(e.pos):
                        c.alternar_pausar_musica()

        # Input polling para movimento contínuo do jogador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            c.player.x -= 5
        if keys[pygame.K_RIGHT]:
            c.player.x += 5
        if keys[pygame.K_UP]:
            c.player.y -= 5
        if keys[pygame.K_DOWN]:
            c.player.y += 5

        # Mantém o player dentro dos limites da janela
        c.player.clamp_ip(pygame.Rect(0, 0, c.WIDTH, c.HEIGHT))

        # Zona de perigo do Darth Vader
        danger_zone = None
        if c.estado["vader_ativo"]:
            danger_zone = pygame.Rect(0, 0, c.WIDTH, c.vader.top)

        if danger_zone and c.player.colliderect(danger_zone):
            now = pygame.time.get_ticks()
            if now - c.estado.get("ultimo_dano_zona_perigo", 0) >= 500:
                c.estado["ultimo_dano_zona_perigo"] = now
                if c.estado["escudo_ativo"]:
                    c.estado["escudo_ativo"] = False
                else:
                    c.estado["vida"] -= 1
                    if not c.estado.get("motivo_morte"):
                        c.estado["motivo_morte"] = "zona_perigo"
                if a.assets["sfx_dano"]:
                    a.assets["sfx_dano"].play()
                if c.estado["vida"] <= 0:
                    processar_fim_de_partida(game_over())
                    return

        # 2) Colisão Guardião contra Inimigos
        if not c.estado["vader_ativo"]:
            for inimigo in c.inimigos[:]:
                if c.player.inflate(-16, -12).colliderect(inimigo["rect"]):
                    c.inimigos.remove(inimigo)

                    # Checagem com escudo ativo
                    if c.estado["escudo_ativo"]:
                        c.estado["escudo_ativo"] = False
                    else:
                        c.estado["vida"] -= 1
                        if not c.estado.get("motivo_morte"):
                            c.estado["motivo_morte"] = "colisao_inimigo"

                    if a.assets["sfx_dano"]:
                        a.assets["sfx_dano"].play()
                    c.explosoes_ativas.append(
                        {
                            "x": inimigo["rect"].x,
                            "y": inimigo["rect"].y,
                            "frame": 0,
                            "last_update": pygame.time.get_ticks(),
                        }
                    )
                    if c.estado["vida"] <= 0:
                        processar_fim_de_partida(game_over())
                        return

        # 3) Projéteis
        atualizar_projeteis(c.tiros, -16, eh_laser_jogador=True)
        atualizar_projeteis(c.tiros_inimigos, 5, eh_laser_jogador=False)

        # Se o Boss final não estiver ativo, move os stormtroopers
        if not c.estado["vader_ativo"]:
            colisao_recuo_inimigos()

        # Probabilidade de disparos dos inimigos comuns
        taxa_disparo = (
            0.008
            if c.estado["nivel_dificuldade_ativa"] == "facil"
            else (0.015 if c.estado["nivel_dificuldade_ativa"] == "medio" else 0.023)
        )
        if (
            random.random() < taxa_disparo
            and c.inimigos
            and not c.estado["vader_ativo"]
        ):
            inimigo = random.choice(c.inimigos)
            c.tiros_inimigos.append(
                {
                    "rect": pygame.Rect(
                        inimigo["rect"].centerx - 2, inimigo["rect"].bottom, 5, 10
                    ),
                    "vader": False,
                }
            )

        # 4) Colisões drops

        # A) Cápsulas de Bacta
        for b in c.bactas[:]:
            # Dicionário: {"rect": Rect, "spawn": ticks}
            b["rect"].y += 2
            now = pygame.time.get_ticks()
            if (
                b["rect"].colliderect(c.player.inflate(8, 8))
                and now - b.get("spawn", 0) >= c.DROP_PICKUP_DELAY_MS
            ):
                teto_vida = 3
                if (
                    c.estado["vida"] < c.estado["vida_maxima"]
                    and c.estado["vida"] < teto_vida
                ):
                    c.estado["vida"] += 1
                if a.assets["sfx_item"]:
                    a.assets["sfx_item"].play()
                c.bactas.remove(b)
            elif b["rect"].top > c.HEIGHT:
                c.bactas.remove(b)

        # B) Corações (Upgrade de Vida Máxima)
        for coracao in c.coracoes[:]:
            # Dicionário: {"rect": Rect, "spawn": ticks}
            coracao["rect"].y += 2
            now = pygame.time.get_ticks()
            if (
                coracao["rect"].colliderect(c.player.inflate(8, 8))
                and now - coracao.get("spawn", 0) >= c.DROP_PICKUP_DELAY_MS
            ):
                c.estado["vida_maxima"] = 4
                if c.estado["vida"] < c.estado["vida_maxima"]:
                    c.estado["vida"] += 1
                if a.assets["sfx_item"]:
                    a.assets["sfx_item"].play()
                c.coracoes.remove(coracao)
            elif coracao["rect"].top > c.HEIGHT:
                c.coracoes.remove(coracao)

        # C) Escudos Defletores
        for ed in c.escudo_defletor[:]:
            # Dicionário: {"rect": Rect, "spawn": ticks}
            ed["rect"].y += 2
            now = pygame.time.get_ticks()
            if (
                ed["rect"].colliderect(c.player.inflate(8, 8))
                and now - ed.get("spawn", 0) >= c.DROP_PICKUP_DELAY_MS
            ):
                c.estado["escudo_ativo"] = True
                if a.assets["sfx_item"]:
                    a.assets["sfx_item"].play()
                c.escudo_defletor.remove(ed)
            elif ed["rect"].top > c.HEIGHT:
                c.escudo_defletor.remove(ed)

        # 5) Colisões inimigos

        # A) Tiros do Guardião contra Tie Fighters (Lacaios)
        for laser in c.tiros[:]:
            for inimigo in c.inimigos[:]:
                if laser.colliderect(inimigo["rect"].inflate(6, 6)):
                    if laser in c.tiros:
                        c.tiros.remove(laser)
                    c.inimigos.remove(inimigo)
                    c.estado["score"] += 10

                    c.explosoes_ativas.append(
                        {
                            "x": inimigo["rect"].x,
                            "y": inimigo["rect"].y,
                            "frame": 0,
                            "last_update": pygame.time.get_ticks(),
                        }
                    )

                    # Sorteio de drops
                    sorteio = random.random()
                    if sorteio < 0.05:
                        c.coracoes.append(
                            {
                                "rect": pygame.Rect(
                                    inimigo["rect"].x, inimigo["rect"].y - 40, 32, 32
                                ),
                                "spawn": pygame.time.get_ticks(),
                            }
                        )
                    elif sorteio < 0.13:
                        c.escudo_defletor.append(
                            {
                                "rect": pygame.Rect(
                                    inimigo["rect"].x, inimigo["rect"].y - 40, 32, 32
                                ),
                                "spawn": pygame.time.get_ticks(),
                            }
                        )
                    elif sorteio < 0.33:
                        c.bactas.append(
                            {
                                "rect": pygame.Rect(
                                    inimigo["rect"].x, inimigo["rect"].y - 40, 32, 32
                                ),
                                "spawn": pygame.time.get_ticks(),
                            }
                        )

        # B) Tiros dos inimigos colidindo com o jogador
        for laser in c.tiros_inimigos[:]:
            if laser["rect"].colliderect(c.player.inflate(-16, -12)):
                c.tiros_inimigos.remove(laser)

                # Escudo ativo
                if c.estado["escudo_ativo"]:
                    c.estado["escudo_ativo"] = False
                else:
                    c.estado["vida"] -= 2 if laser["vader"] else 1
                    if not c.estado.get("motivo_morte"):
                        c.estado["motivo_morte"] = (
                            "laser_vader" if laser["vader"] else "laser_inimigo"
                        )

                if a.assets["sfx_dano"]:
                    a.assets["sfx_dano"].play()
                if c.estado["vida"] <= 0:
                    processar_fim_de_partida(game_over())
                    return

        # Darth Vader e seus eventos
        if (
            c.estado["score"] >= 200
            and not c.estado["vader_ativo"]
            and not c.estado["vitoria_exibida"]
        ):
            c.estado["mostrar_mensagem_darth"] = True

        if c.estado["mostrar_mensagem_darth"]:
            exibir_mensagem_darth()
            continue

        if c.estado["vader_ativo"]:
            c.vader.x += c.estado["vader_direcao"] * 4

            if c.vader.x <= 10 or c.vader.x + c.vader.width >= c.WIDTH - 10:
                c.estado["vader_direcao"] *= -1
                c.vader.y += 20

            if c.vader.bottom >= c.player.top:
                c.estado["vida"] = 0
                c.estado["motivo_morte"] = "vader_chegou"
                processar_fim_de_partida(game_over())
                return

            if random.random() < 0.04:
                c.tiros_inimigos.append(
                    {
                        "rect": pygame.Rect(c.vader.centerx - 2, c.vader.bottom, 5, 10),
                        "vader": True,
                        "dx": 0,
                    }
                )
                c.tiros_inimigos.append(
                    {
                        "rect": pygame.Rect(c.vader.centerx - 2, c.vader.bottom, 5, 10),
                        "vader": True,
                        "dx": -2,
                    }
                )
                c.tiros_inimigos.append(
                    {
                        "rect": pygame.Rect(c.vader.centerx - 2, c.vader.bottom, 5, 10),
                        "vader": True,
                        "dx": 2,
                    }
                )

        for laser in c.tiros_inimigos:
            if "dx" in laser:
                laser["rect"].x += laser["dx"]

        # 3) Tiros do Guardião contra o Darth Vader
        if c.estado["vader_ativo"] and not c.estado["vitoria_exibida"]:
            for laser in c.tiros[:]:
                if laser.colliderect(c.vader.inflate(6, 6)):
                    c.tiros.remove(laser)
                    c.estado["vader_acertos"] += 1

                    c.explosoes_ativas.append(
                        {
                            "x": c.vader.x + random.randint(0, 20),
                            "y": c.vader.y + random.randint(0, 20),
                            "frame": 0,
                            "last_update": pygame.time.get_ticks(),
                        }
                    )
                    if a.assets["sfx_explosao"]:
                        a.assets["sfx_explosao"].play()

                    if c.estado["vader_acertos"] >= 5:
                        pontos = c.config_dificuldade[
                            c.estado["nivel_dificuldade_ativa"]
                        ]["pontos_vader"]
                        c.estado["score"] += pontos
                        c.estado["vitoria_exibida"] = True
                        processar_fim_de_partida(game_vitoria())
                        return

        # Renderização final na tela
        telas_view.tela_partida(inicio_tempo, tempo_pausado_total)
        pygame.display.flip()

        if c.estado["vida"] <= 0:
            if not c.estado.get("motivo_morte"):
                c.estado["motivo_morte"] = "vida_zerada"
            processar_fim_de_partida(game_over())
            return

        if len(c.inimigos) == 0 and not c.estado["vader_ativo"]:
            c.estado["wave"] += 1
            criar_onda(c.estado["wave"])
