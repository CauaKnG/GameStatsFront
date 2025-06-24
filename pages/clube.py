import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_URL = "http://127.0.0.1:8000/clubes/"

def listar_clubes():
    global tree
    for item in tree.get_children():
        tree.delete(item)

    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        clubes = response.json()

        for clube in clubes:
            liga_nome = clube["liga"]["nome"] if clube.get("liga") else "N/A"
            tree.insert("", tk.END, values=(clube["id"], clube["nome"], clube.get("cidade", ""), liga_nome))
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Falha ao buscar clubes: {e}")

def buscar_por_id():
    global entry_id, entry_nome, entry_cidade, entry_liga, tree
    clube_id = entry_id.get()
    if not clube_id:
        messagebox.showwarning("Campos obrigatórios", "Informe o ID do clube que deseja buscar.")
        return

    try:
        response = requests.get(f"{API_URL}{clube_id}")
        if response.status_code == 404:
            messagebox.showwarning("Erro", "Clube não encontrado.")
            return

        response.raise_for_status()
        clube = response.json()

        entry_nome.delete(0, tk.END)
        entry_cidade.delete(0, tk.END)
        entry_liga.delete(0, tk.END)

        entry_nome.insert(0, clube["nome"])
        entry_cidade.insert(0, clube.get("cidade", ""))
        entry_liga.insert(0, clube["liga"]["nome"])

        for item in tree.get_children():
            tree.delete(item)
        tree.insert("", tk.END, values=(clube["id"], clube["nome"], clube.get("cidade", ""), clube["liga"]["nome"]))

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Falha ao buscar clube por ID: {e}")

def cadastrar_clube():
    global entry_nome, entry_cidade, entry_liga
    nome = entry_nome.get()
    cidade = entry_cidade.get()
    nome_liga = entry_liga.get()

    if not nome or not cidade or not nome_liga:
        messagebox.showwarning("Campos obrigatórios", "Preencha Nome, Cidade e Nome da Liga.")
        return

    try:
        response = requests.post(API_URL, json={"nome": nome, "cidade": cidade, "nome_liga": nome_liga})
        if response.status_code == 400:
            messagebox.showwarning("Erro", response.json()["detail"])
        else:
            response.raise_for_status()
            messagebox.showinfo("Sucesso", "Clube cadastrado com sucesso!")
            listar_clubes()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Falha ao cadastrar clube: {e}")

def atualizar_clube():
    global entry_id, entry_nome, entry_cidade, entry_liga
    clube_id = entry_id.get()
    nome = entry_nome.get()
    cidade = entry_cidade.get()
    nome_liga = entry_liga.get()

    if not clube_id:
        messagebox.showwarning("Campos obrigatórios", "Informe o ID do clube que deseja atualizar.")
        return

    if not nome and not cidade and not nome_liga:
        messagebox.showwarning("Campos obrigatórios", "Informe ao menos um campo para atualizar.")
        return

    data = {}
    if nome:
        data["nome"] = nome
    if cidade:
        data["cidade"] = cidade
    if nome_liga:
        data["nome_liga"] = nome_liga

    try:
        response = requests.put(f"{API_URL}{clube_id}", json=data)
        if response.status_code == 404:
            messagebox.showwarning("Erro", "Clube não encontrado.")
        elif response.status_code == 400:
            messagebox.showwarning("Erro", response.json()["detail"])
        else:
            response.raise_for_status()
            messagebox.showinfo("Sucesso", "Clube atualizado com sucesso!")
            listar_clubes()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Falha ao atualizar clube: {e}")

def deletar_clube():
    global entry_id
    clube_id = entry_id.get()

    if not clube_id:
        messagebox.showwarning("Campos obrigatórios", "Informe o ID do clube que deseja deletar.")
        return

    if messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir o clube ID {clube_id}?"):
        try:
            response = requests.delete(f"{API_URL}{clube_id}")
            if response.status_code == 404:
                messagebox.showwarning("Erro", "Clube não encontrado.")
            elif response.status_code == 400:
                messagebox.showwarning("Erro", response.json()["detail"])
            else:
                response.raise_for_status()
                messagebox.showinfo("Sucesso", "Clube deletado com sucesso!")
                listar_clubes()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Falha ao excluir clube: {e}")

def preencher_campos(event):
    global entry_id, entry_nome, entry_cidade, entry_liga, tree
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        entry_id.delete(0, tk.END)
        entry_nome.delete(0, tk.END)
        entry_cidade.delete(0, tk.END)
        entry_liga.delete(0, tk.END)

        entry_id.insert(0, item["values"][0])
        entry_nome.insert(0, item["values"][1])
        entry_cidade.insert(0, item["values"][2])
        entry_liga.insert(0, item["values"][3])

def main():
    global root, entry_id, entry_nome, entry_cidade, entry_liga, tree 

    root = tk.Tk()
    root.title("Gerenciamento de Clubes - Futebol")
    root.configure(bg="#1e5631")  

    frame_inputs = tk.Frame(root, bg="#1e5631")
    frame_inputs.pack(pady=10)

    tk.Label(frame_inputs, text="ID do Clube:", bg="#1e5631", fg="white").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_id = tk.Entry(frame_inputs, width=30)
    entry_id.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_inputs, text="Nome do Clube:", bg="#1e5631", fg="white").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_nome = tk.Entry(frame_inputs, width=30)
    entry_nome.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_inputs, text="Cidade:", bg="#1e5631", fg="white").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_cidade = tk.Entry(frame_inputs, width=30)
    entry_cidade.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame_inputs, text="Nome da Liga:", bg="#1e5631", fg="white").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    entry_liga = tk.Entry(frame_inputs, width=30)
    entry_liga.grid(row=3, column=1, padx=5, pady=5)

    frame_botoes = tk.Frame(root, bg="#1e5631")
    frame_botoes.pack(pady=5)

    btn_cadastrar = tk.Button(frame_botoes, text="Cadastrar", bg="#2e8b57", fg="white", command=cadastrar_clube)
    btn_cadastrar.pack(side=tk.LEFT, padx=5)

    btn_atualizar = tk.Button(frame_botoes, text="Atualizar", bg="#f4a261", fg="black", command=atualizar_clube)
    btn_atualizar.pack(side=tk.LEFT, padx=5)

    btn_deletar = tk.Button(frame_botoes, text="Deletar", bg="#e63946", fg="white", command=deletar_clube)
    btn_deletar.pack(side=tk.LEFT, padx=5)

    btn_listar = tk.Button(frame_botoes, text="Listar Tudo", bg="#264653", fg="white", command=listar_clubes)
    btn_listar.pack(side=tk.LEFT, padx=5)

    btn_buscar_id = tk.Button(frame_botoes, text="Buscar por ID", bg="#457b9d", fg="white", command=buscar_por_id)
    btn_buscar_id.pack(side=tk.LEFT, padx=5)

    frame_tabela = tk.Frame(root, bg="#1e5631")
    frame_tabela.pack(pady=10)

    colunas = ("ID", "Nome", "Cidade", "Liga")
    tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Cidade", text="Cidade")
    tree.heading("Liga", text="Liga")
    tree.column("ID", width=50)
    tree.column("Nome", width=150)
    tree.column("Cidade", width=150)
    tree.column("Liga", width=150)
    tree.pack()

    tree.bind("<<TreeviewSelect>>", preencher_campos)

    listar_clubes()

    root.mainloop()

if __name__ == "__main__":
    main()
