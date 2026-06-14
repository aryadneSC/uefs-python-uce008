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
- [ ] Movimentação em todas as direções 0,5
- [ ] Disparo de tiros energéticos 0,5
- [ ] Coleta de elementos no campo de batalha (vida bônus) 0,5

**Sistema de Inimigos**
- [ ] Inimigos descem gradualmente pelo ecrã 0,5
- [ ] Inimigos disparam tiros que atingem o jogador 0,5
- [ ] Aparecimento em ondas e pausa ao atingir 200 pts 0,5

**Sistema de Colisão**
- [ ] Tiros do jogador registram acerto no inimigo 0,5
- [ ] Tiros/colisão reduzem vida do jogador (-1 ou -2 para Vader) 0,5

**Darth Vader**
- [ ] Darth Vader surge ao atingir determinada pontuação 0,25
- [ ] Darth Vader requer 5 acertos para ser derrotado 0,25
- [ ] Dano duplo ao jogador quando Darth Vader ataca 0,25

**Pontos de Vida**
- [ ] Começa com 3 e vida bonus surge aleatoriamente ao derrotar inimigo 0,5

**Sistema de Pontuação**
- [ ] Stormtrooper vale 10 pts (1 tiro) 0,25
- [ ] Derrotar Darth Vader vale 200 pts e vence o jogo 0,25
- [ ] Game Over quando vida chega a 0 0,25
- [ ] Vitória ao derrotar Darth Vader 0,25

**HUD e Menus**
- [ ] Exibe Score, Barra de Vida e Cronômetro (mm:ss) em tempo real 0,25
- [ ] Menu Principal 0,25
- Menu de Pausa 0,25

**Nível de Dificuldade**
- [ ] Implementação de dificuldade no jogo de acordo ao nivel 0,5
- [ ] Velocidade dos inimigos aumenta conforme a dificuldade 0,5

**Qualidade do Código**
- [ ] Código bem modularizado em funções com responsabilidades claras 1
- [ ] Boas práticas: nomes significativos, sem repetição excessiva (DRY) 0,5
- [ ] Comentários e organização do código-fonte

## Metas de Atualização
- [x] Escopo do protótipo (MVP)
- [x] Protótipo funcional com Assets
- [ ] Adições bacanas extra barema

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
