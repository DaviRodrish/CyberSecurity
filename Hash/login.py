import tkinter as tk
from tkinter import messagebox
import pyotp

# Credenciais e chave secreta TOTP simuladas (em produção seriam guardadas na base de dados)
UTILIZADOR_CORRETO = "admin"
SENHA_CORRETA = "seguranca123"
# Chave secreta Base32 para TOTP
CHAVE_SECRETA_2FA = pyotp.random_base32()


def verificar_login():
    utilizador = entry_user.get()
    senha = entry_pass.get()
    codigo_2fa = entry_2fa.get()

    if utilizador != UTILIZADOR_CORRETO or senha != SENHA_CORRETA:
        messagebox.showerror(
            "Erro de Autenticação", "Utilizador ou palavra-passe incorretos."
        )
        return

    # Validação do segundo fator (TOTP)
    totp = pyotp.TOTP(CHAVE_SECRETA_2FA)
    if totp.verify(codigo_2fa):
        messagebox.showinfo(
            "Sucesso", "Login multifator efetuado com sucesso!"
        )
    else:
        messagebox.showerror(
            "Erro 2FA", "Código de autenticação de 2 fatores inválido ou expirado."
        )


# Interface Gráfica
app = tk.Tk()
app.title("Sistema de Login Multifator (2FA)")
app.geometry("400x320")

tk.Label(app, text="Utilizador:").pack(anchor="w", padx=20, pady=5)
entry_user = tk.Entry(app, width=30)
entry_user.pack(padx=20, pady=2)

tk.Label(app, text="Palavra-passe:").pack(anchor="w", padx=20, pady=5)
entry_pass = tk.Entry(app, show="*", width=30)
entry_pass.pack(padx=20, pady=2)

# Exibe a chave de demonstração para configurar o autenticador
totp_demo = pyotp.TOTP(CHAVE_SECRETA_2FA)
tk.Label(
    app,
    text=f"[Demo] Chave Secret 2FA: {CHAVE_SECRETA_2FA}\n[Demo] Código Atual: {totp_demo.now()}",
    fg="gray",
).pack(pady=10)

tk.Label(app, text="Código 2FA (6 dígitos):").pack(
    anchor="w", padx=20, pady=5
)
entry_2fa = tk.Entry(app, width=30)
entry_2fa.pack(padx=20, pady=2)

btn_login = tk.Button(
    app, text="Entrar", command=verificar_login, bg="#4CAF50", fg="white"
)
btn_login.pack(pady=15)

app.mainloop()