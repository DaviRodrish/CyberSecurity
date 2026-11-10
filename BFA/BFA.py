

import itertools
import string
import time

senha = input("Digite a senha para o ataque: ")

caracteres = string.ascii_lowercase + string.digits

tentativas = 0
inicio = time.time()

print("\nIniciando ataque de força bruta...\n")

for tamanho in range(1, len(senha) + 1):

    for combinacao in itertools.product(caracteres, repeat=tamanho):

        tentativa = ''.join(combinacao)
        tentativas += 1

        print(f"Tentativa {tentativas}: {tentativa}", end="\r")

        if tentativa == senha:
            fim = time.time()

            print("\n\nSenha encontrada!")
            print(f"Senha: {tentativa}")
            print(f"Tentativas: {tentativas}")
            print(f"Tempo: {fim - inicio:.2f} segundos")

            exit()

print("Senha não encontrada.")