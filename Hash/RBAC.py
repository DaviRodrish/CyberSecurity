import datetime

class SimuladorRBAC:
    def __init__(self):
        # Cadastro de papéis e suas respectivas permissões
        self.papeis = {
            "Medico": ["ler_prontuario", "editar_prontuario", "agendar_consulta", "emitir_receita"],
            "Enfermeiro": ["ler_prontuario", "editar_prontuario", "agendar_consulta"],
            "Recepcionista": ["agendar_consulta"]
        }
        
        # Cadastro de usuários vinculados a um ou mais papéis
        self.usuarios = {
            "Dr. House": ["Medico"],
            "Enf. Joy": ["Enfermeiro"],
            "Ana Recepcao": ["Recepcionista"],
            "Dr. Miller": ["Medico", "Enfermeiro"] # Exemplo de usuário com múltiplos papéis
        }
        
        # Log de tentativas de acesso (lista)
        self.logs = []

    def verificar_acesso(self, usuario, recurso, acao):
        """
        Função VerificarAcesso(usuario, recurso, acao) que retorna se 
        o acesso deve ser concedido ou negado.
        Para simplificar, a 'acao' representa diretamente a permissão (ex: 'ler_prontuario').
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "NEGADO"
        
        # Verifica se o usuário existe
        if usuario in self.usuarios:
            papeis_usuario = self.usuarios[usuario]
            # Verifica se algum dos papéis do usuário possui a permissão solicitada
            for papel in papeis_usuario:
                permissoes = self.papeis.get(papel, [])
                if acao in permissoes:
                    status = "CONCEDIDO"
                    break

        # Registra a tentativa no log (lista)
        log_entry = {
            "timestamp": timestamp,
            "usuario": usuario,
            "recurso": recurso,
            "acao": acao,
            "status": status
        }
        self.logs.append(log_entry)
        
        return status == "CONCEDIDO"

    def exibir_logs(self):
        print("\n--- LOG DE TENTATIVAS DE ACESSO ---")
        for i, log in enumerate(self.logs, 1):
            print(f"[{i}] {log['timestamp']} | Usuário: {log['usuario']} | Recurso: {log['recurso']} | Ação: {log['acao']} -> Status: {log['status']}")

# --- Cenário de Teste (Simulando pelo menos 5 tentativas) ---
if __name__ == "__main__":
    sistema = SimuladorRBAC()

    print("Iniciando simulação de cenários de acesso no hospital...\n")

    # 1. Médico tentando emitir receita (Válido - Concedido)
    sistema.verificar_acesso("Dr. House", "Prontuario_01", "emitir_receita")

    # 2. Recepcionista tentando editar prontuário (Inválido - Negado)
    sistema.verificar_acesso("Ana Recepcao", "Prontuario_02", "editar_prontuario")

    # 3. Enfermeiro tentando ler prontuário (Válido - Concedido)
    sistema.verificar_acesso("Enf. Joy", "Prontuario_03", "ler_prontuario")

    # 4. Recepcionista tentando agendar consulta (Válido - Concedido)
    sistema.verificar_acesso("Ana Recepcao", "Agenda_Hospital", "agendar_consulta")

    # 5. Enfermeiro tentando emitir receita - ação restrita a médicos (Inválido - Negado)
    sistema.verificar_acesso("Enf. Joy", "Prontuario_01", "emitir_receita")

    # Exibe todos os registros de log acumulados
    sistema.exibir_logs()