from datetime import datetime, timedelta

def main():
    print("===================================")
    print("   Gestão da Barbearia (2 barbeiros)")
    print("===================================\n")

    BARBEIROS = ["Jhony", "Breno"]
    PRECOS = {
        "corte": 50,
        "barba": 20,
        "bigode": 10,
        "sobrancelha": 10
    }

    DURACAO = {
        "corte": 30,
        "barba": 15,
        "bigode": 15,
        "sobrancelha": 15
    }

    total_pessoas = 0
    total_servicos_prestados = 0
    total_recebido = 0

    ganhos = {b: 0 for b in BARBEIROS}

    relatorio_servicos = {s: {"qtd": 0, "valor": 0} for s in PRECOS.keys()}

    agenda = []

    def parse_horario(h):
        # Espera formato HH:MM (ex: 14:30)
        return datetime.strptime(h, "%H:%M")

    def calcular_fim(horario_inicio, servicos):
        dur_total = sum(DURACAO[s] for s in servicos)
        return horario_inicio + timedelta(minutes=dur_total)

    def sobrepoe(item_a, item_b):
        """
        Verifica sobreposição em linha do tempo [inicio, fim).
        Se uma termina no exato momento que a outra começa, não sobrepõe.
        """
        return (item_a["inicio"] < item_b["fim"]) and (item_b["inicio"] < item_a["fim"])

    def barbeiro_ocupado(barbeiro, inicio, fim):
        tentativa = {"barbeiro": barbeiro, "inicio": inicio, "fim": fim}
        for ag in agenda:
            if ag["barbeiro"] == barbeiro and sobrepoe(tentativa, ag):
                return True
        return False

    def pedir_servicos():
        servicos_cliente = []
        print("\nEscolha os serviços desejados:")

        for servico in PRECOS.keys():
            opcao = input(f"Quer '{servico}'? (s/n): ").strip().lower()
            if opcao == "s":
                servicos_cliente.append(servico)
        return servicos_cliente

    while True:
        print("\n--- Novo cliente ---")
        nome = input("Digite o nome do cliente (ou 'sair' para finalizar): ").strip()
        if nome.lower() == "sair":
            break

        horario_str = input("Digite o horário de atendimento (ex: 14:30): ").strip()
        try:
            horario_inicio = parse_horario(horario_str)
        except ValueError:
            print(" Horário inválido. Use o formato HH:MM (ex: 14:30). Tente novamente.")
            continue

        while True:
            barbeiro = input("Escolha o barbeiro (Jhony ou Breno): ").strip()
            if barbeiro in BARBEIROS:
                break
            print(" Barbeiro inválido. Tente novamente.")

        servicos_cliente = pedir_servicos()
        if not servicos_cliente:
            print(" Nenhum serviço selecionado. Este cliente não será contabilizado.")
            continue

        # Calcula fim com base nos serviços escolhidos
        fim = calcular_fim(horario_inicio, servicos_cliente)

        # Impede sobreposição real para o mesmo barbeiro
        while barbeiro_ocupado(barbeiro, horario_inicio, fim):
            print(f" O barbeiro {barbeiro} está ocupado nesse período.")
            horario_str = input("Digite outro horário de início (ex: 15:00): ").strip()
            try:
                horario_inicio = parse_horario(horario_str)
            except ValueError:
                print(" Horário inválido. Use HH:MM. Tente novamente.")
                continue

            fim = calcular_fim(horario_inicio, servicos_cliente)

        # Cálculo financeiro
        valor_cliente = sum(PRECOS[s] for s in servicos_cliente)
        total_pessoas += 1
        total_servicos_prestados += len(servicos_cliente)
        total_recebido += valor_cliente
        ganhos[barbeiro] += valor_cliente

        # Atualiza relatório por serviço
        for s in servicos_cliente:
            relatorio_servicos[s]["qtd"] += 1
            relatorio_servicos[s]["valor"] += PRECOS[s]

        # Registra na agenda
        agenda.append({
            "nome": nome,
            "barbeiro": barbeiro,
            "inicio": horario_inicio,
            "fim": fim,
            "servicos": servicos_cliente,
            "valor": valor_cliente
        })

        print("\n Cliente atendido/agendado com sucesso!")
        print(f" Início: {horario_inicio.strftime('%H:%M')}")
        print(f" Fim: {fim.strftime('%H:%M')}")
        print(f" Barbeiro: {barbeiro}")
        print(f" Serviços: {', '.join(servicos_cliente)}")
        print(f" Valor do cliente: R$ {valor_cliente:.2f}")

    # Ordena agenda por início
    agenda.sort(key=lambda x: x["inicio"])

    print("\n\n===================================")
    print("         RESUMO DO DIA")
    print("===================================")

    if agenda:
        print("\n Atendimentos:")
        for item in agenda:
            ini = item["inicio"].strftime("%H:%M")
            fim = item["fim"].strftime("%H:%M")
            print(
                f"- {ini}-{fim} | {item['nome']} | {item['barbeiro']} | "
                f"Serviços: {', '.join(item['servicos'])} | Total: R$ {item['valor']:.2f}"
            )
    else:
        print("\nNenhum cliente foi atendido no dia.")

    # Estatísticas finais
    print("\n Resultados gerais:")
    print(f" Pessoas atendidas: {total_pessoas}")
    print(f" Serviços prestados (quantidade): {total_servicos_prestados}")
    print(f" Valor total arrecadado: R$ {total_recebido:.2f}")

    print("\n Ganhos por barbeiro:")
    for b in BARBEIROS:
        print(f"- {b}: R$ {ganhos[b]:.2f}")

    # Relatório por tipo de serviço
    print("\n Relatório por tipo de serviço:")
    for s in PRECOS.keys():
        qtd = relatorio_servicos[s]["qtd"]
        val = relatorio_servicos[s]["valor"]
        print(f"- {s}: {qtd} serviço(ões) | faturamento: R$ {val:.2f}")

if __name__ == "__main__":
    main()