import tkinter as tk
from tkinter import messagebox

def abrir_tela_ligas():
    import liga
    liga.main()

def abrir_tela_clubes():
    import clube 
    clube.main()

def abrir_tela_jogadores():
    import jogador 
    jogador.main()

def abrir_tela_partidas():
    import partida
    partida.main()

def abrir_tela_faltas():
    import falta
    falta.main()

def abrir_tela_lesoes():
    import lesao
    lesao.main()

def abrir_tela_estatisticas_jogador():
    import estatistica_jogador
    estatistica_jogador.main()

root = tk.Tk()
root.title("🏆 Sistema de Futebol - Menu Principal ⚽")
root.configure(bg="#0b6623")

titulo = tk.Label(root, text="🏆 Bem-vindo ao GameStats ⚽", font=("Helvetica", 18, "bold"), bg="#0b6623", fg="white")
titulo.pack(pady=20)

logo = tk.Label(root, text="🌍⚽🏅 Liga Nacional de Futebol", font=("Helvetica", 14), bg="#0b6623", fg="white")
logo.pack(pady=5)

frame_botoes = tk.Frame(root, bg="#0b6623")
frame_botoes.pack(pady=20)

tk.Button(frame_botoes, text="🏆 Ligas", bg="#2e8b57", fg="white", font=("Helvetica", 12, "bold"), width=20, command=abrir_tela_ligas).pack(pady=10)
tk.Button(frame_botoes, text="⚽ Clubes", bg="#1f77b4", fg="white", font=("Helvetica", 12, "bold"), width=20, command=abrir_tela_clubes).pack(pady=10)
tk.Button(frame_botoes, text="👟 Jogadores", bg="#e07a5f", fg="white", font=("Helvetica", 12, "bold"), width=20, command=abrir_tela_jogadores).pack(pady=10)
tk.Button(frame_botoes, text="🏟️ Partidas", bg="#FF8C00", fg="white", font=("Helvetica", 12, "bold"), width=20, command=abrir_tela_partidas).pack(pady=10)
tk.Button(frame_botoes, text="➕ Faltas", bg="#F3DC08", fg="white", font=("Helvetica", 12, "bold"), width=20, command=abrir_tela_faltas).pack(pady=10)
tk.Button(frame_botoes, text="🏥 Lesões", bg="#DC143C", fg="white", font=("Helvetica", 12, "bold"), width=20, command=abrir_tela_lesoes).pack(pady=10)
tk.Button(frame_botoes, text="📊 Estatísticas", bg="#4B0082", fg="white", font=("Helvetica", 12, "bold"), width=20, command=abrir_tela_estatisticas_jogador).pack(pady=10)

rodape = tk.Label(root, text="⚽🏆🥅🏅🏟️", font=("Helvetica", 20), bg="#0b6623", fg="white")
rodape.pack(pady=20)

root.mainloop()
