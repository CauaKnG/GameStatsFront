import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_URL = "http://127.0.0.1:8000/jogadores/"

def listar_jogadores():
    for item in tree.get_children():
        tree.delete(item)

    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        jogadores = response.json()

        for j in jogadores:
            clube_nome = j["clube"]["nome"] if j.get("clube") else "N/A"
            tree.insert("", tk.END, values=(
                j["id"], j["nome"], j["idade"], j["posicao"], j["overall"], clube_nome
            ))
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Falha ao buscar jogadores: {e}")

def buscar_por_id():
    jogador_id = entry_id.get()
    if not jogador_id:
        messagebox.showwarning("Campos obrigatórios", "Informe o ID do jogador que deseja buscar.")
        return

    try:
        response = requests.get(f"{API_URL}{jogador_id}")
        if response.status_code == 404:
            messagebox.showwarning("Erro", "Jogador não encontrado.")
            return

        response.raise_for_status()
        j = response.json()

        entry_nome.delete(0, tk.END)
        entry_idade.delete(0, tk.END)
        entry_posicao.delete(0, tk.END)
        entry_overall.delete(0, tk.END)
        entry_clube.delete(0, tk.END)

        entry_nome.insert(0, j["nome"])
        entry_idade.insert(0, j["idade"])
        entry_posicao.insert(0, j["posicao"])
        entry_overall.insert(0, j["overall"])
        entry_clube.insert(0, j["clube"]["nome"])

        for item in tree.get_children():
            tree.delete(item)
        tree.insert("", tk.END, values=(
            j["id"], j["nome"], j["idade"], j["posicao"], j["overall"], j["clube"]["nome"]
        ))

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Falha ao buscar jogador por ID: {e}")

def cadastrar_jogador():
    nome = entry_nome.get()
    idade = entry_idade.get()
    posicao = entry_posicao.get()
    overall = entry_overall.get()
    clube_nome = entry_clube.get()

    if not (nome and idade and posicao and overall and clube_nome):
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
        return

    try:
        idade_int = int(idade)
        overall_int = int(overall)
    except ValueError:
        messagebox.showwarning("Erro", "Idade e Overall devem ser números inteiros.")
        return

    try:
        response = requests.post(API_URL, json={
            "nome": nome,
            "idade": idade_int,
            "posicao": posicao,
            "overall": overall_int,
            "clube_nome": clube_nome
        })
        if response.status_code == 400 or response.status_code == 404:
            messagebox.showwarning("Erro", response.json().get("detail", "Erro desconhecido"))
        else:
            response.raise_for_status()
            messagebox.showinfo("Sucesso", "Jogador cadastrado com sucesso!")
            listar_jogadores()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Falha ao cadastrar jogador: {e}")

def atualizar_jogador():
    jogador_id = entry_id.get()
    nome = entry_nome.get()
    idade = entry_idade.get()
    posicao = entry_posicao.get()
    overall = entry_overall.get()
    clube_nome = entry_clube.get()

    if not jogador_id:
        messagebox.showwarning("Campos obrigatórios", "Informe o ID do jogador que deseja atualizar.")
        return

    data = {}
    if nome:
        data["nome"] = nome
    if idade:
        try:
            data["idade"] = int(idade)
        except ValueError:
            messagebox.showwarning("Erro", "Idade deve ser um número inteiro.")
            return
    if posicao:
        data["posicao"] = posicao
    if overall:
        try:
            data["overall"] = int(overall)
        except ValueError:
            messagebox.showwarning("Erro", "Overall deve ser um número inteiro.")
            return
    if clube_nome:
        data["clube_nome"] = clube_nome

    if not data:
        messagebox.showwarning("Campos obrigatórios", "Informe ao menos um campo para atualizar.")
        return

    try:
        response = requests.put(f"{API_URL}{jogador_id}", json=data)
        if response.status_code == 404:
            messagebox.showwarning("Erro", "Jogador ou clube não encontrado.")
        elif response.status_code == 400:
            messagebox.showwarning("Erro", response.json().get("detail", "Erro desconhecido"))
        else:
            response.raise_for_status()
            messagebox.showinfo("Sucesso", "Jogador atualizado com sucesso!")
            listar_jogadores()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Falha ao atualizar jogador: {e}")

def deletar_jogador():
    jogador_id = entry_id.get()

    if not jogador_id:
        messagebox.showwarning("Campos obrigatórios", "Informe o ID do jogador que deseja deletar.")
        return

    if messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir o jogador ID {jogador_id}?"):
        try:
            response = requests.delete(f"{API_URL}{jogador_id}")
            if response.status_code == 404:
                messagebox.showwarning("Erro", "Jogador não encontrado.")
            else:
                response.raise_for_status()
                messagebox.showinfo("Sucesso", "Jogador deletado com sucesso!")
                listar_jogadores()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Falha ao excluir jogador: {e}")

def preencher_campos(event):
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        entry_id.delete(0, tk.END)
        entry_nome.delete(0, tk.END)
        entry_idade.delete(0, tk.END)
        entry_posicao.delete(0, tk.END)
        entry_overall.delete(0, tk.END)
        entry_clube.delete(0, tk.END)

        entry_id.insert(0, item["values"][0])
        entry_nome.insert(0, item["values"][1])
        entry_idade.insert(0, item["values"][2])
        entry_posicao.insert(0, item["values"][3])
        entry_overall.insert(0, item["values"][4])
        entry_clube.insert(0, item["values"][5])

def main():
    global root, entry_id, entry_nome, entry_idade, entry_posicao, entry_overall, entry_clube, tree

    root = tk.Tk()
    root.title("Gerenciamento de Jogadores - Futebol")
    root.configure(bg="#1e5631")  

    frame_inputs = tk.Frame(root, bg="#1e5631")
    frame_inputs.pack(pady=10)

    tk.Label(frame_inputs, text="ID do Jogador:", bg="#1e5631", fg="white").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_id = tk.Entry(frame_inputs, width=30)
    entry_id.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_inputs, text="Nome:", bg="#1e5631", fg="white").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_nome = tk.Entry(frame_inputs, width=30)
    entry_nome.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_inputs, text="Idade:", bg="#1e5631", fg="white").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_idade = tk.Entry(frame_inputs, width=30)
    entry_idade.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame_inputs, text="Posição:", bg="#1e5631", fg="white").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    entry_posicao = tk.Entry(frame_inputs, width=30)
    entry_posicao.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(frame_inputs, text="Overall:", bg="#1e5631", fg="white").grid(row=4, column=0, padx=5, pady=5, sticky="e")
    entry_overall = tk.Entry(frame_inputs, width=30)
    entry_overall.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(frame_inputs, text="Nome do Clube:", bg="#1e5631", fg="white").grid(row=5, column=0, padx=5, pady=5, sticky="e")
    entry_clube = tk.Entry(frame_inputs, width=30)
    entry_clube.grid(row=5, column=1, padx=5, pady=5)

    frame_botoes = tk.Frame(root, bg="#1e5631")
    frame_botoes.pack(pady=5)

    btn_cadastrar = tk.Button(frame_botoes, text="Cadastrar", bg="#2e8b57", fg="white", command=cadastrar_jogador)
    btn_cadastrar.pack(side=tk.LEFT, padx=5)

    btn_atualizar = tk.Button(frame_botoes, text="Atualizar", bg="#f4a261", fg="black", command=atualizar_jogador)
    btn_atualizar.pack(side=tk.LEFT, padx=5)

    btn_deletar = tk.Button(frame_botoes, text="Deletar", bg="#e63946", fg="white", command=deletar_jogador)
    btn_deletar.pack(side=tk.LEFT, padx=5)

    btn_listar = tk.Button(frame_botoes, text="Listar Tudo", bg="#264653", fg="white", command=listar_jogadores)
    btn_listar.pack(side=tk.LEFT, padx=5)

    btn_buscar_id = tk.Button(frame_botoes, text="Buscar por ID", bg="#457b9d", fg="white", command=buscar_por_id)
    btn_buscar_id.pack(side=tk.LEFT, padx=5)

    frame_tabela = tk.Frame(root, bg="#1e5631")
    frame_tabela.pack(pady=10)

    colunas = ("ID", "Nome", "Idade", "Posição", "Overall", "Clube")
    tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
    for c in colunas:
        tree.heading(c, text=c)
        if c == "ID":
            tree.column(c, width=50)
        else:
            tree.column(c, width=130)
    tree.pack()

    tree.bind("<<TreeviewSelect>>", preencher_campos)

    listar_jogadores()

    root.mainloop()

if __name__ == "__main__":
    main()
