import os
import json
import pygame
import sys
from datetime import datetime

from modelo.configuracoes import WIDTH, HEIGHT
import modelo.assets as a
import modelo.configuracoes as c
import view.hud as h

# Mesmo raciocínio do assets.py: caminho absoluto evita que o ranking "suma"
# quando o jogo é executado de um diretório diferente (ex: rodando pela IDE
# vs. rodando pelo terminal em outra pasta).
RANKING_FILE = os.path.join(a.BASE_DIR, "hall_da_fama.json")


def load_ranking():
    if not os.path.exists(RANKING_FILE):
        return []
    try:
        with open(RANKING_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("top_scores", [])
    except Exception as erro:
        print(f"[ranking] Falha ao ler {RANKING_FILE}: {erro}")
        return []


def save_ranking(top_scores):
    try:
        with open(RANKING_FILE, "w", encoding="utf-8") as f:
            json.dump({"top_scores": top_scores}, f, indent=4, ensure_ascii=False)
    except Exception as erro:
        print(f"[ranking] Falha ao salvar {RANKING_FILE}: {erro}")


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


def remover_entrada_ranking(indice):
    ranking = load_ranking()
    if 0 <= indice < len(ranking):
        if ranking[indice].get("nome", "").upper() == "LUKE":
            return False
        del ranking[indice]
        save_ranking(ranking)
        return True
    return False


def obter_nome_jogador():
    nome = ""
    clock = pygame.time.Clock()

    while True:
        clock.tick(30)
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
                    nome = nome[:-1]  # Se apertar BACKSPACE, fatia da string o ultimo caractere

                    # e o e.unicode.isalnum() evita a corrupção do JSON por digitação de caracteres especiais ou invisíveis.
                elif len(nome) < 12 and e.unicode.isalnum():
                    nome += e.unicode.upper()


def exibir_ranking():
    selected = 0
    mensagem = ""
    confirm_remocao = False
    clock = pygame.time.Clock()

    while True:
        clock.tick(30)
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
            selected = min(selected, len(ranking) - 1)
            for i, entrada in enumerate(ranking):
                texto_linha = (
                    f"{i + 1}. {entrada['nome']:<12} - {entrada['pontuacao']} PTS"
                )
                cor_linha = h.VERDE if i == 0 else h.BRANCO
                if i == selected:
                    selecionado_rect = pygame.Rect(
                        WIDTH // 2 - 210, 118 + i * 35, 420, 32
                    )
                    pygame.draw.rect(c.screen, h.VERDE_MUSGO, selecionado_rect, 2)
                txt_render = a.assets["fonte_hud"].render(texto_linha, True, cor_linha)
                c.screen.blit(txt_render, (WIDTH // 2 - 200, 120 + i * 35))

        # Para remoção de nome
        if confirm_remocao:
            instrucao = a.assets["fonte_titulo"].render(
                "TEM CERTEZA? [S] Sim - [N] Não",
                True,
                h.VERMELHO,
            )
        else:
            instrucao = a.assets["fonte_titulo"].render(
                "[R] Remover - [ENTER] Voltar",
                True,
                h.VERDE_MUSGO,
            )
        c.screen.blit(instrucao, (WIDTH // 2 - instrucao.get_width() // 2, HEIGHT - 90))

        if mensagem:
            mensagem_txt = a.assets["fonte_hud"].render(mensagem, True, h.BRANCO)
            c.screen.blit(
                mensagem_txt,
                (WIDTH // 2 - mensagem_txt.get_width() // 2, HEIGHT - 50),
            )

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and not confirm_remocao:
                    return
                if ranking:
                    if e.key == pygame.K_UP:
                        selected = max(selected - 1, 0)
                        confirm_remocao = False
                    elif e.key == pygame.K_DOWN:
                        selected = min(selected + 1, len(ranking) - 1)
                        confirm_remocao = False
                    elif e.key == pygame.K_n and confirm_remocao:
                        confirm_remocao = False
                    elif e.key == pygame.K_r and not confirm_remocao:
                        if ranking[selected].get("nome", "").upper() == "LUKE":
                            mensagem = "LUKE não pode ser removido."
                        else:
                            confirm_remocao = True
                    elif e.key == pygame.K_s and confirm_remocao:
                        if ranking[selected].get("nome", "").upper() == "LUKE":
                            mensagem = "LUKE não pode ser removido."
                        elif remover_entrada_ranking(selected):
                            ranking = load_ranking()
                            selected = min(selected, max(len(ranking) - 1, 0))
                            mensagem = "Registro removido."
                        else:
                            mensagem = "Não foi possível remover este registro."
                        confirm_remocao = False
