"""
Lógica relacionada aos inimigos: movimentação, recuo defensivo
e geração das ondas (waves) de Tie Fighters.
"""

import pygame 
import random 

import modelo.configuracoes as c 
import modelo.assets as a 


def colisao_recuo_inimigos ():
    """Gerencia instinto de fuga aos inimigos.
    Explicação: Cada inimigo checa frame a frame a proximidade do player,
    caso próximo, recua horizontalmente."""

    PX_RAIO_LIMITE = 120 

    for inimigo in c.inimigos [:]:
        dx = c.player.centerx - inimigo ['rect'].centerx 
        dy = c.player.centery - inimigo ['rect'].centery 
        distancia = (dx **2 + dy **2 )**0.5 

        if distancia < PX_RAIO_LIMITE :
            if dx > 0 :
                inimigo ['rect'].x -= 4 
            else :
                inimigo ['rect'].x += 4 

            if inimigo ['rect'].x < 0 :
                inimigo ['rect'].x = 0 
            elif inimigo ['rect'].x +inimigo ['rect'].width > c.WIDTH :
                inimigo ['rect'].x = c.WIDTH - inimigo ['rect'].width 

            inimigo ['rect'].y += int (c.velocidade_inimigos )
        else :
            inimigo ['rect'].y += int (c.velocidade_inimigos )

        if inimigo ['rect'].top > c.HEIGHT :
            c.inimigos.remove (inimigo )
            c.estado ["vida"]-= 1 
            if a.assets ["sfx_dano"]:a.assets ["sfx_dano"].play ()


def criar_onda (wave_idx ):
    """Esta matriz de spawn foi inspirada no exercício do tabuleiro 'Big Joe' (Desafios matrizes)"""

    c.inimigos.clear ()

    # Correção de bug: Uso do operador % para mitigar o estouro de índices que resultavam em crashes
    # Explicação: Se o score do jogador for > 200, o ciclo de ondas se repete.
    matriz = c.ondas [wave_idx %len (c.ondas )]

    # Varredura da matriz de spawn para posicionamento horizontal dos Tie Fighters
    for i,v in enumerate (matriz ):
        if v == 1 :
            x = 100 + i * 80 
            # Posicionamento único para cada inimigo (evitar spawns sobrepostos)
            y = -50 -(random.randint (0, 2) * 40 )

            # Dicionário dos inimigos: rect de colisão e vida interna
            # Ótimo para futuras melhorias.
            c.inimigos.append ({'rect':pygame.Rect (x, y, 40, 40 ),'vida':1 })

            # Velocidade progressiva: Acelera os inimigos a cada nova onda,
            # mas nunca ultrapassar os limites para cada dificuldade 
    if wave_idx > 0 :
        config = c.config_dificuldade [c.estado ["nivel_dificuldade_ativa"]]

        # Restringe a aceleração usando min() para respeitar o teto de dificuldade definida no menu
        c.velocidade_inimigos = min (c.velocidade_inimigos +config ['incremento'],config ['limite'])

    c.estado ["wave"] = wave_idx 


def mover_inimigos ():
    for inimigo in c.inimigos [:]:
        inimigo ['rect'].y += int (c.velocidade_inimigos )

        # Se ultrapassar o limite inferior da tela... --->
        if inimigo ['rect'].top > c.HEIGHT:
            c.inimigos.remove (inimigo )
            c.estado ["vida"]-= 1 # <--- decrementa vida
            if a.assets ["sfx_dano"]:
                a.assets ["sfx_dano"].play ()