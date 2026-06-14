# O Despertar do Guardião

PBL da disciplina UCE 008 - Programação em Python | UEFS

## Sobre

Space shooter inspirado em Space Invaders e Star Wars, desenvolvido com Pygame-ce.
O jogador controla um guardião da Força encarregado de proteger o planeta aliado contra a frota do Império Galáctico.

## Requisitos do jogo
- [x] Movimentação em todas as direções e disparo de tiros energéticos
- [x] Coleta de bactas para recuperar vida
- [x] Inimigos descem gradualmente e atiram no jogador
- [x] Stormtrooper: 10 pontos por derrota; Darth Vader surge ao atingir 200 pontos
- [x] Darth Vader exige 5 acertos e causa 2 de dano; derrotá-lo vence o jogo
- [x] HUD com score, barra de vida e cronômetro
- [x] Menu principal (Start, Dificuldade, Sair) e menu de pausa
- [x] Três níveis de dificuldade (fácil, médio, difícil)

## Etapas
- [x] 01 - Configuração inicial e criação de telas
- [x] 02 - Atualização da tela e sprites
- [x] 03 - Movimentação e input do jogador
- [x] 04 - Sistema de colisão e interação entre elementos
- [x] 05 - Persistência de dados
- [x] 06 - Música e efeitos sonoros

## Barema

**Controle do Jogador**
- [x] Movimentação em todas as direções
- [x] Disparo de tiros energéticos
- [x] Coleta de elementos no campo de batalha (vida bônus)

**Sistema de Inimigos**
- [x] Inimigos descem gradualmente pelo ecrã
- [x] Inimigos disparam tiros que atingem o jogador
- [x] Aparecimento em ondas e pausa ao atingir 200 pts

**Sistema de Colisão**
- [x] Tiros do jogador registram acerto no inimigo
- [x] Tiros/colisão reduzem vida do jogador (-1 ou -2 para Vader)

**Darth Vader**
- [x] Darth Vader surge ao atingir determinada pontuação
- [x] Darth Vader requer 5 acertos para ser derrotado
- [x] Dano duplo ao jogador quando Darth Vader ataca

**Pontos de Vida**
- [x] Começa com 3 e vida bonus surge aleatoriamente ao derrotar inimigo

**Sistema de Pontuação**
- [x] Stormtrooper vale 10 pts (1 tiro)
- [x] Derrotar Darth Vader vale 200 pts e vence o jogo
- [x] Game Over quando vida chega a 0
- [x] Vitória ao derrotar Darth Vader

**HUD e Menus**
- [x] Exibe Score, Barra de Vida e Cronômetro (mm:ss) em tempo real
- [x] Menu Principal
- [x] Menu de Pausa

**Nível de Dificuldade**
- [ ] Implementação de dificuldade no jogo de acordo ao nivel
- [x] Velocidade dos inimigos aumenta conforme a dificuldade

**Qualidade do Código**
- [ ] Código bem modularizado em funções com responsabilidades claras
- [ ] Boas práticas: nomes significativos, sem repetição excessiva (DRY)
- [ ] Comentários e organização do código-fonte

## Metas de Atualização
- [x] Escopo do protótipo (MVP)
- [x] Protótipo funcional com Assets
- [ ] Jogo completo com critérios do barema
- [ ] 1. Adições bacanas extra barema:
- [ ] 1.1 Pontuação ao derrotar Vader varia com a dificuldade

## Tecnologias
- Eclipse IDE
- Python 3.11
- Pygame-ce 2.6
- Visual Studio Code

## Referências
- [Documentação do pygame](https://www.pygame.org/docs/)
- Guias providenciados pelo coordenador do curso
- [OpenGameArt.org](https://opengameart.org/)
- [Building Space Invaders Using PyGame - Python](https://www.geeksforgeeks.org/python/building-space-invaders-using-pygame-python/)
