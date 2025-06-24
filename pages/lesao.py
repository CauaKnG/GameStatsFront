import tkinter as tk
from tkinter import messagebox, ttk
import requests

API_URL = "http://127.0.0.1:8000/lesoes/"

def cadastrar_lesao():
    try:
        data = {
            "nome_jogador": entry_nome_jogador.get(),
            "tipo_lesao": entry_tipo.get(),
            "data_lesao": entry_data.get(),
            "duracao_estimada_dias": int(entry_duracao.get())
        }
        response = requests.post(API_URL, json=data)
        if response.status_code in (200, 201):
            messagebox.showinfo("Sucesso", "Lesão cadastrada!")
            listar_lesoes()
        else:
            messagebox.showerror("Erro", response.json().get("detail", "Erro ao cadastrar lesão"))
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def listar_lesoes():
    response = requests.get(API_URL)
    if response.status_code == 200:
        limpar_tabela()
        for lesao in response.json():
            tree.insert("", "end", values=(
                lesao["id"],
                lesao["nome_jogador"],
                lesao["tipo_lesao"],
                lesao["data_lesao"],
                lesao["duracao_estimada_dias"]
            ))
    else:
        messagebox.showerror("Erro", "Erro ao listar lesões.")

def listar_lesao_por_id():
    lesao_id = entry_id.get()
    if lesao_id:
        response = requests.get(API_URL + lesao_id)
        if response.status_code == 200:
            limpar_tabela()
            lesao = response.json()
            tree.insert("", "end", values=(
                lesao["id"],
                lesao["nome_jogador"],
                lesao["tipo_lesao"],
                lesao["data_lesao"],
                lesao["duracao_estimada_dias"]
            ))
        else:
            messagebox.showerror("Erro", "Lesão não encontrada.")
    else:
        messagebox.showwarning("Atenção", "Informe o ID da lesão.")

def atualizar_lesao():
    lesao_id = entry_id.get()
    if lesao_id:
        try:
            data = {
                "nome_jogador": entry_nome_jogador.get(),
                "tipo_lesao": entry_tipo.get(),
                "data_lesao": entry_data.get(),
                "duracao_estimada_dias": int(entry_duracao.get())
            }
            response = requests.put(API_URL + lesao_id, json=data)
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Lesão atualizada!")
                listar_lesoes()
            else:
                messagebox.showerror("Erro", response.json().get("detail", "Erro ao atualizar"))
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    else:
        messagebox.showwarning("Atenção", "Informe o ID da lesão.")

def deletar_lesao():
    lesao_id = entry_id.get()
    if lesao_id:
        response = requests.delete(API_URL + lesao_id)
        if response.status_code == 200:
            messagebox.showinfo("Sucesso", "Lesão deletada!")
            listar_lesoes()
        else:
            messagebox.showerror("Erro", response.json().get("detail", "Erro ao deletar"))
    else:
        messagebox.showwarning("Atenção", "Informe o ID da lesão.")

def limpar_tabela():
    for item in tree.get_children():
        tree.delete(item)

def main():
    global entry_id, entry_nome_jogador, entry_tipo, entry_data, entry_duracao, tree

    root = tk.Tk()
    root.title("🩼 Gestão de Lesões ⚽")
    root.configure(bg="#0b6623")

    frame_inputs = tk.Frame(root, bg="#0b6623")
    frame_inputs.pack(pady=10)

    tk.Label(frame_inputs, text="ID:", bg="#0b6623", fg="white").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_id = tk.Entry(frame_inputs)
    entry_id.grid(row=0, column=1)

    tk.Label(frame_inputs, text="Jogador:", bg="#0b6623", fg="white").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_nome_jogador = tk.Entry(frame_inputs)
    entry_nome_jogador.grid(row=1, column=1)

    tk.Label(frame_inputs, text="Tipo de Lesão:", bg="#0b6623", fg="white").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_tipo = tk.Entry(frame_inputs)
    entry_tipo.grid(row=2, column=1)

    tk.Label(frame_inputs, text="Data da Lesão (YYYY-MM-DD):", bg="#0b6623", fg="white").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    entry_data = tk.Entry(frame_inputs)
    entry_data.grid(row=3, column=1)

    tk.Label(frame_inputs, text="Duração Estimada (dias):", bg="#0b6623", fg="white").grid(row=4, column=0, padx=5, pady=5, sticky="w")
    entry_duracao = tk.Entry(frame_inputs)
    entry_duracao.grid(row=4, column=1)

    frame_botoes = tk.Frame(root, bg="#0b6623")
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="Cadastrar", command=cadastrar_lesao, bg="#228B22", fg="white", width=12).grid(row=0, column=0, padx=5)
    tk.Button(frame_botoes, text="Listar todas", command=listar_lesoes, bg="#1E90FF", fg="white", width=12).grid(row=0, column=1, padx=5)
    tk.Button(frame_botoes, text="Listar por ID", command=listar_lesao_por_id, bg="#DAA520", fg="white", width=12).grid(row=0, column=2, padx=5)
    tk.Button(frame_botoes, text="Atualizar", command=atualizar_lesao, bg="#8B008B", fg="white", width=12).grid(row=0, column=3, padx=5)
    tk.Button(frame_botoes, text="Deletar", command=deletar_lesao, bg="#B22222", fg="white", width=12).grid(row=0, column=4, padx=5)

    tree = ttk.Treeview(root, columns=("ID", "Jogador", "Tipo", "Data", "Duração"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(pady=10)

    listar_lesoes()

    root.mainloop()

if __name__ == "__main__":
    main()
