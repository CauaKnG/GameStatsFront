import tkinter as tk
from tkinter import messagebox, ttk
import requests

API_URL = "http://127.0.0.1:8000/estatisticas_jogador/"

def cadastrar_estatistica():
    try:
        data = {
            "nome_jogador": entry_nome_jogador.get(),
            "gols": int(entry_gols.get()),
            "assistencias": int(entry_assistencias.get()),
            "passes_completos": int(entry_passes.get()),
            "finalizacoes": int(entry_finalizacoes.get()),
            "partida_id": int(entry_partida_id.get())
        }
        response = requests.post(API_URL, json=data)
        if response.status_code in (200, 201):
            messagebox.showinfo("Sucesso", "Estatística cadastrada!")
            listar_estatisticas()
        else:
            messagebox.showerror("Erro", response.json().get("detail", "Erro ao cadastrar"))
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def listar_estatisticas():
    response = requests.get(API_URL)
    if response.status_code == 200:
        limpar_tabela()
        for est in response.json():
            tree.insert("", "end", values=(
                est["id"],
                est["nome_jogador"],
                est["gols"],
                est["assistencias"],
                est["passes_completos"],
                est["finalizacoes"],
                est["partida_id"]
            ))
    else:
        messagebox.showerror("Erro", "Erro ao listar estatísticas.")

def listar_estatistica_por_id():
    estatistica_id = entry_id.get()
    if estatistica_id:
        response = requests.get(API_URL + estatistica_id)
        if response.status_code == 200:
            limpar_tabela()
            estatisticas = response.json()
            for est in estatisticas:
                tree.insert("", "end", values=(
                    est["id"],
                    est["nome_jogador"],
                    est["gols"],
                    est["assistencias"],
                    est["passes_completos"],
                    est["finalizacoes"],
                    est["partida_id"]
                ))
        else:
            messagebox.showerror("Erro", "Estatística não encontrada.")
    else:
        messagebox.showwarning("Atenção", "Informe o ID do jogador.")

def atualizar_estatistica():
    estatistica_id = entry_id.get()
    if estatistica_id:
        try:
            data = {
                "nome_jogador": entry_nome_jogador.get(),
                "gols": int(entry_gols.get()),
                "assistencias": int(entry_assistencias.get()),
                "passes_completos": int(entry_passes.get()),
                "finalizacoes": int(entry_finalizacoes.get()),
                "partida_id": int(entry_partida_id.get())
            }
            response = requests.put(API_URL + estatistica_id, json=data)
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Estatística atualizada!")
                listar_estatisticas()
            else:
                messagebox.showerror("Erro", response.json().get("detail", "Erro ao atualizar"))
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    else:
        messagebox.showwarning("Atenção", "Informe o ID da estatística.")

def deletar_estatistica():
    estatistica_id = entry_id.get()
    if estatistica_id:
        response = requests.delete(API_URL + estatistica_id)
        if response.status_code == 200:
            messagebox.showinfo("Sucesso", "Estatística deletada!")
            listar_estatisticas()
        else:
            messagebox.showerror("Erro", response.json().get("detail", "Erro ao deletar"))
    else:
        messagebox.showwarning("Atenção", "Informe o ID da estatística.")

def limpar_tabela():
    for item in tree.get_children():
        tree.delete(item)

def main():
    global entry_id, entry_nome_jogador, entry_gols, entry_assistencias, entry_passes, entry_finalizacoes, entry_partida_id, tree

    root = tk.Tk()
    root.title("📊 Gestão de Estatísticas de Jogadores ⚽")
    root.configure(bg="#0b6623")

    frame_inputs = tk.Frame(root, bg="#0b6623")
    frame_inputs.pack(pady=10)

    tk.Label(frame_inputs, text="ID do Jogador:", bg="#0b6623", fg="white").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_id = tk.Entry(frame_inputs)
    entry_id.grid(row=0, column=1)

    tk.Label(frame_inputs, text="Nome do Jogador:", bg="#0b6623", fg="white").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_nome_jogador = tk.Entry(frame_inputs)
    entry_nome_jogador.grid(row=1, column=1)

    tk.Label(frame_inputs, text="Gols:", bg="#0b6623", fg="white").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_gols = tk.Entry(frame_inputs)
    entry_gols.grid(row=2, column=1)

    tk.Label(frame_inputs, text="Assistências:", bg="#0b6623", fg="white").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    entry_assistencias = tk.Entry(frame_inputs)
    entry_assistencias.grid(row=3, column=1)

    tk.Label(frame_inputs, text="Passes Completos:", bg="#0b6623", fg="white").grid(row=4, column=0, padx=5, pady=5, sticky="w")
    entry_passes = tk.Entry(frame_inputs)
    entry_passes.grid(row=4, column=1)

    tk.Label(frame_inputs, text="Finalizações:", bg="#0b6623", fg="white").grid(row=5, column=0, padx=5, pady=5, sticky="w")
    entry_finalizacoes = tk.Entry(frame_inputs)
    entry_finalizacoes.grid(row=5, column=1)

    tk.Label(frame_inputs, text="Partida ID:", bg="#0b6623", fg="white").grid(row=6, column=0, padx=5, pady=5, sticky="w")
    entry_partida_id = tk.Entry(frame_inputs)
    entry_partida_id.grid(row=6, column=1)

    frame_botoes = tk.Frame(root, bg="#0b6623")
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="Cadastrar", command=cadastrar_estatistica, bg="#228B22", fg="white", width=12).grid(row=0, column=0, padx=5)
    tk.Button(frame_botoes, text="Listar Todas", command=listar_estatisticas, bg="#1E90FF", fg="white", width=12).grid(row=0, column=1, padx=5)
    tk.Button(frame_botoes, text="Listar por ID", command=listar_estatistica_por_id, bg="#DAA520", fg="white", width=12).grid(row=0, column=2, padx=5)
    tk.Button(frame_botoes, text="Atualizar", command=atualizar_estatistica, bg="#8B008B", fg="white", width=12).grid(row=0, column=3, padx=5)
    tk.Button(frame_botoes, text="Deletar", command=deletar_estatistica, bg="#B22222", fg="white", width=12).grid(row=0, column=4, padx=5)

    tree = ttk.Treeview(root, columns=("ID", "Jogador", "Gols", "Assistências", "Passes", "Finalizações", "Partida ID"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(pady=10)

    listar_estatisticas()

    root.mainloop()

if __name__ == "__main__":
    main()
