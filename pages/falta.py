import tkinter as tk
from tkinter import messagebox, ttk
import requests

API_URL = "http://127.0.0.1:8000/faltas/"

def cadastrar_falta():
    try:
        data = {
            "nome_jogador": entry_nome_jogador.get(),
            "minuto_ocorrido": int(entry_minuto.get()),
            "tipo_cartao": entry_cartao.get(),
            "descricao": entry_descricao.get(),
            "dentro_area": bool(var_dentro_area.get())
        }
        response = requests.post(API_URL, json=data)
        if response.status_code in (200, 201):
            messagebox.showinfo("Sucesso", "Falta cadastrada!")
            listar_faltas()
        else:
            messagebox.showerror("Erro", response.json().get("detail", "Erro ao cadastrar falta"))
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def listar_faltas():
    response = requests.get(API_URL)
    if response.status_code == 200:
        limpar_tabela()
        for falta in response.json():
            tree.insert("", "end", values=(
                falta["nome_jogador"],
                falta["minuto_ocorrido"],
                falta["tipo_cartao"],
                falta["descricao"],
                falta["dentro_area"]
            ))
    else:
        messagebox.showerror("Erro", "Erro ao listar faltas.")

def listar_falta_por_id():
    falta_id = entry_id.get()
    if falta_id:
        response = requests.get(API_URL + falta_id)
        if response.status_code == 200:
            limpar_tabela()
            falta = response.json()
            tree.insert("", "end", values=(
                falta["nome_jogador"],
                falta["minuto_ocorrido"],
                falta["tipo_cartao"],
                falta["descricao"],
                falta["dentro_area"]
            ))
        else:
            messagebox.showerror("Erro", "Falta não encontrada.")
    else:
        messagebox.showwarning("Atenção", "Informe o ID da falta.")

def atualizar_falta():
    falta_id = entry_id.get()
    if falta_id:
        try:
            data = {
                "nome_jogador": entry_nome_jogador.get(),
                "minuto_ocorrido": int(entry_minuto.get()),
                "tipo_cartao": entry_cartao.get(),
                "descricao": entry_descricao.get(),
                "dentro_area": bool(var_dentro_area.get())
            }
            response = requests.put(API_URL + falta_id, json=data)
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Falta atualizada!")
                listar_faltas()
            else:
                messagebox.showerror("Erro", response.json().get("detail", "Erro ao atualizar"))
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    else:
        messagebox.showwarning("Atenção", "Informe o ID da falta.")

def deletar_falta():
    falta_id = entry_id.get()
    if falta_id:
        response = requests.delete(API_URL + falta_id)
        if response.status_code == 200:
            messagebox.showinfo("Sucesso", "Falta deletada!")
            listar_faltas()
        else:
            messagebox.showerror("Erro", response.json().get("detail", "Erro ao deletar"))
    else:
        messagebox.showwarning("Atenção", "Informe o ID da falta.")

def limpar_tabela():
    for item in tree.get_children():
        tree.delete(item)

def main():
    global entry_id, entry_nome_jogador, entry_minuto, entry_cartao, entry_descricao, var_dentro_area, tree

    root = tk.Tk()
    root.title("Gestão de Faltas ⚽")
    root.configure(bg="#0b6623")

    frame_inputs = tk.Frame(root, bg="#0b6623")
    frame_inputs.pack(pady=10)

    tk.Label(frame_inputs, text="ID:", bg="#0b6623", fg="white").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_id = tk.Entry(frame_inputs)
    entry_id.grid(row=0, column=1)

    tk.Label(frame_inputs, text="Jogador:", bg="#0b6623", fg="white").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_nome_jogador = tk.Entry(frame_inputs)
    entry_nome_jogador.grid(row=1, column=1)

    tk.Label(frame_inputs, text="Minuto:", bg="#0b6623", fg="white").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_minuto = tk.Entry(frame_inputs)
    entry_minuto.grid(row=2, column=1)

    tk.Label(frame_inputs, text="Cartão (amarelo, vermelho, sem_cartao):", bg="#0b6623", fg="white").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    entry_cartao = tk.Entry(frame_inputs)
    entry_cartao.grid(row=3, column=1)

    tk.Label(frame_inputs, text="Descrição:", bg="#0b6623", fg="white").grid(row=4, column=0, padx=5, pady=5, sticky="w")
    entry_descricao = tk.Entry(frame_inputs)
    entry_descricao.grid(row=4, column=1)

    var_dentro_area = tk.IntVar(value=0)
    chk_dentro_area = tk.Checkbutton(frame_inputs, text="Dentro da Área", variable=var_dentro_area, onvalue=1, offvalue=0, bg="#0b6623", fg="white", selectcolor="#0b6623", activebackground="#0b6623", anchor="w")
    chk_dentro_area.grid(row=5, column=0, columnspan=2, sticky="w", padx=5, pady=5)

    frame_botoes = tk.Frame(root, bg="#0b6623")
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="Cadastrar", command=cadastrar_falta, bg="#228B22", fg="white", width=12).grid(row=0, column=0, padx=5)
    tk.Button(frame_botoes, text="Listar todas", command=listar_faltas, bg="#1E90FF", fg="white", width=12).grid(row=0, column=1, padx=5)
    tk.Button(frame_botoes, text="Listar por ID", command=listar_falta_por_id, bg="#DAA520", fg="white", width=12).grid(row=0, column=2, padx=5)
    tk.Button(frame_botoes, text="Atualizar", command=atualizar_falta, bg="#8B008B", fg="white", width=12).grid(row=0, column=3, padx=5)
    tk.Button(frame_botoes, text="Deletar", command=deletar_falta, bg="#B22222", fg="white", width=12).grid(row=0, column=4, padx=5)

    tree = ttk.Treeview(root, columns=("Jogador", "Minuto", "Cartão", "Descrição", "Dentro da Área"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(pady=10)

    listar_faltas()

    root.mainloop()

if __name__ == "__main__":
    main()