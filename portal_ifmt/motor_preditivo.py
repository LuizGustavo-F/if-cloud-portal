import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor

class MotorPreditivo:
    """
    IA Estatística e Machine Learning
    Utiliza Regressão Linear Simples, KNN e Random Forest para prever o esgotamento
    de recursos computacionais (CPU e RAM) com base no histórico do Zabbix.
    """

    def __init__(self, limite_critico=95.0):
        self.limite_critico = limite_critico

    def _calcular_regressao_linear(self, historico):
        """
        Aplica a fórmula matemática da Regressão Linear (y = mx + b) manualmente.
        """
        n = len(historico)
        if n < 2:
            return 0, 0

        x = list(range(n))
        y = historico

        sum_x = sum(x)
        sum_y = sum(y)
        sum_x_quadrado = sum([i**2 for i in x])
        sum_xy = sum([x[i] * y[i] for i in range(n)])

        denominador = (n * sum_x_quadrado) - (sum_x ** 2)
        
        if denominador == 0:
            return 0, sum_y / n

        m = ((n * sum_xy) - (sum_x * sum_y)) / denominador
        b = (sum_y - (m * sum_x)) / n

        return m, b

    def comparar_modelos(self, historico):
        """
        Realiza o benchmarking entre a Regressão Linear, KNN e Random Forest.
        Treina os 3 modelos com o histórico e tenta prever qual será o próximo valor de consumo.
        """
        if not historico or len(historico) < 3:
            return "Dados insuficientes para comparação."

        n = len(historico)
        
        # Preparando os dados no formato que o Scikit-Learn exige (Matrizes 2D)
        X_treino = np.array(range(n)).reshape(-1, 1) # [ [0], [1], [2], [3], [4] ]
        y_treino = np.array(historico)               # [ 60, 70, 80, 90, 95 ]
        
        # Ponto no futuro que queremos prever (o próximo passo imediato)
        X_futuro = np.array([[n]])

        # 1. Regressão Linear (Scikit-Learn)
        modelo_lr = LinearRegression()
        modelo_lr.fit(X_treino, y_treino)
        pred_lr = modelo_lr.predict(X_futuro)[0]

        # 2. K-Nearest Neighbors (KNN)
        # Usamos n_neighbors=2 pois nossa janela do Zabbix é pequena (ex: 5 pontos)
        modelo_knn = KNeighborsRegressor(n_neighbors=2)
        modelo_knn.fit(X_treino, y_treino)
        pred_knn = modelo_knn.predict(X_futuro)[0]

        # 3. Random Forest
        modelo_rf = RandomForestRegressor(n_estimators=100, random_state=42)
        modelo_rf.fit(X_treino, y_treino)
        pred_rf = modelo_rf.predict(X_futuro)[0]

        print(f"--- BENCHMARKING DE IA ---")
        print(f"Histórico Recebido: {historico}")
        print(f"Previsão Regressão Linear: {pred_lr:.2f}%")
        print(f"Previsão KNN:              {pred_knn:.2f}%")
        print(f"Previsão Random Forest:    {pred_rf:.2f}%")
        print(f"--------------------------")

        return pred_lr, pred_knn, pred_rf

    def analisar_metrica(self, nome_metrica, historico, intervalo_minutos=5):
        """
        Analisa a lista de histórico e devolve um parecer da IA (Usando a Regressão Linear padrão).
        """
        if not historico or len(historico) < 3:
            return {"status": "normal", "mensagem": "Dados insuficientes para previsão."}

        m, b = self._calcular_regressao_linear(historico)
        valor_atual = historico[-1]

        if m <= 0:
            if valor_atual >= self.limite_critico:
                return {"status": "critico", "mensagem": f"{nome_metrica} já excedeu {self.limite_critico}%!"}
            return {"status": "normal", "mensagem": "Consumo estável ou em declínio."}

        passo_critico = (self.limite_critico - b) / m
        passo_atual = len(historico) - 1
        
        passos_restantes = passo_critico - passo_atual

        if passos_restantes <= 0:
            return {"status": "critico", "mensagem": f"{nome_metrica} em sobrecarga iminente ou atual!"}

        minutos_restantes = int(passos_restantes * intervalo_minutos)

        if minutos_restantes < 30:
            return {"status": "critico", "mensagem": f"⚠️ Risco de esgotamento de {nome_metrica} em ~{minutos_restantes} min!"}
        elif minutos_restantes <= 120:
            return {"status": "alerta", "mensagem": f"📈 Tendência de alta. {nome_metrica} no limite em ~{minutos_restantes} min."}
        else:
            return {"status": "normal", "mensagem": "Consumo a crescer, mas dentro de níveis seguros."}

    def avaliar_maquina(self, historico_cpu, historico_ram):
        # ... MANTÉM IGUAL AO SEU ORIGINAL ...
        analise_cpu = self.analisar_metrica("CPU", historico_cpu)
        analise_ram = self.analisar_metrica("RAM", historico_ram)

        if analise_cpu['status'] == 'critico' or analise_ram['status'] == 'critico':
            status_geral = 'critico'
            msg = analise_cpu['mensagem'] if analise_cpu['status'] == 'critico' else analise_ram['mensagem']
        elif analise_cpu['status'] == 'alerta' or analise_ram['status'] == 'alerta':
            status_geral = 'alerta'
            msg = analise_cpu['mensagem'] if analise_cpu['status'] == 'alerta' else analise_ram['mensagem']
        else:
            status_geral = 'normal'
            msg = "Sistema Saudável."

        return {
            "status_ia": status_geral,
            "mensagem_ia": msg,
            "detalhes": {
                "cpu": analise_cpu,
                "ram": analise_ram
            }
        }