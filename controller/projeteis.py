import modelo.configuracoes as c


def atualizar_projeteis(lista_tiros, velocidade_y, eh_laser_jogador=True):
    """
    O 'eh_laser_jogador' diferencia se caso os lasers são do herói (True, então o laser sobe)
    or dos inimigos (False, lasers descem), que possuem dados extras de direção e dano.
    """
    for t in lista_tiros[:]:
        # Para lasers do jogador, extrai a Rect diretamente. Para inimigos, extrai o 'rect' do dicionário aninhado
        rect_objeto = t if eh_laser_jogador else t["rect"]
        rect_objeto.y += velocidade_y

        # Verifica fronteira superior (jogador) ou inferior (inimigo)
        if (eh_laser_jogador and rect_objeto.bottom < 0) or (
            not eh_laser_jogador and rect_objeto.top > c.HEIGHT
        ):
            lista_tiros.remove(t)
