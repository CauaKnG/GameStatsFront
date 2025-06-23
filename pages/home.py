import tkinter as tk
from tkinter import messagebox

def abrir_tela_ligas():
    import ligas
    ligas.main()

def abrir_tela_clubes():
    import clubes
    clubes.main()

def abrir_tela_jogadores():
    messagebox.showinfo("Em construção", "Tela de jogadores ainda não criada.")

root = tk.Tk()
root.title("🏆 Sistema de Futebol - Menu Principal ⚽")
root.configure(bg="#0b6623")  # Verde grama

# --- Título ---
titulo = tk.Label(root, text="🏆 Bem-vindo ao GameStats ⚽", font=("Helvetica", 18, "bold"), bg="#0b6623", fg="white")
titulo.pack(pady=20)

# --- Logo (simulada com texto) ---
logo = tk.Label(root, text="🌍⚽🏅 Liga Nacional de Futebol", font=("Helvetica", 14), bg="#0b6623", fg="white")
logo.pack(pady=5)

# --- Frame de botões ---
frame_botoes = tk.Frame(root, bg="#0b6623")
frame_botoes.pack(pady=20)

btn_ligas = tk.Button(frame_botoes, text="⚽ Ligas", bg="#2e8b57", fg="white", font=("Helvetica", 12, "bold"), width=20, command=abrir_tela_ligas)
btn_ligas.pack(pady=10)

btn_clubes = tk.Button(frame_botoes, text="🏆 Clubes", bg="#1f77b4", fg="white", font=("Helvetica", 12, "bold"), width=20, command=abrir_tela_clubes)
btn_clubes.pack(pady=10)

btn_jogadores = tk.Button(frame_botoes, text="👟 Jogadores", bg="#e07a5f", fg="white", font=("Helvetica", 12, "bold"), width=20, command=abrir_tela_jogadores)
btn_jogadores.pack(pady=10)

# --- Rodapé com emojis temáticos ---
rodape = tk.Label(root, text="⚽🏆🥅🏅🏟️", font=("Helvetica", 20), bg="#0b6623", fg="white")
rodape.pack(pady=20)

root.mainloop()
