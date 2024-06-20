import pygame
import random
import time
import threading
import perguntas_bio
import perguntas_computador

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

tempo_de_resposta = 10

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Perguntas e Respostas")

font = pygame.font.Font(None, 36)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def input_with_timeout(prompt, timeout):
    clock = pygame.time.Clock()
    user_input = ""
    start_time = time.time()

    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

        screen.fill(WHITE)
        draw_text(prompt, font, BLACK, screen, 20, 20)
        draw_text(user_input, font, BLACK, screen, 20, 60)

        pygame.display.flip()
        clock.tick(FPS)

        if time.time() - start_time > timeout:
            input_active = False

    return user_input

def mensagem_inicial():
    clock = pygame.time.Clock()
    start_time = time.time()
    message = "Deseja começar o jogo? (Y/N)"
    user_input = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    return False

        screen.fill(WHITE)
        draw_text(message, font, BLACK, screen, 20, 20)
        pygame.display.flip()
        clock.tick(FPS)

def modo_normal(perguntas):
    if not mensagem_inicial():
        return

    perguntas = list(perguntas.items())
    random.shuffle(perguntas)
    pontuacao = 0

    for pergunta, resposta in perguntas:
        user_input = input_with_timeout(f"{pergunta}\nVocê tem {tempo_de_resposta} segundos para responder", tempo_de_resposta)
        if user_input == "dica":
            draw_text(f"Dica: {resposta['dica']}", font, BLACK, screen, 20, 100)
            pygame.display.flip()
            time.sleep(2)
            pontuacao -= 1
        elif user_input.lower() == resposta['resposta'].lower():
            draw_text("Correto!", font, BLACK, screen, 20, 100)
            pygame.display.flip()
            time.sleep(2)
            pontuacao += 2
        else:
            draw_text(f"Incorreto. A resposta correta é: {resposta['resposta']}", font, BLACK, screen, 20, 100)
            pygame.display.flip()
            time.sleep(2)

    draw_text(f"Fim do jogo! Sua pontuação final é: {pontuacao}", font, BLACK, screen, 20, 100)
    pygame.display.flip()
    time.sleep(3)

def modo_estudo(perguntas):
    if not mensagem_inicial():
        return

    perguntas = list(perguntas.items())
    random.shuffle(perguntas)

    for pergunta, resposta in perguntas:
        user_input = input_with_timeout(f"{pergunta}\nResposta: ", 0)
        if user_input.lower() == resposta['resposta'].lower():
            draw_text("Correto!", font, BLACK, screen, 20, 100)
        else:
            draw_text(f"Incorreto. A resposta correta é: {resposta['resposta']}", font, BLACK, screen, 20, 100)
        pygame.display.flip()
        time.sleep(2)

    draw_text("Fim do jogo!", font, BLACK, screen, 20, 100)
    pygame.display.flip()
    time.sleep(3)

def modo_multiplayer(perguntas):
    if not mensagem_inicial():
        return

    perguntas = list(perguntas.items())
    random.shuffle(perguntas)

    numero_jogadores = int(input_with_timeout("Quantidade de jogadores: ", 0))
    pontos_jogadores = [0] * numero_jogadores

    for i in range(numero_jogadores):
        draw_text(f"Jogador {i+1}", font, BLACK, screen, 20, 20)
        pygame.display.flip()
        time.sleep(2)

        for pergunta, resposta in perguntas:
            user_input = input_with_timeout(f"{pergunta}\nVocê tem {tempo_de_resposta} segundos para responder", tempo_de_resposta)
            if user_input == "dica":
                draw_text(f"Dica: {resposta['dica']}", font, BLACK, screen, 20, 100)
                pygame.display.flip()
                time.sleep(2)
                pontos_jogadores[i] -= 1
            elif user_input.lower() == resposta['resposta'].lower():
                draw_text("Correto!", font, BLACK, screen, 20, 100)
                pygame.display.flip()
                time.sleep(2)
                pontos_jogadores[i] += 2
            else:
                draw_text(f"Incorreto. A resposta correta é: {resposta['resposta']}", font, BLACK, screen, 20, 100)
                pygame.display.flip()
                time.sleep(2)

    pontos_ganhador = max(pontos_jogadores)
    jogador_ganhador = pontos_jogadores.index(pontos_ganhador)
    draw_text(f"O Jogador {jogador_ganhador+1} ganhou com {pontos_ganhador} pontos!", font, BLACK, screen, 20, 100)
    pygame.display.flip()
    time.sleep(3)

    for i in range(numero_jogadores):
        draw_text(f"Jogador {i+1}: {pontos_jogadores[i]}", font, BLACK, screen, 20, 100 + (i*40))
        pygame.display.flip()
        time.sleep(1)

def modo_adptativo(matriz, tema, dificuldade):
    if not mensagem_inicial():
        return

    pontuacao = 0
    cont = 0
    while cont != 9:
        perguntas = matriz[dificuldade][tema]
        perguntas = list(perguntas.items())
        random.shuffle(perguntas)

        for pergunta, resposta in perguntas:
            user_input = input_with_timeout(f"{pergunta}\nVocê tem {tempo_de_resposta} segundos para responder", tempo_de_resposta)
            if user_input == "dica":
                draw_text(f"Dica: {resposta['dica']}", font, BLACK, screen, 20, 100)
                pygame.display.flip()
                time.sleep(2)
                pontuacao -= 1
            elif user_input.lower() == resposta['resposta'].lower():
                draw_text("Correto!", font, BLACK, screen, 20, 100)
                pygame.display.flip()
                time.sleep(2)
                pontuacao += 2
                dificuldade = min(dificuldade + 1, 2)
            else:
                draw_text(f"Incorreto. A resposta correta é: {resposta['resposta']}", font, BLACK, screen, 20, 100)
                pygame.display.flip()
                time.sleep(2)
                dificuldade = max(dificuldade - 1, 0)

        cont += 1

    draw_text(f"Fim do jogo! Sua pontuação final é: {pontuacao}", font, BLACK, screen, 20, 100)
    pygame.display.flip()
    time.sleep(3)

def iniciar_modo(modo, tema_var, dificuldade_var):
    if tema_var == "Biologia":
        tema = 0
    elif tema_var == "Computadores":
        tema = 1
    else:
        draw_text("Tema inválido", font, BLACK, screen, 20, 100)
        pygame.display.flip()
        time.sleep(2)
        return

    if dificuldade_var == "Fácil":
        dificuldade = 0
    elif dificuldade_var == "Normal":
        dificuldade = 1
    elif dificuldade_var == "Difícil":
        dificuldade = 2
    else:
        draw_text("Dificuldade inválida", font, BLACK, screen, 20, 100)
        pygame.display.flip()
        time.sleep(2)
        return

    matriz = [
        [perguntas_bio.bio_facil, perguntas_computador.compu_facil],
        [perguntas_bio.bio_normal, perguntas_computador.compu_normal],
        [perguntas_bio.bio_dificil, perguntas_computador.compu_dificil]
    ]

    perguntas = matriz[dificuldade][tema]
    if modo == "normal":
        modo_normal(perguntas)
    elif modo == "estudo":
        modo_estudo(perguntas)
    elif modo == "multiplayer":
        modo_multiplayer(perguntas)
    elif modo == "adaptativo":
        modo_adptativo(matriz, tema, dificuldade)
    else:
        draw_text("Modo de jogo inválido", font, BLACK, screen, 20, 100)
        pygame.display.flip()
        time.sleep(2)

def menu():
    clock = pygame.time.Clock()
    running = True

    tema_var = "Biologia"
    dificuldade_var = "Fácil"

    while running:
        screen.fill(WHITE)
        draw_text("Bem-vindo ao jogo de Perguntas e Respostas!", font, BLACK, screen, 20, 20)

        draw_text("Escolha o tema:", font, BLACK, screen, 20, 60)
        draw_text(f"Tema atual: {tema_var}", font, BLACK, screen, 20, 100)

        draw_text("Escolha a dificuldade:", font, BLACK, screen, 20, 140)
        draw_text(f"Dificuldade atual: {dificuldade_var}", font, BLACK, screen, 20, 180)

        draw_text("Pressione N para Modo Normal", font, BLACK, screen, 20, 220)
        draw_text("Pressione E para Modo Estudo", font, BLACK, screen, 20, 260)
        draw_text("Pressione M para Modo Multiplayer", font, BLACK, screen, 20, 300)
        draw_text("Pressione A para Modo Adaptativo", font, BLACK, screen, 20, 340)
        draw_text("Pressione T para Trocar Tema", font, BLACK, screen, 20, 380)
        draw_text("Pressione D para Trocar Dificuldade", font, BLACK, screen, 20, 420)
        draw_text("Pressione Q para Sair", font, BLACK, screen, 20, 460)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    iniciar_modo("normal", tema_var, dificuldade_var)
                elif event.key == pygame.K_e:
                    iniciar_modo("estudo", tema_var, dificuldade_var)
                elif event.key == pygame.K_m:
                    iniciar_modo("multiplayer", tema_var, dificuldade_var)
                elif event.key == pygame.K_a:
                    iniciar_modo("adaptativo", tema_var, dificuldade_var)
                elif event.key == pygame.K_t:
                    if tema_var == "Biologia":
                        tema_var = "Computadores"
                    else:
                        tema_var = "Biologia"
                elif event.key == pygame.K_d:
                    if dificuldade_var == "Fácil":
                        dificuldade_var = "Normal"
                    elif dificuldade_var == "Normal":
                        dificuldade_var = "Difícil"
                    else:
                        dificuldade_var = "Fácil"
                elif event.key == pygame.K_q:
                    running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    menu()
