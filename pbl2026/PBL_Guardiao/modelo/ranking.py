"Ranking:Gerenciamento da persistência de dados (hall_da_fama.json)"

import os
import json
import pygame
import sys
from datetime import datetime

from modelo.configuracoes import WIDTH, HEIGHT
import modelo.assets as a
import modelo.configuracoes as c
import view.menus as m

RANKING_FILE = "hall_da_fama.json"

def load_ranking():
    """Faz a leitura física do JSON de recordes e trata corrupções preventivamente."""
    if not os.path.exists(RANKING_FILE): 
        return [] # Se o arquivo não existir fisicamente no disco, devolve uma lista de dados vazia
    try:
        with open(RANKING_FILE, 'r', encoding='utf-8') as f:
            # Deserializa o texto puro do JSON convertendo-o de volta em uma lista nativa de dicionários do Python
            # Fonte: DevMedia
            return json.load(f).get("top_scores", [])
    except: 
        return [] # Retorna lista vazia caso os arquivos foram corrompidos ou modificados manualmente

def save_ranking(top_scores):
    """Grava fisicamente os recordes no disco com formatação bonitinha."""
    try:
        with open(RANKING_FILE, 'w', encoding='utf-8') as f:
            json.dump({"top_scores": top_scores}, f, indent=4, ensure_ascii=False)
    except: 
        pass

def update_ranking(nome_jogador, pontuacao):
    """Efetua a inserção do novo recorde, ordenação decrescente e poda do Top 10."""
    
    ranking_atual = load_ranking() # Carrega a tabela de recordistas atualizada do disco
    
    # Monta a nova entrada estruturada de dicionário para o novo recordista
    ranking_atual.append({
        "nome": nome_jogador if nome_jogador.strip() != "" else "GUARDIÃO", # default caso o jogador não insira um nome no rnk
        "pontuacao": pontuacao,
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    # O reverse=True garante que a ordenação comece pelo maior score.
    ranking_atual.sort(key=lambda x: x["pontuacao"], reverse=True)
    # ARmazena e exibe somente os 10 primeiros recordistas
    save_ranking(ranking_atual[:10])

def obter_nome_jogador():
    """Loop gráfico nativo do Pygame para capturar a digitação do nome do jogador."""
    
    nome = ""
    
    while True:
        c.screen.fill(m.PRETO)
        
        prompt = a.fonte_titulo.render("NOVO RECORDISTA! DIGITE SEU NOME:", True, m.AMARELO)
        txt_nome = a.fonte_titulo.render(nome + "_", True, m.BRANCO)
        alerta = a.fonte_hud.render("Pressione ENTER para Salvar", True, m.VERDE_MUSGO)
        
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
                    nome = nome[:-1] # Se apertar BACKSPACE, executa um fatiamento de string removendo o último caractere
                # Explicação do len(nome): restringe o tamanho máximo em 12 caracteres para evitar estouro de texto no HUD
                # e o e.unicode.isalnum() impede a digitação de caracteres especiais ou invisíveis que corrompem o JSON.
                elif len(nome) < 12 and e.unicode.isalnum(): 
                    nome += e.unicode.upper() # Concatena o caractere digitado forçando-o a ficar em caixa alta

def exibir_ranking():
    """Exibe na tela a tabela das 10 maiores pontuações persistidas no JSON."""
    while True:
        c.screen.fill(m.PRETO)
        titulo = a.fonte_titulo.render("TOP 10 - HALL DA FAMA", True, m.AMARELO)
        c.screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 50))
        
        ranking = load_ranking() # Requisita os recordes deserializados do arquivo JSON
        if not ranking:
            # Mensagem preventiva caso o arquivo JSON seja recém-criado ou esteja vazio
            vazio_txt = a.fonte_hud.render("NENHUM SCORE REGISTRADO AINDA.", True, m.CINZA)
            c.screen.blit(vazio_txt, (WIDTH // 2 - vazio_txt.get_width() // 2, HEIGHT // 2))
        else:
            # Varre os elementos retornados do JSON para imprimir o placar geral linha por linha
            for i, entrada in enumerate(ranking):
                # Cria uma string formatada alinhando o nome e os pontos usando espaçamento fixo à esquerda (<12)
                texto_linha = f"{i+1}. {entrada['nome']:<12} - {entrada['pontuacao']} PTS"
                # Primeiro colocado (Top 1) em verde, e os demais recordistas em branco
                cor_linha = m.VERDE if i == 0 else m.BRANCO
                txt_render = a.fonte_hud.render(texto_linha, True, cor_linha)
                c.screen.blit(txt_render, (WIDTH // 2 - 200, 120 + i * 35)) # Incrementa 35 pixels verticais por linha (Grid vertical)
                
        instrucao = a.fonte_titulo.render("PRESSIONE ENTER PARA VOLTAR", True, m.VERDE_MUSGO)
        c.screen.blit(instrucao, (WIDTH // 2 - instrucao.get_width() // 2, HEIGHT - 70))
        pygame.display.flip()
        
        # Escuta de eventos para fechar a janela ou retornar com segurança desempilhando a função
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN: 
                    return