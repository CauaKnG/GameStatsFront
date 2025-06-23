import tkinter as tk
from tkinter import messagebox, ttk
import requests

API_URL = "http://127.0.0.1:8000/partidas/"

def cadastrar_partida():
    try:
        data = {
            "data_partida": entry_data.get(),
            "local": entry_local.get(),
            "clube_casa": entry_clube_casa.get(),
            "clube_fora": entry_clube_fora.get(),
            "gols_casa": int(entry_gols_casa.get()),
            "gols_fora": int(entry_gols_fora.get())
        }
        response = requests.post(API_URL, json=data)
        if response.status_code == 201:
            messagebox.showinfo("Sucesso", "Partida cadastrada com sucesso!")
            listar_partidas()
        else:
            messagebox.showerror("Erro", response.json().get("detail", "Erro ao cadastrar partida"))
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def listar_partidas():
    response = requests.get(API_URL)
    if response.status_code == 200:
        limpar_tabela()
        for partida in response.json():
            tree.insert("", "end", values=(
                partida["id"],
                partida["data_partida"],
                partida["local"],
                partida["clube_casa"],
                partida["clube_fora"],
                partida["gols_casa"],
                partida["gols_fora"]
            ))
    else:
        messagebox.showerror("Erro", "Erro ao listar partidas.")

def listar_partida_por_id():
    partida_id = entry_id.get()
    if partida_id:
        response = requests.get(API_URL + partida_id)
        if response.status_code == 200:
            limpar_tabela()
            partida = response.json()
            tree.insert("", "end", values=(
                partida["id"],
                partida["data_partida"],
                partida["local"],
                partida["clube_casa"],
                partida["clube_fora"],
                partida["gols_casa"],
                partida["gols_fora"]
            ))
        else:
            messagebox.showerror("Erro", "Partida não encontrada.")
    else:
        messagebox.showwarning("Atenção", "Informe o ID da partida.")

def atualizar_partida():
    partida_id = entry_id.get()
    if partida_id:
        try:
            data = {
                "data_partida": entry_data.get(),
                "local": entry_local.get(),
                "clube_casa": entry_clube_casa.get(),
                "clube_fora": entry_clube_fora.get(),
                "gols_casa": int(entry_gols_casa.get()),
                "gols_fora": int(entry_gols_fora.get())
            }
            response = requests.put(API_URL + partida_id, json=data)
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Partida atualizada!")
                listar_partidas()
            else:
                messagebox.showerror("Erro", response.json().get("detail", "Erro ao atualizar"))
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    else:
        messagebox.showwarning("Atenção", "Informe o ID da partida.")

def deletar_partida():
    partida_id = entry_id.get()
    if partida_id:
        response = requests.delete(API_URL + partida_id)
        if response.status_code == 200:
            messagebox.showinfo("Sucesso", "Partida deletada!")
            listar_partidas()
        else:
            messagebox.showerror("Erro", response.json().get("detail", "Erro ao deletar"))
    else:
        messagebox.showwarning("Atenção", "Informe o ID da partida.")

def limpar_tabela():
    for item in tree.get_children():
        tree.delete(item)

def main():
    global entry_id, entry_data, entry_local, entry_clube_casa, entry_clube_fora, entry_gols_casa, entry_gols_fora, tree

    root = tk.Tk()
    root.title("🏟️ Gestão de Partidas ⚽")
    root.configure(bg="#0b6623")

    frame_inputs = tk.Frame(root, bg="#0b6623")
    frame_inputs.pack(pady=10)

    tk.Label(frame_inputs, text="ID:", bg="#0b6623", fg="white").grid(row=0, column=0)
    entry_id = tk.Entry(frame_inputs)
    entry_id.grid(row=0, column=1)

    tk.Label(frame_inputs, text="Data (dd/mm/yyyy HH:MM):", bg="#0b6623", fg="white").grid(row=1, column=0)
    entry_data = tk.Entry(frame_inputs)
    entry_data.grid(row=1, column=1)

    tk.Label(frame_inputs, text="Local:", bg="#0b6623", fg="white").grid(row=2, column=0)
    entry_local = tk.Entry(frame_inputs)
    entry_local.grid(row=2, column=1)

    tk.Label(frame_inputs, text="Clube Casa:", bg="#0b6623", fg="white").grid(row=3, column=0)
    entry_clube_casa = tk.Entry(frame_inputs)
    entry_clube_casa.grid(row=3, column=1)

    tk.Label(frame_inputs, text="Clube Fora:", bg="#0b6623", fg="white").grid(row=4, column=0)
    entry_clube_fora = tk.Entry(frame_inputs)
    entry_clube_fora.grid(row=4, column=1)

    tk.Label(frame_inputs, text="Gols Casa:", bg="#0b6623", fg="white").grid(row=5, column=0)
    entry_gols_casa = tk.Entry(frame_inputs)
    entry_gols_casa.grid(row=5, column=1)

    tk.Label(frame_inputs, text="Gols Fora:", bg="#0b6623", fg="white").grid(row=6, column=0)
    entry_gols_fora = tk.Entry(frame_inputs)
    entry_gols_fora.grid(row=6, column=1)

    frame_botoes = tk.Frame(root, bg="#0b6623")
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="Cadastrar", command=cadastrar_partida, bg="#228B22", fg="white", width=12).grid(row=0, column=0, padx=5)
    tk.Button(frame_botoes, text="Listar todas", command=listar_partidas, bg="#1E90FF", fg="white", width=12).grid(row=0, column=1, padx=5)
    tk.Button(frame_botoes, text="Listar por ID", command=listar_partida_por_id, bg="#DAA520", fg="white", width=12).grid(row=0, column=2, padx=5)
    tk.Button(frame_botoes, text="Atualizar", command=atualizar_partida, bg="#8B008B", fg="white", width=12).grid(row=0, column=3, padx=5)
    tk.Button(frame_botoes, text="Deletar", command=deletar_partida, bg="#B22222", fg="white", width=12).grid(row=0, column=4, padx=5)

    tree = ttk.Treeview(root, columns=("ID", "Data", "Local", "Casa", "Fora", "Gols Casa", "Gols Fora"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
