class MotorInferenciaOpenStack:
    def __init__(self):
        # predefinição no microstack
        self.flavors = {
            "m1.tiny": {"ram": 512, "vcpus": 1, "disk": 1},
            "if.small": {"ram": 2048, "vcpus": 1, "disk": 20},
            "m1.medium": {"ram": 4096, "vcpus": 2, "disk": 20},
            "m1.large": {"ram": 8192, "vcpus": 4, "disk": 20}
        }

    def avaliar_necessidade(self, aplicacao, carga):
        """
        Aplica as regras lógicas do Sistema Especialista (SE... ENTÃO)
        """
        if aplicacao == "machine_learning":
            return self._gerar_resposta("m1.large", "Modelos de IA exigem alta capacidade de processamento e memória para treinamento.")

        if aplicacao in ["site_estatico", "trabalho_academico"]:
            if carga == "alta":
                return self._gerar_resposta("if.small", "Sites com alto tráfego precisam de um pouco mais de RAM para não travar o servidor web.")
            else:
                return self._gerar_resposta("m1.tiny", "Para sites simples em HTML/CSS e poucos acessos, a configuração mínima é suficiente e economiza recursos do IF Cloud.")

        if aplicacao == "banco_de_dados":
            if carga == "alta":
                return self._gerar_resposta("m1.medium", "Bancos de dados com muitas requisições simultâneas precisam de mais núcleos de CPU e RAM para manter a performance.")
            else:
                return self._gerar_resposta("if.small", "Para bancos de dados em desenvolvimento, 2GB de RAM garantem que o serviço rode sem gargalos.")

        # REGRA 4: Backend e APIs (Ex: Django, Node.js)
        if aplicacao == "backend":
            if carga == "baixa":
                return self._gerar_resposta("if.small", "Sua API rodará confortavelmente com a configuração padrão.")
            else:
                return self._gerar_resposta("m1.medium", "Para aguentar picos de tráfego na sua API, alocamos mais vCPUs.")

        # Fallback (Regra padrão de segurança)
        return self._gerar_resposta("if.small", "Configuração balanceada recomendada como padrão para uso geral.")

    def _gerar_resposta(self, flavor_id, justificativa):
        specs = self.flavors[flavor_id]
        return {
            "flavor_recomendado": flavor_id,
            "especificacoes": f"{specs['vcpus']} vCPUs, {specs['ram']}MB RAM, {specs['disk']}GB Disco",
            "justificativa_da_ia": justificativa
        }