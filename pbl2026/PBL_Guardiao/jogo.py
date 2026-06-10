"""Jogo.py: 
Este módulo contém a main e atua como núcleo que inicializa a janela de hardware do SDL,
sincroniza os atalhos locais de vídeo e dita a sequência linear de boot do jogo.
"""

import pygame
import sys

# Explicação: depois de alguns testes, percebi que inicializar o pygame
# antes de importar os demais packages impede erros de inicialização de recursos (como fontes e áudio), 
# isso será replicado também em outros módulos com lógica aplicada
pygame.init()

# Aplicação de alias para visualização limpa
import modelo.configuracoes as c
import modelo.assets as a
import modelo.ranking as rnk
import view.menus as m
import controller.logica as l

# Configurações Iniciais e Fixas
c.screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
pygame.display.set_caption("O Despertar do Guardião")

# Explicação: Inicialmente, declarar 'screen = c.screen' antes do display.set_mode() 
# gerava um NameError ou atribuía None, pois o display ainda não existia. Ao mover esta linha para cá, 
# resultou em um atalho seguro e local que aponta perfeitamente para a superficie ativa da janela.
screen = c.screen 

a.inicializar_assets()  # Entre outras funções, carrega as imagens já formatas em .convert_alpha()
a.tocar_musica_tema()

def menu_principal():
    """Gerencia a navegação inicial baseada no teclado e delega o disparo da partida para o Controller."""
    while True:
        # Bug corrigido: Caso o jogador voltasse da tela de vitória/derrota via ESC, a música 
        # de fundo permanecia desligada. 
        # O get_busy() checa o canal de áudio e reativa a trilha caso esteja em silêncio.
        # CORREÇÃO: Alterado de c.estado_tela para c.estado
        if not pygame.mixer.music.get_busy() and not c.estado["musica_pausada"]:
            a.tocar_musica_tema()

        c.screen.fill(m.PRETO) # Limpa o frame anterior preenchendo a janela com preto absoluto

        # CORREÇÃO: Alterado de c.estado_tela para c.estado nas chaves abaixo
        titulo = a.assets["fonte_titulo"].render("O DESPERTAR DO GUARDIÃO", True, m.AMARELO)
        start_txt = a.assets["fonte_titulo"].render("[ENTER] Iniciar", True, m.BRANCO)
        dificuldade_txt = a.assets["fonte_titulo"].render("[D] Dificuldade: " + c.estado["nivel_dificuldade_ativa"].capitalize(), True, m.BRANCO)
        ranking_txt = a.assets["fonte_titulo"].render("[H] Hall da Fama", True, m.BRANCO)
        sair_txt = a.assets["fonte_titulo"].render("[ESC] Sair", True, m.BRANCO)
        
        # Blitagem do Menu principal
        # Fórmula aplicada: (Largura_Total_Janela // 2) - (Largura_Superfície_Texto // 2) para alinhamento central.
        c.screen.blit(titulo, (c.WIDTH // 2 - titulo.get_width() // 2, c.HEIGHT // 4)) # posiciona no primeiro quadrante
        c.screen.blit(start_txt, (c.WIDTH // 2 - start_txt.get_width() // 2, c.HEIGHT // 2 - 40)) # início do grid vertical
        
        c.screen.blit(dificuldade_txt, (c.WIDTH // 2 - dificuldade_txt.get_width() // 2, c.HEIGHT // 2 + 10)) # Salto de 50px

        c.screen.blit(ranking_txt, (c.WIDTH // 2 - ranking_txt.get_width() // 2, c.HEIGHT // 2 + 60))        # Salto de 50px
        c.screen.blit(sair_txt, (c.WIDTH // 2 - sair_txt.get_width() // 2, c.HEIGHT // 2 + 110))
                         
        # botao de alternar msucia
        m.desenhar_botao_pausar_msc()
        
        pygame.display.flip() # Inverte o buffer de desenho oculto projetando a tela final montada para o monitor
        
        # Aplicado tratamento de inputs no Menu Principal:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: # Captura o clique no 'X' para fechar janela
                pygame.quit()         # Desliga com segurança a SDL
                sys.exit()            # Finaliza a execução do processo Python no terminal do sistema
            
            # Botão de pausar musica na tela narrativa
            if e.type == pygame.KEYDOWN: # Avalia se o usuário pressionou qualquer tecla
                if e.key == pygame.K_m: # captura tecla M para pausar
                    c.alternar_pausar_musica()
                        
                elif e.key == pygame.K_RETURN:
                    l.iniciar_jogo() # Zera arrays, zera score e calibra escudos com base na dificuldade (Model)
                    l.main_loop()    # Transfere o controle da Call Stack para o loop de 60 FPS (Controller)
              
                # D: Alternador circular do nível de dificuldade (Garante eficiência e baixo uso de RAM)
                # CORREÇÃO: Alterado de c.estado_tela para c.estado
                elif e.key == pygame.K_d:
                    if c.estado["nivel_dificuldade_ativa"] == 'facil': 
                        c.estado["nivel_dificuldade_ativa"] = 'medio'
                    elif c.estado["nivel_dificuldade_ativa"] == 'medio': 
                        c.estado["nivel_dificuldade_ativa"] = 'dificil'
                    else: 
                        c.estado["nivel_dificuldade_ativa"] = 'facil'
                        
                # H: Pausa temporariamente o menu e invoca a sub-rotina de exibição do ranking deserializado
                elif e.key == pygame.K_h:
                    rnk.exibir_ranking() # Carrega os dados do hall_da_fama.json e desenha em tela
                    
                # ESC: Força a interrupção imediata de hardware e encerramento do programa
                elif e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    while True:
        # Aplicado Ciclo Linear de Telas (State Pattern):
        m.tela_narrativa()    
        
        # 2. Após desempilhar a narrativa com o ENTER, abre o menu interativo.
        menu_principal()