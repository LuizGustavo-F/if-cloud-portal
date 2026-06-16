import csv
from sklearn.metrics import accuracy_score, precision_score, recall_score

class MotorPreditivo:
    def __init__(self, limite_critico=95.0):
        self.limite_critico = limite_critico

    def _calcular_regressao_linear(self, historico):
        n = len(historico)
        if n < 2: return 0, 0
        x = list(range(n))
        y = historico
        sum_x = sum(x)
        sum_y = sum(y)
        sum_x_quadrado = sum([i**2 for i in x])
        sum_xy = sum([x[i] * y[i] for i in range(n)])
        denominador = (n * sum_x_quadrado) - (sum_x ** 2)
        if denominador == 0: return 0, sum_y / n
        m = ((n * sum_xy) - (sum_x * sum_y)) / denominador
        b = (sum_y - (m * sum_x)) / n
        return m, b

    def analisar_metrica(self, nome_metrica, historico, intervalo_minutos=5):
        if not historico or len(historico) < 3:
            return {"status": "normal"}
        m, b = self._calcular_regressao_linear(historico)
        valor_atual = historico[-1]
        
        if m <= 0:
            if valor_atual >= self.limite_critico:
                return {"status": "critico"}
            return {"status": "normal"}
            
        passo_critico = (self.limite_critico - b) / m
        passo_atual = len(historico) - 1
        passos_restantes = passo_critico - passo_atual
        
        if passos_restantes <= 0:
            return {"status": "critico"}
            
        minutos_restantes = int(passos_restantes * intervalo_minutos)
        
        if minutos_restantes < 30:
            return {"status": "critico"}
        elif minutos_restantes <= 120:
            return {"status": "alerta"}
        else:
            return {"status": "normal"}


def executar_avaliacao():
    ia = MotorPreditivo()
    
    gabarito_real = []
    previsoes_da_ia = []
    
    print("Iniciando leitura do dataset_zabbix.csv...")
    print("-" * 50)
    
    try:
        with open('dataset_zabbix.csv', mode='r') as arquivo:
            leitor_csv = csv.DictReader(arquivo)
            
            for linha in leitor_csv:
                status_verdadeiro = int(linha['status_real'])
                gabarito_real.append(status_verdadeiro)
                
                historico_cpu = [
                    float(linha['t0']), float(linha['t1']), 
                    float(linha['t2']), float(linha['t3']), float(linha['t4'])
                ]
                
                resultado_ia = ia.analisar_metrica("CPU", historico_cpu)
                
                if resultado_ia['status'] in ['alerta', 'critico']:
                    previsoes_da_ia.append(1)
                else:
                    previsoes_da_ia.append(0)
                    
    except FileNotFoundError:
        print("ERRO: O arquivo 'dataset_zabbix.csv' não foi encontrado na mesma pasta.")
        return

    acuracia = accuracy_score(gabarito_real, previsoes_da_ia)
    precisao = precision_score(gabarito_real, previsoes_da_ia)
    recall = recall_score(gabarito_real, previsoes_da_ia)
    
    print("✅ Avaliação concluída com sucesso!")
    print("\n📊 RESULTADOS OFICIAIS DO MOTOR PREDITIVO (IF CLOUD)")
    print("=" * 50)
    print(f"Total de Máquinas Analisadas: {len(gabarito_real)}")
    print(f"Acurácia Geral: {acuracia * 100:.1f}%  (Acertos totais)")
    print(f"Precisão:       {precisao * 100:.1f}%  (Quando avisou de perigo, era real?)")
    print(f"Recall:         {recall * 100:.1f}%  (Deixou passar alguma máquina que ia cair?)")
    print("=" * 50)

if __name__ == "__main__":
    executar_avaliacao()