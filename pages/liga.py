import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_URL = "http://127.0.0.1:8000/ligas/"

def listar_ligas():
    for item in tree.get_children():
        tree.delete(item)

    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        ligas = response.json()

        for liga in ligas:
            tree.insert("", tk.END, values=(liga["id"], liga["nome"], liga["pais"]))
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Falha ao buscar ligas: {e}")

def buscar_por_id():
    liga_id = entry_id.get()
    if not liga_id:
        messagebox.showwarning("Campos obrigatórios", "Informe o ID da liga que deseja buscar.")
        return

    try:
        response = requests.get(f"{API_URL}{liga_id}")
        if response.status_code == 404:
            messagebox.showwarning("Erro", "Liga não encontrada.")
            return

        response.raise_for_status()
        liga = response.json()

        entry_nome.delete(0, tk.END)
        entry_pais.delete(0, tk.END)
        entry_nome.insert(0, liga["nome"])
        entry_pais.insert(0, liga["pais"])

        for item in tree.get_children():
            tree.delete(item)
        tree.insert("", tk.END, values=(liga["id"], liga["nome"], liga["pais"]))

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Falha ao buscar liga por ID: {e}")

def cadastrar_liga():
    nome = entry_nome.get()
    pais = entry_pais.get()

    if not nome or not pais:
        messagebox.showwarning("Campos obrigatórios", "Preencha Nome e País.")
        return

    try:
        response = requests.post(API_URL, json={"nome": nome, "pais": pais})
        response.raise_for_status()
        messagebox.showinfo("Sucesso", "Liga cadastrada com sucesso!")
        listar_ligas()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Falha ao cadastrar liga: {e}")

def atualizar_liga():
    liga_id = entry_id.get()
    nome = entry_nome.get()
    pais = entry_pais.get()

    if not liga_id:
        messagebox.showwarning("Campos obrigatórios", "Informe o ID da liga que deseja atualizar.")
        return

    if not nome and not pais:
        messagebox.showwarning("Campos obrigatórios", "Informe ao menos Nome ou País para atualizar.")
        return

    data = {}
    if nome:
        data["nome"] = nome
    if pais:
        data["pais"] = pais

    try:
        response = requests.put(f"{API_URL}{liga_id}", json=data)
        if response.status_code == 404:
            messagebox.showwarning("Erro", "Liga não encontrada.")
        else:
            response.raise_for_status()
            messagebox.showinfo("Sucesso", "Liga atualizada com sucesso!")
            listar_ligas()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Falha ao atualizar liga: {e}")

def deletar_liga():
    liga_id = entry_id.get()

    if not liga_id:
        messagebox.showwarning("Campos obrigatórios", "Informe o ID da liga que deseja deletar.")
        return

    if messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir a liga ID {liga_id}?"):
        try:
            response = requests.delete(f"{API_URL}{liga_id}")
            if response.status_code == 400:
                messagebox.showwarning("Erro", "Não é possível excluir uma liga com clubes associados.")
            elif response.status_code == 404:
                messagebox.showwarning("Erro", "Liga não encontrada.")
            else:
                response.raise_for_status()
                messagebox.showinfo("Sucesso", "Liga deletada com sucesso!")
                listar_ligas()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Falha ao excluir liga: {e}")

def preencher_campos(event):
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        entry_id.delete(0, tk.END)
        entry_nome.delete(0, tk.END)
        entry_pais.delete(0, tk.END)
        entry_id.insert(0, item["values"][0])
        entry_nome.insert(0, item["values"][1])
        entry_pais.insert(0, item["values"][2])

def main():
    global root, entry_id, entry_nome, entry_pais, tree

    root = tk.Tk()
    root.title("🏆 Gestão de Ligas 🌍")
    root.configure(bg="#0b6623")

    frame_inputs = tk.Frame(root, bg="#0b6623")
    frame_inputs.pack(pady=10)

    tk.Label(frame_inputs, text="ID da Liga:", bg="#0b6623", fg="white").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_id = tk.Entry(frame_inputs, width=30)
    entry_id.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_inputs, text="Nome da Liga:", bg="#0b6623", fg="white").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_nome = tk.Entry(frame_inputs, width=30)
    entry_nome.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_inputs, text="País:", bg="#0b6623", fg="white").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_pais = tk.Entry(frame_inputs, width=30)
    entry_pais.grid(row=2, column=1, padx=5, pady=5)

    frame_botoes = tk.Frame(root, bg="#0b6623")
    frame_botoes.pack(pady=5)

    tk.Button(frame_botoes, text="Cadastrar", bg="#228B22", fg="white", command=cadastrar_liga).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes, text="Atualizar", bg="#8B008B", fg="white", command=atualizar_liga).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes, text="Deletar", bg="#B22222", fg="white", command=deletar_liga).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes, text="Listar", bg="#1E90FF", fg="white", command=listar_ligas).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes, text="Buscar por ID", bg="#DAA520", fg="black", command=buscar_por_id).pack(side=tk.LEFT, padx=5)

    frame_tabela = tk.Frame(root, bg="#0b6623")
    frame_tabela.pack(pady=10)

    colunas = ("ID", "Nome", "País")
    tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack()

    tree.bind("<<TreeviewSelect>>", preencher_campos)

    listar_ligas()

    root.mainloop()

if __name__ == "__main__":
    main()
