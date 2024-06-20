import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import threading
import time
import queue
import perguntas_bio
import perguntas_computador

tempo_de_resposta = 10

def input_with_timeout(prompt, timeout, root):
    def get_input(entry, user_input_queue):
        user_input_queue.put(entry.get())
        frame.pack_forget()

    user_input_queue = queue.Queue()

    frame = tk.Frame(root)
    frame.pack(pady=10)

    tk.Label(frame, text=prompt).pack(side="top", fill="x", pady=10)
    entry = tk.Entry(frame)
    entry.pack(side="top", fill="x", pady=10)
    entry.bind("<Return>", lambda event: get_input(entry, user_input_queue))

    def on_timeout():
        if user_input_queue.empty():
            user_input_queue.put("")

    root.after(timeout * 1000, on_timeout)

    def check_input():
        if not user_input_queue.empty():
            root.quit()
        else:
            root.after(100, check_input)

    root.after(100, check_input)
    root.mainloop()

    if not user_input_queue.empty():
        return user_input_queue.get()
    else:
        return ""

def mensagem_inicial(root):
    resposta = messagebox.askyesno("Iniciar Jogo", "Deseja começar o jogo?", parent=root)
    if resposta:
        messagebox.showinfo("Começando", "Começando", parent=root)
        for tempo in range(3, 0, -1):
            time.sleep(0.5)
        return True  
    return False

def modo_normal(perguntas, root):
    messagebox.showinfo("Modo Normal", "Bem-vindo ao modo normal de Jogo", parent=root)
    if not mensagem_inicial(root):
        return

    perguntas = list(perguntas.items())
    random.shuffle(perguntas)
    pontuacao = 0

    for pergunta, resposta in perguntas:
        pergunta_label = tk.Label(root, text=pergunta)
        pergunta_label.pack()

        palpite = input_with_timeout(f"Você tem {tempo_de_resposta} segundos para responder", tempo_de_resposta, root)
        if palpite == "dica":
            messagebox.showinfo("Dica", resposta['dica'], parent=root)
            pontuacao -= 1
        elif palpite.lower() == resposta['resposta'].lower():
            messagebox.showinfo("Correto", "Correto!", parent=root)
            pontuacao += 2
        else:
            messagebox.showinfo("Incorreto", f"Incorreto. A resposta correta é: {resposta['resposta']}", parent=root)
        
        pergunta_label.pack_forget()

    messagebox.showinfo("Fim do jogo", f"Fim do jogo! Sua pontuação final é: {pontuacao}", parent=root)

def modo_estudo(perguntas, root):
    messagebox.showinfo("Modo Estudo", "Bem-vindo ao modo de estudo de Jogo", parent=root)
    if not mensagem_inicial(root):
        return

    perguntas = list(perguntas.items())
    random.shuffle(perguntas)

    for pergunta, resposta in perguntas:
        palpite = input_with_timeout(pergunta, 0, root)
        if palpite.lower() == resposta['resposta'].lower():
            messagebox.showinfo("Correto", "Correto!", parent=root)
        else:
            messagebox.showinfo("Incorreto", f"Incorreto. A resposta correta é: {resposta['resposta']}", parent=root)

    messagebox.showinfo("Fim do jogo", "Fim do jogo!", parent=root)

def modo_multiplayer(perguntas, root):
    messagebox.showinfo("Modo Multiplayer", "Bem-vindo ao modo multiplayer de Jogo", parent=root)
    if not mensagem_inicial(root):
        return

    perguntas = list(perguntas.items())
    random.shuffle(perguntas)

    numero_jogadores = int(simpledialog.askstring("Número de Jogadores", "Quantidade de jogadores:", parent=root))
    pontos_jogadores = [0] * numero_jogadores

    for i in range(numero_jogadores):
        messagebox.showinfo(f"Jogador {i+1}", f"Jogador {i+1}", parent=root)

        for pergunta, resposta in perguntas:
            palpite = input_with_timeout(pergunta, tempo_de_resposta, root)
            if palpite == "dica":
                messagebox.showinfo("Dica", resposta['dica'], parent=root)
                pontos_jogadores[i] -= 1
            elif palpite.lower() == resposta['resposta'].lower():
                messagebox.showinfo("Correto", "Correto!", parent=root)
                pontos_jogadores[i] += 2
            else:
                messagebox.showinfo("Incorreto", f"Incorreto. A resposta correta é: {resposta['resposta']}", parent=root)

    pontos_ganhador = max(pontos_jogadores)
    jogador_ganhador = pontos_jogadores.index(pontos_ganhador)
    messagebox.showinfo("Resultado", f"O Jogador {jogador_ganhador+1} ganhou com {pontos_ganhador} pontos!", parent=root)

    for i in range(numero_jogadores):
        messagebox.showinfo(f"Jogador {i+1}", f"Jogador {i+1}: {pontos_jogadores[i]}", parent=root)

def modo_adptativo(matriz, tema, dificuldade, root):
    messagebox.showinfo("Modo Adaptativo", "Bem-vindo ao modo adaptativo de Jogo", parent=root)
    if not mensagem_inicial(root):
        return

    pontuacao = 0
    cont = 0
    while cont != 9:
        perguntas = matriz[dificuldade][tema]
        perguntas = list(perguntas.items())
        random.shuffle(perguntas)

        for pergunta, resposta in perguntas:
            palpite = input_with_timeout(pergunta, tempo_de_resposta, root)
            if palpite == "dica":
                messagebox.showinfo("Dica", resposta['dica'], parent=root)
                pontuacao -= 1
            elif palpite.lower() == resposta['resposta'].lower():
                messagebox.showinfo("Correto", "Correto!", parent=root)
                pontuacao += 2
                dificuldade = min(dificuldade + 1, 2)
            else:
                messagebox.showinfo("Incorreto", f"Incorreto. A resposta correta é: {resposta['resposta']}", parent=root)
                dificuldade = max(dificuldade - 1, 0)

        cont += 1

    messagebox.showinfo("Fim do jogo", f"Fim do jogo! Sua pontuação final é: {pontuacao}", parent=root)

def iniciar_modo(modo, tema_var, dificuldade_var, root):
    tema = tema_var.get()
    dificuldade = dificuldade_var.get()
    if tema == "Biologia":
        tema = 0
    elif tema == "Computadores":
        tema = 1
    else:
        messagebox.showerror("Erro", "Tema inválido", parent=root)
        return

    if dificuldade == "Fácil":
        dificuldade = 0
    elif dificuldade == "Normal":
        dificuldade = 1
    elif dificuldade == "Difícil":
        dificuldade = 2
    else:
        messagebox.showerror("Erro", "Dificuldade inválida", parent=root)
        return

    matriz = [
        [perguntas_bio.bio_facil, perguntas_computador.compu_facil],
        [perguntas_bio.bio_normal, perguntas_computador.compu_normal],
        [perguntas_bio.bio_dificil, perguntas_computador.compu_dificil]
    ]

    perguntas = matriz[dificuldade][tema]

    # Cria nova janela e fecha a anterior
    nova_janela = tk.Tk()
    nova_janela.title("Modo de Jogo")
    root.destroy()

    if modo == "normal":
        modo_normal(perguntas, nova_janela)
    elif modo == "estudo":
        modo_estudo(perguntas, nova_janela)
    elif modo == "multiplayer":
        modo_multiplayer(perguntas, nova_janela)
    elif modo == "adaptativo":
        modo_adptativo(matriz, tema, dificuldade, nova_janela)
    else:
        messagebox.showerror("Erro", "Modo de jogo inválido", parent=nova_janela)

def menu():
    root = tk.Tk()
    root.title("Jogo de Perguntas e Respostas")

    tk.Label(root, text="Bem-vindo ao jogo de Perguntas e Respostas!").pack(pady=10)

    tk.Label(root, text="Escolha o tema:").pack()
    tema_var = tk.StringVar(value="Biologia")
    tk.OptionMenu(root, tema_var, "Biologia", "Computadores").pack()

    tk.Label(root, text="Escolha a dificuldade:").pack()
    dificuldade_var = tk.StringVar(value="Fácil")
    tk.OptionMenu(root, dificuldade_var, "Fácil", "Normal", "Difícil").pack()

    tk.Button(root, text="Modo Normal", command=lambda: iniciar_modo("normal", tema_var, dificuldade_var, root)).pack(pady=5)
    tk.Button(root, text="Modo Estudo", command=lambda: iniciar_modo("estudo", tema_var, dificuldade_var, root)).pack(pady=5)
    tk.Button(root, text="Modo Multiplayer", command=lambda: iniciar_modo("multiplayer", tema_var, dificuldade_var, root)).pack(pady=5)
    tk.Button(root, text="Modo Adaptativo", command=lambda: iniciar_modo("adaptativo", tema_var, dificuldade_var, root)).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    menu()
