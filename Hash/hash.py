import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox


def calcular_hash_texto():
    texto = entry_texto.get()
    if not texto:
        messagebox.showwarning("Aviso", "Por favor, introduza um texto.")
        return
    hash_resultado = hashlib.sha256(texto.encode("utf-8")).hexdigest()
    resultado_var.set(hash_resultado)


def calcular_hash_ficheiro():
    caminho_ficheiro = filedialog.askopenfilename(
        title="Selecionar Ficheiro de Texto",
        filetypes=[("Ficheiros de Texto", "*.txt"), ("Todos os Ficheiros", "*.*")],
    )
    if not caminho_ficheiro:
        return

    try:
        sha256 = hashlib.sha256()
        with open(caminho_ficheiro, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        resultado_var.set(sha256.hexdigest())
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao ler ficheiro: {e}")


# Interface Gráfica
app = tk.Tk()
app.title("Gerador de Hash SHA-256")
app.geometry("550x250")

tk.Label(app, text="Texto Simples:").pack(anchor="w", padx=10, pady=5)
entry_texto = tk.Entry(app, width=60)
entry_texto.pack(padx=10, pady=2)

btn_hash_texto = tk.Button(
    app, text="Calcular Hash do Texto", command=calcular_hash_texto
)
btn_hash_texto.pack(pady=5)

tk.Label(app, text="-- OU --").pack(pady=5)

btn_hash_ficheiro = tk.Button(
    app,
    text="Selecionar Ficheiro de Texto e Calcular Hash",
    command=calcular_hash_ficheiro,
)
btn_hash_ficheiro.pack(pady=5)

resultado_var = tk.StringVar()
tk.Label(app, text="Resultado (SHA-256):").pack(anchor="w", padx=10, pady=5)
entry_resultado = tk.Entry(
    app, textvariable=resultado_var, width=70, state="readonly"
)
entry_resultado.pack(padx=10, pady=2)

app.mainloop()