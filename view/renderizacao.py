import pygame

import modelo.assets as a
import modelo.configuracoes as c
import view.hud as h


def renderizar_projeteis():
    for proj in c.tiros:
        pygame.draw.rect(c.screen, h.AZUL, proj)

    for tiro in c.tiros_inimigos:
        cor_tiro = h.VERMELHO if tiro["vader"] else h.AMARELO
        pygame.draw.rect(c.screen, cor_tiro, tiro["rect"])


def renderizar_player():
    if a.assets["img_player_frames"]:
        frame_atual_player = (pygame.time.get_ticks() // 200) % len(
            a.assets["img_player_frames"]
        )
        c.screen.blit(a.assets["img_player_frames"][frame_atual_player], c.player)
    else:
        ponto_topo = (c.player.centerx, c.player.top)
        ponto_esq = (c.player.left, c.player.bottom)
        ponto_dir = (c.player.right, c.player.bottom)
        pygame.draw.polygon(c.screen, h.VERDE, [ponto_topo, ponto_esq, ponto_dir])


def renderizar_inimigos_explodindo():
    tempo_agora = pygame.time.get_ticks()
    for exp in c.explosoes_ativas[:]:
        if a.assets["img_explosao_frames"]:
            c.screen.blit(
                a.assets["img_explosao_frames"][exp["frame"]], (exp["x"], exp["y"])
            )
            if tempo_agora - exp["last_update"] > 60:
                exp["frame"] += 1
                exp["last_update"] = tempo_agora
                if exp["frame"] >= len(a.assets["img_explosao_frames"]):
                    c.explosoes_ativas.remove(exp)
        else:
            c.explosoes_ativas.remove(exp)


def renderizar_tie_fighters():
    if not c.estado["vader_ativo"]:
        for inimigo in c.inimigos:
            if a.assets["img_inimigo"]:
                c.screen.blit(a.assets["img_inimigo"], inimigo["rect"])
            else:
                # Fallback: retângulos
                pygame.draw.rect(c.screen, h.VERMELHO, inimigo["rect"])


def renderizar_vader():
    if c.estado["vader_ativo"]:
        if a.assets["img_vader"]:
            c.screen.blit(a.assets["img_vader"], c.vader)
        else:
            # Fallback: quadrado 60x60 px
            pygame.draw.rect(c.screen, (150, 0, 0), c.vader)


def _rect_from_drop(item):
    return item["rect"] if isinstance(item, dict) else item


def _renderizar_drop(lista, imagem, cor_padrao, forma_fallback="rect"):
    for item in lista:
        rect = _rect_from_drop(item)
        if imagem:
            c.screen.blit(imagem, rect)
        elif forma_fallback == "ellipse":
            pygame.draw.ellipse(c.screen, cor_padrao, rect)
        else:
            pygame.draw.rect(c.screen, cor_padrao, rect)


def renderizar_bactas():
    _renderizar_drop(c.bactas, a.assets["img_bacta"], h.TURQUESA)

    for v in range(c.estado["vida"]):
        if a.assets["img_coracao"]:
            c.screen.blit(a.assets["img_coracao"], (110 + v * 35, 50))
        else:
            pygame.draw.rect(c.screen, (255, 182, 193), (110 + v * 35, 55, 20, 20))


def renderizar_coracoes():
    _renderizar_drop(c.coracoes, a.assets["img_coracao"], (255, 182, 193))


def renderizar_escudos():
    _renderizar_drop(
        c.escudo_defletor,
        a.assets.get("img_escudo"),
        (0, 191, 255),
        forma_fallback="ellipse",
    )


def renderizar_aura_protecao():
    if c.estado["escudo_ativo"]:
        pygame.draw.circle(
            c.screen, (0, 255, 255), c.player.center, c.player.width // 2 + 10, 2
        )
