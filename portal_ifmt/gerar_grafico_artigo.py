import matplotlib.pyplot as plt
import numpy as np

tempos_historico = np.array([0, 5, 10, 15, 20])
cpu_historico = np.array([62, 68, 77, 81, 89])

m, b = np.polyfit(tempos_historico, cpu_historico, 1)

tempos_futuro = np.array([0, 5, 10, 15, 20, 25, 30])
cpu_projetada = m * tempos_futuro + b

limite_critico = 95
tempo_critico = (limite_critico - b) / m

plt.style.use('dark_background')
plt.figure(figsize=(10, 6))

plt.scatter(tempos_historico, cpu_historico, color='#00ffcc', s=100, label='Coletas Reais (Zabbix)', zorder=5)
plt.plot(tempos_futuro, cpu_projetada, color='#ff00ff', linestyle='--', linewidth=2, label=f'Tendência Linear (y = {m:.2f}x + {b:.2f})')
plt.axhline(y=limite_critico, color='#ff3333', linestyle='-', linewidth=2, label='Limite Crítico (95%)')
plt.scatter([tempo_critico], [limite_critico], color='#ff3333', s=150, marker='X', zorder=6, label=f'Colapso Estimado ({tempo_critico:.1f} min)')

plt.title('Motor Preditivo: Projeção de Esgotamento de CPU', fontsize=14, pad=15)
plt.xlabel('Tempo (Minutos)', fontsize=12)
plt.ylabel('Consumo de CPU (%)', fontsize=12)
plt.ylim(50, 105)
plt.xlim(-1, 32)
plt.grid(True, linestyle=':', alpha=0.3)
plt.legend(loc='lower right', fontsize=10)

plt.savefig('grafico_regressao_cpu.png', dpi=300, bbox_inches='tight')
print("Gráfico gerado com sucesso: grafico_regressao_cpu.png")