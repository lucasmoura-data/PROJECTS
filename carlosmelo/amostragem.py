# Importando bibliotecas necessárias
import numpy as np
import matplotlib.pyplot as plt

# Gerando um sinal contínuo (combinação de senoides)
x = np.linspace(0, 4*np.pi, 1000)
y = np.sin(x) + 0.3 * np.sin(3*x) + 0.2 * np.cos(7*x)

# Amostragem: discretização do domínio contínuo
sample_factor = 20
x_sampled = x[::sample_factor]
y_sampled = y[::sample_factor]

# Quantização: redução da resolução em amplitude
num_levels = 8
y_min, y_max = y.min(), y.max()
step = (y_max - y_min) / num_levels
y_quantized = np.floor((y_sampled - y_min) / step) * step + y_min

# Plotando o sinal com amostragem e quantização
plt.figure(figsize=(10, 4))
plt.plot(x, y, label='Sinal Contínuo', alpha=0.75, color='blue')
markerline, stemlines, baseline = plt.stem(x_sampled, y_sampled,
                                          linefmt='r-', markerfmt='ro', basefmt=' ',
                                          label='Amostras')
plt.setp(markerline, alpha=0.2)
plt.setp(stemlines, alpha=0.2)

# Linhas horizontais de quantização
for i in range(num_levels + 1):
    y_line = y_min + i * step
    plt.axhline(y_line, color='gray', linestyle='--', linewidth=0.5, alpha=0.6)

# Linhas verticais de amostragem
for x_tick in x_sampled:
    plt.axvline(x_tick, color='gray', linestyle='--', linewidth=0.5, alpha=0.6)

# Casas de quantização com preenchimento
delta_x = (x[1] - x[0]) * sample_factor
for xi, yi in zip(x_sampled, y_quantized):
    plt.gca().add_patch(plt.Rectangle(
        (xi - delta_x / 2, yi),
        width=delta_x,
        height=step,
        edgecolor='black',
        facecolor='lightgreen',
        linewidth=1.5,
        alpha=0.85
    ))

# Pontos quantizados
plt.scatter(x_sampled, y_quantized, color='green', label='Quantizado')
plt.title("Sinal Amostrado e Quantizado (8 Níveis)")
plt.xlabel("Tempo")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(False)
plt.tight_layout()
plt.show()