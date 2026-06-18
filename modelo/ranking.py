import os
import json
import pygame
import sys
from datetime import datetime

from modelo.configuracoes import WIDTH, HEIGHT
import modelo.assets as a
import modelo.configuracoes as c
import view.hud as h

RANKING_FILE = "hall_da_fama.json"


def load_ranking():
    if not os.path.exists(RANKING_FILE):
        return []
    try:
        with open(RANKING_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("top_scores", [])
    except:
        return []


def save_ranking(top_scores):
    try:
        with open(RANKING_FILE, "w", encoding="utf-8") as f:
            json.dump({"top_scores": top_scores}, f, indent=4, ensure_ascii=False)
    except:
        pass


def update_ranking(nome_jogador, pontuacao):

    ranking_atual = load_ranking()

    ranking_atual.append(
        {
            "nome": nome_jogador if nome_jogador.strip() != "" else "GUARDIÃO",
            "pontuacao": pontuacao,
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )

    ranking_atual.sort(key=lambda x: x["pontuacao"], reverse=True)
    save_ranking(ranking_atual[:10])


def obter_nome_jogador():

    nome = ""

    while True:
        c.screen.fill(h.PRETO)

        prompt = a.assets["fonte_titulo"].render(
            "NOVO RECORDISTA! DIGITE SEU NOME:", True, h.AMARELO
        )
        txt_nome = a.assets["fonte_titulo"].render(nome + "_", True, h.BRANCO)
        alerta = a.assets["fonte_hud"].render(
            "Pressione ENTER para Salvar", True, h.VERDE_MUSGO
        )

        c.screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 3))
        c.screen.blit(txt_nome, (WIDTH // 2 - txt_nome.get_width() // 2, HEIGHT // 2))
        c.screen.blit(alerta, (WIDTH // 2 - alerta.get_width() // 2, HEIGHT // 2 + 80))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    return nome
                elif e.key == pygame.K_BACKSPACE:
                    nome = nome[
                        :-1
                    ]  # Se apertar BACKSPACE, fatia da string o ultimo caractere
                    # Explicação do len(nome): restringe o tamanho máximo em 12 caracteres para evitar estouro de texto no HUD
                    # e o e.unicode.isalnum() impede a digitação de caracteres especiais ou invisíveis que corrompem o JSON.
                elif len(nome) < 12 and e.unicode.isalnum():
                    nome += e.unicode.upper()


def exibir_ranking():
    while True:
        c.screen.fill(h.PRETO)
        titulo = a.assets["fonte_titulo"].render(
            "TOP 10 - HALL DA FAMA", True, h.AMARELO
        )
        c.screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 50))

        ranking = load_ranking()
        if not ranking:
            vazio_txt = a.assets["fonte_hud"].render(
                "NENHUM SCORE REGISTRADO AINDA.", True, h.CINZA
            )
            c.screen.blit(
                vazio_txt, (WIDTH // 2 - vazio_txt.get_width() // 2, HEIGHT // 2)
            )
        else:
            for i, entrada in enumerate(ranking):
                texto_linha = (
                    f"{i +1 }. {entrada ['nome']:<12} - {entrada ['pontuacao']} PTS"
                )
                cor_linha = h.VERDE if i == 0 else h.BRANCO
                txt_render = a.assets["fonte_hud"].render(texto_linha, True, cor_linha)
                c.screen.blit(txt_render, (WIDTH // 2 - 200, 120 + i * 35))

        instrucao = a.assets["fonte_titulo"].render(
            "PRESSIONE ENTER PARA VOLTAR", True, h.VERDE_MUSGO
        )
        c.screen.blit(instrucao, (WIDTH // 2 - instrucao.get_width() // 2, HEIGHT - 70))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    return
