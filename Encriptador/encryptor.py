import base64
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText
import hashlib

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except Exception as error:
    AESGCM = None
    CRYPTO_ERROR = repr(error)
else:
    CRYPTO_ERROR = None


APP_TITLE = "Máquina de Criptografia"
SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32  # AES-256


def derive_key(password: str, salt: bytes) -> bytes:
    """Deriva uma chave AES-256 a partir da senha usando PBKDF2-HMAC-SHA256."""
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600_000,
        dklen=KEY_SIZE,
    )


def encrypt_bytes(data: bytes, password: str) -> bytes:
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    key = derive_key(password, salt)

    encrypted = AESGCM(key).encrypt(nonce, data, None)

    # Formato:
    # MAGIC(4) + SALT(16) + NONCE(12) + DADOS_CRIPTOGRAFADOS
    return b"CRP1" + salt + nonce + encrypted


def decrypt_bytes(package: bytes, password: str) -> bytes:
    if len(package) < 4 + SALT_SIZE + NONCE_SIZE + 16:
        raise ValueError("O arquivo/dado criptografado é inválido ou está incompleto.")

    if package[:4] != b"CRP1":
        raise ValueError("Formato de criptografia desconhecido.")

    salt_start = 4
    nonce_start = salt_start + SALT_SIZE
    data_start = nonce_start + NONCE_SIZE

    salt = package[salt_start:nonce_start]
    nonce = package[nonce_start:data_start]
    encrypted = package[data_start:]

    key = derive_key(password, salt)

    try:
        return AESGCM(key).decrypt(nonce, encrypted, None)
    except Exception:
        raise ValueError("Não foi possível descriptografar. A senha pode estar incorreta ou os dados foram alterados.")


class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("900x700")
        self.root.minsize(760, 600)

        self.mode = tk.StringVar(value="encrypt")
        self.password = tk.StringVar()
        self.file_path = tk.StringVar(value="Nenhum arquivo selecionado")

        self.build_style()
        self.build_interface()

    def build_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"))
        style.configure("Subtitle.TLabel", font=("Segoe UI", 10))
        style.configure("Big.TButton", font=("Segoe UI", 11, "bold"), padding=10)
        style.configure("Mode.TButton", font=("Segoe UI", 10, "bold"), padding=8)

    def build_interface(self):
        main = ttk.Frame(self.root, padding=20)
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="🔐 Máquina de Criptografia", style="Title.TLabel").pack(
            anchor="w"
        )
        ttk.Label(
            main,
            text="Criptografia de textos e arquivos TXT usando AES-256-GCM.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(2, 18))

        # Modo
        mode_frame = ttk.LabelFrame(main, text="Operação", padding=10)
        mode_frame.pack(fill="x", pady=(0, 12))

        ttk.Radiobutton(
            mode_frame,
            text="🔒 Criptografar",
            variable=self.mode,
            value="encrypt",
            command=self.update_labels,
        ).pack(side="left", padx=10)

        ttk.Radiobutton(
            mode_frame,
            text="🔓 Descriptografar",
            variable=self.mode,
            value="decrypt",
            command=self.update_labels,
        ).pack(side="left", padx=10)

        # Senha
        password_frame = ttk.LabelFrame(main, text="Senha", padding=10)
        password_frame.pack(fill="x", pady=(0, 12))

        password_entry = ttk.Entry(
            password_frame,
            textvariable=self.password,
            show="•",
            font=("Segoe UI", 11),
        )
        password_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

        ttk.Button(
            password_frame,
            text="Mostrar",
            command=self.toggle_password,
        ).pack(side="right")

        self.password_entry = password_entry
        self.password_visible = False

        # Texto
        text_frame = ttk.LabelFrame(main, text="Texto", padding=10)
        text_frame.pack(fill="both", expand=True, pady=(0, 12))

        self.text_area = ScrolledText(
            text_frame,
            wrap=tk.WORD,
            font=("Consolas", 11),
            height=12,
        )
        self.text_area.pack(fill="both", expand=True)

        # Arquivo
        file_frame = ttk.LabelFrame(main, text="Arquivo TXT", padding=10)
        file_frame.pack(fill="x", pady=(0, 12))

        ttk.Label(
            file_frame,
            textvariable=self.file_path,
            anchor="w",
        ).pack(side="left", fill="x", expand=True, padx=(0, 10))

        ttk.Button(
            file_frame,
            text="Selecionar arquivo",
            command=self.select_file,
        ).pack(side="right")

        # Botões
        button_frame = ttk.Frame(main)
        button_frame.pack(fill="x")

        self.action_button = ttk.Button(
            button_frame,
            text="🔒 Criptografar",
            style="Big.TButton",
            command=self.process_text,
        )
        self.action_button.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.file_button = ttk.Button(
            button_frame,
            text="📁 Criptografar arquivo",
            style="Big.TButton",
            command=self.process_file,
        )
        self.file_button.pack(side="left", fill="x", expand=True, padx=6)

        ttk.Button(
            button_frame,
            text="Limpar",
            style="Big.TButton",
            command=self.clear_all,
        ).pack(side="left", fill="x", expand=True, padx=(6, 0))

        ttk.Label(
            main,
            text="Para descriptografar, use a mesma senha utilizada na criptografia.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(12, 0))

    def toggle_password(self):
        self.password_visible = not self.password_visible
        self.password_entry.configure(
            show="" if self.password_visible else "•"
        )

    def update_labels(self):
        if self.mode.get() == "encrypt":
            self.action_button.configure(text="🔒 Criptografar")
            self.file_button.configure(text="📁 Criptografar arquivo")
        else:
            self.action_button.configure(text="🔓 Descriptografar")
            self.file_button.configure(text="📁 Descriptografar arquivo")

    def validate_password(self):
        password = self.password.get()

        if len(password) < 8:
            messagebox.showwarning(
                "Senha fraca",
                "Digite uma senha com pelo menos 8 caracteres.",
            )
            return False

        return True

    def process_text(self):
        if AESGCM is None:
            messagebox.showerror(
            "Erro ao carregar cryptography",
         f"Não foi possível carregar a biblioteca.\n\n"
         f"Erro encontrado:\n{CRYPTO_ERROR}"
        )
        return

        if not self.validate_password():
            return

        text = self.text_area.get("1.0", tk.END).rstrip("\n")

        if not text:
            messagebox.showwarning(
                "Texto vazio",
                "Digite um texto para continuar.",
            )
            return

        try:
            if self.mode.get() == "encrypt":
                encrypted = encrypt_bytes(
                    text.encode("utf-8"),
                    self.password.get(),
                )

                # Base64 torna o resultado adequado para exibição em texto.
                result = base64.b64encode(encrypted).decode("ascii")

                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", result)

                messagebox.showinfo(
                    "Sucesso",
                    "Texto criptografado com sucesso.",
                )

            else:
                try:
                    package = base64.b64decode(text.encode("ascii"), validate=True)
                except Exception:
                    raise ValueError(
                        "O texto não está em um formato criptografado válido."
                    )

                decrypted = decrypt_bytes(
                    package,
                    self.password.get(),
                )

                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", decrypted.decode("utf-8"))

                messagebox.showinfo(
                    "Sucesso",
                    "Texto descriptografado com sucesso.",
                )

        except UnicodeDecodeError:
            messagebox.showerror(
                "Erro",
                "O conteúdo descriptografado não é um texto UTF-8 válido.",
            )
        except ValueError as error:
            messagebox.showerror("Erro", str(error))
        except Exception as error:
            messagebox.showerror(
                "Erro inesperado",
                f"Ocorreu um erro:\n{error}",
            )

    def select_file(self):
        path = filedialog.askopenfilename(
            title="Selecionar arquivo",
            filetypes=[
                ("Arquivos TXT", "*.txt"),
                ("Arquivos criptografados", "*.enc"),
                ("Todos os arquivos", "*.*"),
            ],
        )

        if path:
            self.file_path.set(path)

    def process_file(self):
        if AESGCM is None:
            self.show_install_error()
            return

        if not self.validate_password():
            return

        path = self.file_path.get()

        if path == "Nenhum arquivo selecionado":
            messagebox.showwarning(
                "Arquivo",
                "Selecione um arquivo primeiro.",
            )
            return

        try:
            with open(path, "rb") as file:
                data = file.read()

            if self.mode.get() == "encrypt":
                result = encrypt_bytes(data, self.password.get())

                default_name = os.path.splitext(path)[0] + ".enc"

                output_path = filedialog.asksaveasfilename(
                    title="Salvar arquivo criptografado",
                    initialfile=os.path.basename(default_name),
                    defaultextension=".enc",
                    filetypes=[
                        ("Arquivo criptografado", "*.enc"),
                        ("Todos os arquivos", "*.*"),
                    ],
                )

            else:
                result = decrypt_bytes(data, self.password.get())

                # Tenta remover .enc; caso não tenha, adiciona _descriptografado.
                if path.lower().endswith(".enc"):
                    default_name = path[:-4]
                else:
                    default_name = os.path.splitext(path)[0] + "_descriptografado.txt"

                output_path = filedialog.asksaveasfilename(
                    title="Salvar arquivo descriptografado",
                    initialfile=os.path.basename(default_name),
                    defaultextension=".txt",
                    filetypes=[
                        ("Arquivo TXT", "*.txt"),
                        ("Todos os arquivos", "*.*"),
                    ],
                )

            if not output_path:
                return

            with open(output_path, "wb") as file:
                file.write(result)

            messagebox.showinfo(
                "Sucesso",
                f"Arquivo processado com sucesso!\n\nSalvo em:\n{output_path}",
            )

        except ValueError as error:
            messagebox.showerror("Erro", str(error))
        except PermissionError:
            messagebox.showerror(
                "Erro",
                "Não foi possível acessar o arquivo. Verifique as permissões.",
            )
        except Exception as error:
            messagebox.showerror(
                "Erro inesperado",
                f"Ocorreu um erro:\n{error}",
            )

    def clear_all(self):
        self.text_area.delete("1.0", tk.END)
        self.password.set("")
        self.file_path.set("Nenhum arquivo selecionado")

    @staticmethod
    def show_install_error():
        messagebox.showerror(
            "Biblioteca ausente",
            "A biblioteca 'cryptography' não está instalada.\n\n"
            "Abra o terminal e execute:\n\n"
            "pip install cryptography",
        )


def main():
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
