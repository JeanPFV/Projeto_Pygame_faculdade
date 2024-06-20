import random
import threading
import time
import pygame
import sys
import keyboard

# Importa as perguntas de múltipla escolha, respostas e dicas
import perguntas_bio
import perguntas_computador


# Definir limite de resposta para cada pergunta
tempo_de_resposta = 10


def mensagem_inicial():

    resp = input("Deseja começar o jogo? (S/N)\n")
    if resp.lower() == "s":
        print("Começando o jogo...")
        for tempo in range(3, 0, -1):
            time.sleep(1)
            print(tempo)
        print("Vamos lá!")


def input_with_timeout(prompt, timeout):
    print(prompt)
    user_input = [""]  # Lista para armazenar a entrada do palpite do usuário

    # Função para receber a entrada do usuário
    def get_input():
        user_input[0] = input("\nResposta: ")

    # Criando uma thread para receber a entrada do usuário
    input_thread = threading.Thread(target=get_input)
    input_thread.start()

    # Aguardando o tempo limite ou até que o usuário forneça uma resposta
    input_thread.join(timeout)

    # Retorna uma String vazia se o usuário não digitar nada e usa o keyboard para apertar
    # enter e interroper o Threading
    # Ou retorna o Input do usuário
    if user_input[0] == "":
        keyboard.press("enter")
        return ""
    else:
        return user_input[0]


# Modo normal, com tempo e sistema de pontuação
def modo_normal(perguntas):

    print("Bem-vindo ao modo normal de Jogo")
    mensagem_inicial()

    # Embaralhador de perguntas
    perguntas = list(perguntas.items())
    random.shuffle(perguntas)

    # Marca a pontuação inicial
    pontuacao = 0

    # Iteração para cada pergunta
    for pergunta, resposta in perguntas:
        print(pergunta + "\nSe precisar de uma dica digite: dica")  # Print da Pergunta
        start_time = time.time()  # Marca o início do tempo para esta pergunta
        # While que vai fazer as verificações de input e verificar se o usuário pediu dica
        while True:
            # Resposta do usuário fica na variável palpite
            palpite = input_with_timeout(
                f"Você tem {tempo_de_resposta} segundos para responder ",
                tempo_de_resposta,
            )
            if palpite == "dica":
                # Verificação se o tempo acabou quando foi pedido a dica
                time_left = tempo_de_resposta - (time.time() - start_time)
                if time_left <= 0:
                    print("Tempo esgotado!")
                    break
                print(f"{resposta['dica']}\n")  # Print da dica
                pontuacao -= (
                    1  # Diminuição da pontuação do usuário caso ele peça a dica
                )
                continue
            # Tratamento de input de usuário
            elif palpite in ["a", "b", "c", "d"]:
                # Verificação se o tempo acabou quando foi dado a resposta
                time_left = tempo_de_resposta - (time.time() - start_time)
                if time_left <= 0:
                    print("Tempo esgotado!")
                    break
                # Se a resposta for correta
                if palpite == resposta["resposta"].lower():
                    print("\nCorreto!\n")
                    pontuacao += 2  # Adiciona dois ponto a pontução
                    break
                # Se a resposta for incorreta
                else:
                    print(
                        f"\nIncorreto. A resposta correta é: {resposta['resposta']}.\n"
                    )
                    break
            # Se não tiver um input do usuário
            elif palpite == "":
                print("Tempo Esgotado!")
                break
            # Tratemento de input do usuário
            else:
                if palpite.lower() in ["a", "b", "c", "d"]:
                    break
                else:
                    print("\nResposta inválida. Tente novamente.\n")

    # Print da pontuação final do usuário
    print(f"\nFim do jogo! Sua pontuação final é: {pontuacao}\n")


# Modo Estudo é idêntico ao modo normal, mas não tem a sistema de pontos e temporizador
def modo_estudo(perguntas):

    print("Bem-vindo ao modo de estudo de Jogo")
    mensagem_inicial()

    # Embaralhador de perguntas
    perguntas = list(perguntas.items())
    random.shuffle(perguntas)

    # Iteração para cada pergunta
    for pergunta, resposta in perguntas:

        print(pergunta)
        # While que faz a verificação de input
        while True:
            # Resposta do Usuário
            palpite = input("Resposta: ")
            # Se a resposta do usuário for válida
            if palpite in ["a", "b", "c", "d"]:
                # Se a resposta estiver correta
                if (
                    palpite != ""
                    and palpite.strip().lower() == resposta["resposta"].lower()
                ):
                    print("Correto!\n")
                    break
                # Se a resposta estiver errada
                else:
                    print(f"Incorreto. A resposta correta é: {resposta['resposta']}.\n")
                    break
            # Verificação de input
            else:
                if palpite.lower() in ["a", "b", "c", "d"]:
                    break
                else:
                    print("\nResposta inválida. Tente novamente.\n")

    print("Fim do jogo!")


# Modo multiplayer é igual ao modo normal em mecânica,
# mas poder ser jogado por um número de jogadores que o usuário pode selecionar
def modo_multiplayer(perguntas):

    print("Bem-vindo ao modo multiplayer de Jogo")

    mensagem_inicial()

    # Embaralhador de perguntas
    perguntas = list(perguntas.items())
    random.shuffle(perguntas)

    # Define um número de players
    numero_jogadores = int(input("Quantidade de jogadores: >>> "))

    # Cria uma lista para armazenar os pontos dos jogadores
    pontos_jogadores = [0] * numero_jogadores

    # Iteração baseada no número de jogadores
    for i in range(numero_jogadores):
        print(f"Jogador {i+1}\n")

        # Iteração de perguntas
        for pergunta, resposta in perguntas:
            print(pergunta + "\nSe precisar de uma dica digite: dica")
            start_time = time.time()  # Marca o início do tempo para esta pergunta
            # While que faz a pergunta continuar válida depois da dica e que faz o tratamento de input
            while True:
                # Resposta do usuário
                palpite = input_with_timeout(
                    f"Você tem {tempo_de_resposta} segundos para responder: ",
                    tempo_de_resposta,
                )

                # Se o jogador pedir uma dica
                if palpite == "dica":
                    print(f"{resposta['dica']}\n")
                    pontos_jogadores[
                        i
                    ] -= 1  # Diminui um ponto do jogador que pediu a dica
                    # Verifica se o tempo acabou durante a dica
                    time_left = tempo_de_resposta - (time.time() - start_time)
                    if time_left <= 0:
                        print("Tempo esgotado!")
                        break
                    continue
                # Se a resposta for válida
                elif palpite in ["a", "b", "c", "d"]:
                    # Verifica se o tempo acabou quando foi dado a resposta
                    time_left = tempo_de_resposta - (time.time() - start_time)
                    if time_left <= 0:
                        print("Tempo esgotado!")
                        break
                    # Se a resposta for correta
                    if palpite == resposta["resposta"].lower():
                        print("\nCorreto!\n")
                        pontos_jogadores[
                            i
                        ] += 2  # Adiciona dois pontos na pontuação do jogador
                        break
                    # Se a resposta for errada
                    else:
                        print(
                            f"\nIncorreto. A resposta correta é: {resposta['resposta']}.\n"
                        )
                        break
                # Se o usuário não responder
                elif palpite == "":
                    print("Tempo Esgotado!")
                    break
                # Verificação de input
                else:
                    if palpite.lower() in ["a", "b", "c", "d"]:
                        break
                    else:
                        print("\nResposta inválida. Tente novamente.\n")

    # Pega a posição do jogador que fez mais pontos e faz um print especial
    pontos_ganhador = max(pontos_jogadores)
    jogador_ganhador = pontos_jogadores.index(pontos_ganhador)
    print(f"O Jogador {jogador_ganhador+1} ganhou com {pontos_ganhador} pontos!")

    # Mostra a pontuação de todos jogadores
    for i in range(numero_jogadores):
        print(f"Jogardor {i+1}: {pontos_jogadores[i]}")


# O modo adaptativo se adapta conforme o usuário responde as perguntas,
# fica mais fácil se errar, e mais difícil se acertar
def modo_adptativo(matriz, tema, dificuldade):

    print("Bem-vindo ao modo adaptativo de Jogo")
    mensagem_inicial()

    # Pontuação inicial
    pontuacao = 0
    # Contador para ter um número limite de perguntas
    cont = 0
    while cont != 9:

        # as perguntas aleatorias sao criadas dentro do laço para serem mudadas
        # conforme o usuário responde
        perguntas = matriz[dificuldade][tema]
        perguntas = list(perguntas.items())
        random.shuffle(perguntas)

        # Iteração de perguntas
        for pergunta, resposta in perguntas:
            print(pergunta + "\nSe precisar de uma dica digite: dica")
            start_time = time.time()  # Marca o início do tempo para esta pergunta

            # While que cuida da pergunta estar disponível até depois de uma dica e
            # faz o tratamento de input
            while True:
                # Resposta do usuário
                palpite = input_with_timeout(
                    f"Você tem {tempo_de_resposta} segundos para responder ",
                    tempo_de_resposta,
                )

                if palpite == "dica":
                    # Verifica se o tempo acabou quando pedido a dica
                    time_left = tempo_de_resposta - (time.time() - start_time)
                    if time_left <= 0:
                        print("Tempo esgotado!")
                        break
                    print(f"{resposta['dica']}\n")
                    pontuacao -= 1
                    continue

                # Verificação de input
                elif palpite in ["a", "b", "c", "d"]:
                    # Verifica se o tempo acabou quando foi dado a resposta
                    time_left = tempo_de_resposta - (time.time() - start_time)
                    if time_left <= 0:
                        print("Tempo esgotado!")
                        break

                    # Se a resposta estiver correta
                    if palpite == resposta["resposta"].lower():
                        print("\nCorreto!\n")
                        pontuacao += 2  # Aumenta em dois a pontuação
                        dificuldade += 1  # Aumenta a dificuldade (De fácil para médio e médio para difícil)
                        # Verificação para a dificuldade ficar no máximo disponível
                        if dificuldade > 2:
                            dificuldade = 2
                        break

                    # Se a resposta estiver errada
                    else:
                        print(
                            f"\nIncorreto. A resposta correta é: {resposta['resposta']}.\n"
                        )
                        dificuldade -= 1  # Diminui a dificuldade em (De difícil para médio e de médio para fácil)
                        if dificuldade < 0:
                            dificuldade = 0
                        break

                # Se o tempo acabar
                elif palpite == "":
                    print("Tempo Esgotado!")
                    dificuldade -= 1  # Diminui a dificuldade em (De difícil para médio e de médio para fácil)
                    # Verificação para a dificuldade ficar no mínimo disponível
                    if dificuldade < 0:
                        dificuldade = 0
                    break

                # Verificação de input
                else:
                    if palpite.lower() in ["a", "b", "c", "d"]:
                        break
                    else:
                        print("\nResposta inválida. Tente novamente.\n")

            # Atualizar a dificuldade somente após o usuário responder à pergunta
            # Limpando a lista de pergunta e criando uma nova com base na dificuldade nova
            perguntas.clear()
            perguntas = matriz[dificuldade][tema]
            perguntas = list(perguntas.items())
            random.shuffle(perguntas)

        # Contador para ter um limite de perguntas
        cont += 1

    # Print para mostrar a pontuação final
    print(f"\nFim do jogo! Sua pontuação final é: {pontuacao}")


# Menu inicial
def menu():
    print("Bem-vindo ao jogo de Perguntas e Respostas!\n")

    # Matriz para selecionar tema e dificuldade
    # Sendo os temas 0 = Biologia e 1 = Computação
    # As dificuldade 0 = Fácil, 1 = Normal e 2 = Difícil
    matriz = [
        [perguntas_bio.bio_facil, perguntas_computador.compu_facil],
        [perguntas_bio.bio_normal, perguntas_computador.compu_normal],
        [perguntas_bio.bio_dificil, perguntas_computador.compu_dificil],
    ]

    # Menu para o usuário escolher o tema e a dificuldade de acordo com o número
    # fazendo uma verificação no processo
    # É colocado o -1 no final para a interface ser mais user friendly
    while True:
        tema = int(input("Escolha o tema:\n 1. Biologia\n 2. Computadores\n>>> ")) - 1
        if 0 <= tema <= 1:
            break
        else:
            print("Valor inválido. Tente novamente.")

    while True:
        dificuldade = (
            int(
                input(
                    "Escolha a dificuldade:\n 1. Fácil\n 2. Normal\n 3. Difícil\n>>> "
                )
            )
            - 1
        )
        if 0 <= dificuldade <= 2:
            break
        else:
            print("Valor inválido. Tente novamente.")

    # Pega o dicionário baseado nos inputs do usuário para ser usado nos modos
    perguntas = matriz[dificuldade][tema]

    # Apresenta os modos de jogo para que o usuário escolher de acordo com o número, e descreve como funciona o jogo e a pontuação
    print(
        "Você terá 20 segundos para responder as 5 perguntas, cada pergunta vale 2 pontos, você pode pedir dicas, mas perderá 1 ponto a cada dica usada.\n"
    )
    print("Selecione o modo de jogo:\n")
    print("1. Modo Normal (Jogo normal)\n")
    print("2. Modo Estudo (Revise as perguntas e respostas)\n")
    print("3. Modo Multiplayer (O jogador com a maior pontuação vence)\n")
    print("4. Adaptativo (A dificuldade se ajusta ao jogador)\n")
    print("0. Sair\n")

    # Usuário escolhe o modo de jogo de acordo com o número
    opcao = input("Digite o número da opção desejada >>>")

    # match case para cada modo de jogo
    match opcao:
        case "0":
            print("Saindo do jogo...")
        case "1":
            modo_normal(perguntas)
        case "2":
            modo_estudo(perguntas)
        case "3":
            modo_multiplayer(perguntas)
        case "4":
            modo_adptativo(matriz, tema, dificuldade)
        case _:
            print("Opção inválida. Tente novamente. \n")
            menu()

    return matriz, perguntas


# Torna o menu o processo main
def main():
    menu()


if __name__ == "__main__":
    main()
