"""Espaço isolado para organizar interfaces e separar textos na tela"""

import pygame
import sys

import modelo.assets as a
import modelo.configuracoes as c

AMARELO = (255, 255, 0)
AZUL = (0, 0, 255)
BRANCO = (255, 255, 255)
CIANO = (255, 0, 255)
CINZA = (150, 150, 150)
PRETO = (0, 0, 0)
VERDE_MUSGO = (2, 85, 100)
VERMELHO_PASTEL = (255, 100, 100)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
TURQUESA = (64, 204, 208)

def tela_narrativa():
    """
    Exibe a introdução do universo de Star Wars contextualizando a missão do Guardião.
    Correção de erro: Antigamente, essa tela ficava dentro da jogo.py gerando NameError
    porque as fontes ainda não tinham sido inicializadas no motor gráfico. Agora ela roda em escopo isolado.
    """
    while True:
        c.screen.fill(PRETO)
        desenhar_botao_pausar_msc()
        titulo_narrativa = a.assets["fonte_titulo"].render("O IMPÉRIO GALÁCTICO CONTRA-ATACA", True, AMARELO)
        c.screen.blit(titulo_narrativa, (c.WIDTH // 2 - titulo_narrativa.get_width() // 2, 70))
        
        texto = [
            "A terrível Frota Imperial avança",
            "contra a base secreta",
            "do Planeta Aliado Kashyyyk!",
            "Nossas forças estão quase no fim",
            "",
            "Guardião, você é nossa única esperança", 
            "de expulsar as tropas inimigas.",
            "Que a Força esteja com você...", "",
        ]
        instrucao = a.assets["fonte_titulo"].render("Pressione ENTER para iniciar", True, VERDE_MUSGO)
        c.screen.blit(instrucao, (c.WIDTH // 2 - instrucao.get_width() // 2, c.HEIGHT - 70))
        
        # Loop de blitagem das linhas com incremento vertical de 40 pixels (Criação do bloco de texto formatado)
        for i, linha in enumerate(texto):
            txt = a.assets["fonte_titulo"].render(linha, True, BRANCO)
            c.screen.blit(txt, (c.WIDTH // 2 - txt.get_width() // 2, c.HEIGHT // 4 + i * 40))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_m:
                    c.alternar_pausar_musica()
                elif e.key == pygame.K_RETURN: 
                    return

def mostrar_menu_pausa():
    # IMPORTANTE: Essa função NÃO possui um loop 'while' interno próprio. 
    # Ela é apenas um renderizador estático. O loop de travamento é controlado pela logica.py em Controller.
    c.screen.fill(PRETO)
    titulo = a.assets["fonte_titulo"].render("JOGO PAUSADO", True, AMARELO)
    continuar_txt = a.assets["fonte_hud"].render("Pressione P para Continuar", True, BRANCO)
    sair_txt = a.assets["fonte_hud"].render("Pressione ESC para Sair", True, VERMELHO_PASTEL)
    
    # Blita e centraliza matematicamente as instruções na tela ativa do monitor
    c.screen.blit(titulo, (c.WIDTH // 2 - titulo.get_width() // 2, c.HEIGHT // 3))
    c.screen.blit(continuar_txt, (c.WIDTH // 2 - continuar_txt.get_width() // 2, c.HEIGHT // 2))
    c.screen.blit(sair_txt, (c.WIDTH // 2 - sair_txt.get_width() // 2, c.HEIGHT // 2 + 50))
    pygame.display.flip() 
    
def desenhar_botao_pausar_msc():
    img_msc = getattr(a, "img_icone_msc", None)
    if img_msc:
        indice_imagem = 1 if c.estado["musica_pausada"] else 0
        c.screen.blit(img_msc[indice_imagem], c.msc_botao)
    else:
        cor_botao = VERMELHO_PASTEL if c.estado["musica_pausada"] else AMARELO
        pygame.draw.rect(c.screen, cor_botao, c.msc_botao)

    txt_msc = a.assets["fonte_hud"].render("(M)", True, BRANCO)
    c.screen.blit(txt_msc, (c.msc_botao.x + (c.msc_botao.width // 2) - (txt_msc.get_width() // 2), c.msc_botao.y + 35))