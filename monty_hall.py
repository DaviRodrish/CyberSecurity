
import random

def monty_hall(n):
    vitorias_manter = 0
    vitorias_trocar = 0

    for _ in range(n):
        # Sorteia a porta que contém o prêmio
        premio = random.randint(1, 3)

        # O participante escolhe uma porta
        escolha = random.randint(1, 3)

        # O apresentador abre uma porta sem prêmio,
        # diferente da porta escolhida
        portas_disponiveis = [
            porta for porta in range(1, 4)
            if porta != premio and porta != escolha
        ]

        porta_aberta = random.choice(portas_disponiveis)

        # Estratégia 1: manter a escolha inicial
        if escolha == premio:
            vitorias_manter += 1

        # Estratégia 2: trocar de porta
        porta_trocada = [
            porta for porta in range(1, 4)
            if porta != escolha and porta != porta_aberta
        ][0]

        if porta_trocada == premio:
            vitorias_trocar += 1

    # Exibe os resultados
    print(f"Número de simulações: {n}\n")

    print("--- MANTER A PORTA ---")
    print(f"Vitórias: {vitorias_manter}")
    print(f"Derrotas: {n - vitorias_manter}")
    print(
        f"Taxa de vitória: "
        f"{vitorias_manter / n * 100:.2f}%"
    )

    print("\n--- TROCAR DE PORTA ---")
    print(f"Vitórias: {vitorias_trocar}")
    print(f"Derrotas: {n - vitorias_trocar}")
    print(
        f"Taxa de vitória: "
        f"{vitorias_trocar / n * 100:.2f}%"
    )


# Executa 10.000 simulações
monty_hall(100000)
