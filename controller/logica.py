""""
Banco de dados para todas as funções lógicas do jogo,
desde movimentos, colisões diversas, controle de ondas, 
loops temporais, janela de pausa, drops de Bacta, IA do Vader, etc.
"""

import pygame
import sys
import random
import time

import modelo.configuracoes as c
import modelo.assets as a
import modelo.ranking as rnk
import view.menus as m
import view.jogabilidade as j

def colisao_recuo_inimigos():
    """Gerencia instinto de fuga aos inimigos.
    Explicação: Cada inimigo checa frame a frame a proximidade do player,
    caso próximo, recua horizontalmente."""
    
    PX_RAIO_LIMITE = 120
    
    for inimigo in c.inimigos[:]:
        dx = c.player.centerx - inimigo['rect'].centerx
        dy = c.player.centery - inimigo['rect'].centery
        distancia = (dx**2 + dy**2) ** 0.5
        
        if distancia < PX_RAIO_LIMITE:
            if dx > 0:
                inimigo['rect'].x -= 4
            else:
                inimigo['rect'].x += 4
                
            if inimigo['rect'].x < 0:
                inimigo['rect'].x = 0
            elif inimigo['rect'].x + inimigo['rect'].width > c.WIDTH:
                inimigo['rect'].x = c.WIDTH - inimigo['rect'].width
                
            inimigo['rect'].y += int(c.velocidade_inimigos)
        else:
            inimigo['rect'].y += int(c.velocidade_inimigos)
            
        if inimigo['rect'].top > c.HEIGHT:
            c.inimigos.remove(inimigo)
            c.estado["vida"] -= 1
            if a.assets["sfx_dano"]: a.assets["sfx_dano"].play()

def criar_onda(wave_idx):
    """Essa matriz de spawn foi inspirada no exercício do tabuleiro 'Big Joe' (Desafios matrizes)"""

    c.inimigos.clear()
    
    # Correção de bug: Uso do operador % para mitigar o estouro de índices que resultavam em crashes
    # Explicação: Se o score do jogador for > 200, o ciclo de ondas se repete.
    matriz = c.ondas[wave_idx % len(c.ondas)]
    
    # Varredura da matriz de spawn para posicionamento horizontal dos Tie Fighters
    for i, v in enumerate(matriz):
        if v == 1:
            x = 100 + i * 80
            # Posicionamento único para cada inimigo (evitar spawns sobrepostos)
            y = -50 - (random.randint(0, 2) * 40)

            # Dicionário dos inimigos: rect de colisão e vida interna
            # Ótimo para futuras melhorias.
            c.inimigos.append({'rect': pygame.Rect(x, y, 40, 40), 'vida': 1})
            
    # Velocidade progressiva: Acelera os inimigos a cada nova onda,
    # mas nunca ultrapassar os limites permitidos para cada dificuldade 
    # (vide 'def controle_dificuldade()' in c.py)
    if wave_idx > 0:
        config = c.config_dificuldade[c.estado["nivel_dificuldade_ativa"]]

        # Restringe a aceleração usando min() para respeitar o teto de dificuldade definida no menu
        c.velocidade_inimigos = min(c.velocidade_inimigos + config['incremento'], config['limite'])

    c.estado["wave"] = wave_idx

def mover_inimigos():
    """Gerencia a descida gradual das naves imperiais e penalização de vida no HUD."""
    for inimigo in c.inimigos[:]:
        inimigo['rect'].y += int(c.velocidade_inimigos)
        
        # Se ultrapassar o limite inferior da tela... --->
        if inimigo['rect'].top > c.HEIGHT:
            c.inimigos.remove(inimigo)
            c.estado["vida"] -= 1     # <--- decrementa vida
            if a.assets["sfx_dano"]: 
                a.assets["sfx_dano"].play()

def gerenciar_pausa():
    """
    Aplicado congelamento completo de todos os atores e do cronômetro.
    """
    inicio_pausa = time.time()  # Registra o instante exato em que o jogo congelou
    while c.estado["pause"]:
        m.mostrar_menu_pausa()
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                # Pressionar 'P' ou 'ESC' retoma a execução normal desativando a flag
                if e.key == pygame.K_p or e.key == pygame.K_ESCAPE:
                    c.estado["pause"] = False
                    
    # Retorna o total de segundos gastos pausado para descontar do cronômetro principal
    return time.time() - inicio_pausa

def iniciar_jogo():
    """Tem a importante missão de limpar todas as listas da memória antes de inicializar a partida."""
    c.estado["vitoria_exibida"] = False
    c.estado["mostrar_mensagem_darth"] = False
    c.estado["pause"] = False
    c.estado["score"] = 0
    c.estado["wave"] = 0
    c.estado["vader_ativo"] = False
    
    # Posicionamento centralizado inicial do Boss
    c.vader.x = c.WIDTH // 2 - c.vader.width // 2
    c.vader.y = 50  
    c.estado["vader_acertos"] = 0
    
    # Gerenciamento de dificuldade (vide modelo.configurações.py):
    # Define a vida conforme a escolha do menu principal
    c.controle_dificuldade()
    c.velocidade_inimigos = c.config_dificuldade[c.estado["nivel_dificuldade_ativa"]]['inicial']
    
    # Reseta a posição do quadrado do jogador
    c.player.x = c.WIDTH // 2 - c.player.width // 2
    c.player.y = c.HEIGHT - 80
    
def limpar_tela():
    c.inimigos.clear()
    c.tiros.clear()
    c.tiros_inimigos.clear()
    c.bactas.clear()
    c.explosoes_ativas.clear()
    
    # Fabrica a primeira leva de naves da partida
    criar_onda(c.estado["wave"])

def exibir_mensagem_darth():
    while True:
        c.screen.fill(m.PRETO)
        msg = a.assets["fonte_titulo"].render("DARTH VADER SE APROXIMA!", True, m.VERMELHO)
        instr = a.assets["fonte_hud"].render("Pressione ENTER para Enfrentá-lo", True, m.VERDE_MUSGO)
        c.screen.blit(msg, (c.WIDTH // 2 - msg.get_width() // 2, c.HEIGHT // 3))
        c.screen.blit(instr, (c.WIDTH // 2 - instr.get_width() // 2, c.HEIGHT // 3 + 60))
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
    # Melhoria: elaborada função encapsulada pois foi aplicada em vários contextos.
    ranking = rnk.load_ranking()
    # Verifica se a tabela tem menos de 10 recordes ou se o score atual supera o último colocado
    if len(ranking) < 10 or c.estado["score"] > ranking[-1]['pontuacao']:
        nome_salvo = rnk.obter_nome_jogador()
        rnk.update_ranking(nome_salvo, c.estado["score"])
        rnk.exibir_ranking()

def atualizar_projeteis(lista_tiros, velocidade_y, eh_laser_jogador=True):
    """
    O 'eh_laser_jogador' diferencia se caso os lasers são do herói (True, então o laser sobe)
    or dos inimigos (False, lasers descem), que possuem dados extras de direção e dano."""
    for t in lista_tiros[:]:
        # Para lasers do jogador, extrai a Rect diretamente. Para inimigos, extrai o 'rect' do dicionário aninhado
        rect_objeto = t if eh_laser_jogador else t['rect']
        rect_objeto.y += velocidade_y
        
        # Verifica fronteira superior (jogador) ou inferior (inimigo)
        if (eh_laser_jogador and rect_objeto.bottom < 0) or (not eh_laser_jogador and rect_objeto.top > c.HEIGHT):
            lista_tiros.remove(t)

"""O nome é autoexplicativo: garante inicialização limpa completa antes de
de engajar um evento ou tela, evitando empilhamento infinito"""            
def capturar_evento_e_reiniciar_jogo():
    for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    pygame.mixer.stop()          # Corta a música de Game Over
                    a.tocar_musica_tema()        # Recarrega a trilha sonora de partida
                    iniciar_jogo()               # Reseta os arrays da memória
                    limpar_tela()
                    return
                elif e.key == pygame.K_ESCAPE:
                    pygame.mixer.stop()
                    pygame.quit()
                    sys.exit()
        
# Guia 5: JSON
def game_over():
    """Gerencia a persistência automática do ranking no JSON e rotina de derrota."""
    pygame.mixer.music.stop()
    if a.assets["sfx_gameover"]: 
        a.assets["sfx_gameover"].play()
        
    verificar_e_atualizar_ranking()
        
    while True:
        j.tela_game_over()
        capturar_evento_e_reiniciar_jogo()
        return

def game_vitoria():
    """Gerencia a persistência automática do ranking no JSON e pontuação de vitória."""
    pygame.mixer.music.stop()
    if a.assets["sfx_vitoria"]: 
        a.assets["sfx_vitoria"].play()
    
    verificar_e_atualizar_ranking()
        
    while True:
        j.tela_vitoria()
        capturar_evento_e_reiniciar_jogo()
        return

def main_loop():
    """Loop central de execução de jogabilidade."""
    inicio_tempo = time.time()    # Marca a estampa de tempo real de início de combate
    tempo_pausado_total = 0       # Zera o acumulador de congelamento de telas
    clock = pygame.time.Clock()
    
    limpar_tela()

    while True:
        # Melhoria - Controle de pausa: Se o jogo for pausado, captura e desconta os segundos ociosos
        if c.estado["pause"]:
            tempo_pausado_total += gerenciar_pausa()
            continue

        clock.tick(60)
        
        # loop do jogo
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_m:
                    c.alternar_pausar_musica()
                if e.key == pygame.K_p or e.key == pygame.K_ESCAPE:
                    c.estado["pause"] = True
                # Explicação: ESPAÇO cria um novo feixe de laser logo acima do topo da nave do Guardião
                if e.key == pygame.K_SPACE:
                    c.tiros.append(pygame.Rect(c.player.centerx - 5, c.player.top - 10, 10, 20))
                    if a.assets["sfx_laser"]: 
                        a.assets["sfx_laser"].play()
            # Capturar clique no botão de musica
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1: # Clique com o botão esquerdo do mouse
                    # Verifica se a coordenada do clique (e.pos) está dentro do nosso Rect
                    if c.msc_botao.collidepoint(e.pos):
                        c.alternar_pausar_musica() # Altera o booleano e aplica pause/unpause
                        
        # Varredura de teclas pressionadas para movimentação omnidirecional
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: c.player.x -= 5
        if keys[pygame.K_RIGHT]: c.player.x += 5
        if keys[pygame.K_UP]: c.player.y -= 5
        if keys[pygame.K_DOWN]: c.player.y += 5
        # Definição de limites de movimento do player para evitar sumir das bordas
        c.player.clamp_ip(pygame.Rect(0, 0, c.WIDTH, c.HEIGHT))
        
        if not c.estado["vader_ativo"]: # Verifica colisao  direta guardião-inimigo
            # Reduz a hitbox do jogador para a colisão contra os inimigos comuns ficar menos agressiva nas pontas das asas.
            for inimigo in c.inimigos[:]:
                if c.player.inflate(-16, -12).colliderect(inimigo['rect']):
                    c.inimigos.remove(inimigo)
                    c.estado["vida"] -= 1
                    if a.assets["sfx_dano"]: a.assets["sfx_dano"].play()
                    c.explosoes_ativas.append({
                        'x': inimigo['rect'].x, 'y': inimigo['rect'].y,
                        'frame': 0, 'last_update': pygame.time.get_ticks()
                    })
                    if c.estado["vida"] <= 0:
                        game_over()
                        return
        
        atualizar_projeteis(c.tiros, -16, eh_laser_jogador=True)

        # Se o Boss final não estiver ativo, continua descendo os stormtropers do Império
        if not c.estado["vader_ativo"]:
            colisao_recuo_inimigos()

        # Mecanismo para taxa probabilística de disparo das naves inimigas (Tie Fighters)
        taxa_disparo = 0.008 if c.estado["nivel_dificuldade_ativa"] == 'facil' else (0.015 if c.estado["nivel_dificuldade_ativa"] == 'medio' else 0.023)
        if random.random() < taxa_disparo and c.inimigos and not c.estado["vader_ativo"]:
            inimigo = random.choice(c.inimigos)
            # Adiciona o laser roxo do lacaio à lista de vetores de perigo
            c.tiros_inimigos.append({'rect': pygame.Rect(inimigo['rect'].centerx - 2, inimigo['rect'].bottom, 5, 10), 'vader': False})

        # Processamento físico de descida e colisão de Bactas (cura Guardião)
        for b in c.bactas[:]:
            b.y += 2
            # Infla a área do jogador para facilitar a coleta dos itens de cura (efeito magnético).
            if b.colliderect(c.player.inflate(8, 8)):
                # Restringe a cura máxima com base na dificuldade para evitar trapaças 
                teto_vida = 3
                if c.estado["vida"] < teto_vida:
                    c.estado["vida"] += 1
                if a.assets["sfx_bacta"]: 
                    a.assets["sfx_bacta"].play()
                c.bactas.remove(b)
            elif b.top > c.HEIGHT: 
                c.bactas.remove(b)

        atualizar_projeteis(c.tiros_inimigos, 5, eh_laser_jogador=False)

        # Colisões de Tiros do Guardião contra Tie Fighters Comuns
        for t in c.tiros[:]:
            for inimigo in c.inimigos[:]:
                # Infla um pouco os inimigos para os tiros do jogador acertarem mais fácil se passarem raspando.
                if t.colliderect(inimigo['rect'].inflate(6, 6)):
                    if t in c.tiros: 
                        c.tiros.remove(t)
                    
                    # Aloca a animação de explosão das naves inimigas por frame
                    c.explosoes_ativas.append({
                        'x': inimigo['rect'].x, 'y': inimigo['rect'].y, 
                        'frame': 0, 'last_update': pygame.time.get_ticks()
                    })
                    
                    c.inimigos.remove(inimigo)
                    c.estado["score"] += 10  # Stormtrooper/Tie Fighter computa 10 pontos de score
                    
                    if random.random() < 0.2: # Sorteio de drops de cápsula de Bacta (20% de chance)
                        c.bactas.append(pygame.Rect(inimigo['rect'].x, inimigo['rect'].y, 32, 32))
                    if a.assets["sfx_explosao"]: 
                        a.assets["sfx_explosao"].play()
                    break

        # INTERSECÇÃO GEOMÉTRICA: Tiros do Império atingindo a nave rebelde do Guardião
        for t in c.tiros_inimigos[:]:
            # Encolhe a hitbox do jogador para os lasers inimigos não acertarem as pontas invisíveis das asas.
            if t['rect'].colliderect(c.player.inflate(-16, -12)):
                c.tiros_inimigos.remove(t)
                # Dano remove 2 vidas se for feixe Sith ou 1 se for tiro comum
                c.estado["vida"] -= 2 if t['vader'] else 1
                if a.assets["sfx_dano"]: 
                    a.assets["sfx_dano"].play()
                if c.estado["vida"] <= 0:
                    game_over()
                    return

        # Critério para evento Boss - se bater 200 pontos.
        # Melhoria: para as ondas normais e evoca a tela modal do Darth Vader
        if c.estado["score"] >= 200 and not c.estado["vader_ativo"] and not c.estado["vitoria_exibida"]:
            c.estado["mostrar_mensagem_darth"] = True

        if c.estado["mostrar_mensagem_darth"]:
            exibir_mensagem_darth()
            continue

        # Inteligência artificial do Darth Vader
        if c.estado["vader_ativo"]:
            # Incrementa deslocamento lateral contínuo do Boss
            c.vader.x += c.estado["vader_direcao"] * 4
            
            # Rebatida nas bordas della tela: Inverte a direção e avança verticalmente esmagando a base
            if c.vader.x <= 10 or c.vader.x + c.vader.width >= c.WIDTH - 10:
                c.estado["vader_direcao"] *= -1
                c.vader.y += 20  # Avanço progressivo vertical em zigue-zague
                
            # Fail-state instantâneo se o Lorde Sith invadir o perímetro do jogador
            if c.vader.bottom >= c.player.top: 
                c.estado["vida"] = 0
                game_over()
                return

            # Disparo triplo em leque geométrico inspirado em Jesse Schell Challenge Lens
            if random.random() < 0.04:
                # Aloca três projéteis no mesmo local, mas observando deslocamentos laterais distintos (dx)
                c.tiros_inimigos.append({'rect': pygame.Rect(c.vader.centerx - 2, c.vader.bottom, 5, 10), 'vader': True, 'dx': 0})
                c.tiros_inimigos.append({'rect': pygame.Rect(c.vader.centerx - 2, c.vader.bottom, 5, 10), 'vader': True, 'dx': -2})
                c.tiros_inimigos.append({'rect': pygame.Rect(c.vader.centerx - 2, c.vader.bottom, 5, 10), 'vader': True, 'dx': 2})

        # Processamento vetorial do deslocamento lateral oblíquo do leque triplo de lasers do Boss
        for t in c.tiros_inimigos:
            if 'dx' in t: 
                t['rect'].x += t['dx']

        # Verifica tiros do Guardião atingindo o Darth Vader
        if c.estado["vader_ativo"] and not c.estado["vitoria_exibida"]:
            for t in c.tiros[:]:
                # Aumenta ligeiramente a hitbox do Boss final para ficar mais satisfatório acertar tiros nele.
                if t.colliderect(c.vader.inflate(6, 6)):
                    c.tiros.remove(t)
                    c.estado["vader_acertos"] += 1  # Incrementa o medidor de impactos no Boss
                    
                    # Melhoria: Gera faíscas e pequenas explosões posicionais no Vader
                    c.explosoes_ativas.append({
                        'x': c.vader.x + random.randint(0, 20), 'y': c.vader.y + random.randint(0, 20), 
                        'frame': 0, 'last_update': pygame.time.get_ticks()
                    })
                    if a.assets["sfx_explosao"]: 
                        a.assets["sfx_explosao"].play()
                        
                    # Condição de vitória
                    if c.estado["vader_acertos"] >= 5:
                        c.estado["score"] += 200
                        c.estado["vitoria_exibida"] = True
                        game_vitoria()
                        return

        # Renderização
        j.desenhar_cenario(inicio_tempo, tempo_pausado_total)
        pygame.display.flip()

        # Critérios de game over e vitória
        if c.estado["vida"] <= 0:
            game_over()
            return

        if len(c.inimigos) == 0 and not c.estado["vader_ativo"]:
            c.estado["wave"] += 1
            criar_onda(c.estado["wave"])
