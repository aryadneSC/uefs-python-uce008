"""Centraliza toda a renderização de efeitos, sons, gráficos, etc"""
import pygame
import time

import modelo.configuracoes as c
import modelo.assets as assets
import view.menus as m

# Motivo de uso da função: Automatiza o cálculo matemático de alinhamento horizontal 
def desenhar_texto_centralizado(superficie_texto, altura_y):
    """Calcula o alinhamento horizontal perfeito e carimba o texto na tela."""
    posicao_x = c.WIDTH // 2 - superficie_texto.get_width() // 2
    c.screen.blit(superficie_texto, (posicao_x, altura_y))

def desenhar_cenario(inicio_tempo, tempo_pausado_total):
    """Pinta e atualiza recursivamente todos os elementos dinâmicos do campo de batalha.
    Esta função roda a cada iteração do clock (60 FPS) redesenhando a tela do zero."""
    # Renderização do background (Camada Inferior - Fundo do Tabuleiro):
    if assets.img_fundo: 
        c.screen.blit(assets.img_fundo, (0, 0))
    else: 
        # Fallback caso a imagem space-2 falhe, limpa a tela pintando preto absoluto
        c.screen.fill(m.PRETO)
        
    # Renderização do Caça (player)
    if assets.img_player_frames:
        # o pygame.time.get_ticks() mede o tempo total que o jogo está aberto em milissegundos.
        # Dividir por 200 significa que a imagem muda a cada 200 milissegundos (velocidade do motor).
        # O operador '%' por 2 alterna ciclicamente os índices apenas entre 0 e 1 de forma infinita.
        frame_atual_player = (pygame.time.get_ticks() // 200) % 2
        c.screen.blit(assets.img_player_frames[frame_atual_player], c.player)
    else: 
        # Fallback: desenha um retângulo verde primitivo se as sprites da pasta player sumirem
        pygame.draw.rect(c.screen, m.VERDE, c.player)
        
    # Renderização dos Tie Fighters
    if not c.estado["vader_ativo"]:
        for inimigo in c.inimigos:
            if assets.img_inimigo: 
                c.screen.blit(assets.img_inimigo, inimigo['rect'])
            else: 
                # Fallback: desenha retângulos vermelhos primitivos
                pygame.draw.rect(c.screen, m.VERMELHO, inimigo['rect'])
                
    # Renderização das bactas
    for b in c.bactas:
        if assets.img_bacta: 
            # Blita o sprite da cápsula médica na sua coordenada atual de descida
            c.screen.blit(assets.img_bacta, b)
        else: 
            # Fallback: desenha quadrados primitivos
            pygame.draw.rect(c.screen, m.TURQUESA, b)
            
    # Animação procedural da explosão:
    tempo_agora = pygame.time.get_ticks()
    # Uso da [:] para iterar de forma segura enquanto são removidos elements da lista original
    for exp in c.explosoes_ativas[:]:
        if assets.img_explosao_frames:
            # Puxa o quadro atual mapeado no dicionário da explosão específica
            c.screen.blit(assets.img_explosao_frames[exp['frame']], (exp['x'], exp['y']))
            # Troca de quadro a cada 60 milissegundos para garantir fluidez visual de estilhaços de energia
            if tempo_agora - exp['last_update'] > 60:
                exp['frame'] += 1 # Avança para o próximo PNG da animação
                exp['last_update'] = tempo_agora # Reseta o carimbo de última atualização do frame
                if exp['frame'] >= 5: 
                    # Se estourar o limite de 5 quadros (0 a 4), deleta a explosão da memória (Coleta de lixo ativa)
                    c.explosoes_ativas.remove(exp)
        else: 
            # Se não houver sprites de explosão na pasta, limpa o array imediatamente para não travar o loop
            c.explosoes_ativas.remove(exp)
    
    # Botão de pausar e despausar musica
    img_msc = getattr(assets, "img_icone_msc", None)
    if img_msc:
        # Se as imagens carregaram, blita o ícone correspondente (0 para ativo, 1 para mutado)
        indice_imagem = 1 if c.estado["musica_pausada"] else 0
        c.screen.blit(img_msc[indice_imagem], c.msc_botao)
    else:
        cor_botao = m.VERMELHO_PASTEL if c.estado["musica_pausada"] else m.AMARELO
        pygame.draw.rect(c.screen, cor_botao, c.msc_botao)
    
    fonte_msc = assets.fonte_hud.render("(M)", True, m.BRANCO)
    c.screen.blit(fonte_msc, (c.msc_botao.x + (c.msc_botao.width // 2) - (fonte_msc.get_width() // 2), c.msc_botao.y + 35))
    
    # Renderização dos lasers
    for t in c.tiros: 
        pygame.draw.rect(c.screen, m.AZUL, t)
        
    for t in c.tiros_inimigos:
        cor_tiro = m.VERMELHO if t['vader'] else m.AMARELO
        pygame.draw.rect(c.screen, cor_tiro, t['rect'])
        
    # Renderização do Boss
    if c.estado["vader_ativo"]:
        if assets.img_vader: 
            c.screen.blit(assets.img_vader, c.vader)
        else: 
            # Fallback: desenha um bloco vermelho escuro de tamanho 60x60 pixels
            pygame.draw.rect(c.screen, (150, 0, 0), c.vader)

    # Exibição da pontuação, vida e cronômetro
    score_txt = assets.fonte_hud.render(f"Score: {c.estado['score']}", True, m.BRANCO)
    vida_txt = assets.fonte_hud.render(f"Vida: {c.estado['vida']}", True, m.BRANCO)
    # Explicação '% 3600': Desconta os segundos em que o jogo permaneceu pausado
    tempo_atual = int(time.time() - inicio_tempo - tempo_pausado_total) % 3600 
    # Formata a saída numérica em formato 00:00 (ex: 02:05) usando divisão inteira e resto
    tempo_txt = assets.fonte_hud.render(f"Tempo: {tempo_atual//60:02d}:{tempo_atual%60:02d}", True, m.BRANCO)
    # Grid da interface estática
    c.screen.blit(score_txt, (10, 10))  # Canto superior esquerdo (Margem de 10 pixels)
    c.screen.blit(vida_txt, (10, 50))   # Logo abaixo do score, com alinhamento vertical
    c.screen.blit(tempo_txt, (c.WIDTH - 250, 10)) # Alinhado à direita subtraindo a largura estimada do texto

def tela_game_over():
    """Desenha a tela modal preta estática de derrota imediata ao perder os escudos."""
    c.screen.fill(m.PRETO)
    msg = assets.fonte_titulo.render("GAME OVER", True, m.VERMELHO)
    instr = assets.fonte_hud.render("R para Reiniciar - ESC para Sair", True, m.BRANCO)
    
    desenhar_texto_centralizado(msg, c.HEIGHT // 3)
    desenhar_texto_centralizado(instr, c.HEIGHT // 3 + 60)
    pygame.display.flip()

def tela_vitoria():
    """Desenha a tela modal preta estática de triunfo definitivo ao derrotar Darth Vader."""
    c.screen.fill(m.PRETO)
    msg = assets.fonte_titulo.render("VOCÊ VENCEU! A GALÁXIA ESTÁ SALVA!", True, m.VERDE)
    instr = assets.fonte_hud.render("Press R para Reiniciar ou ESC para voltar ao menu", True, m.BRANCO)
    
    desenhar_texto_centralizado(msg, c.HEIGHT // 3)
    desenhar_texto_centralizado(instr, c.HEIGHT // 3 + 60)
    pygame.display.flip()