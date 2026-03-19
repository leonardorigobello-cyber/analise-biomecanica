import matplotlib.pyplot as plt

def gerar_grafico(df, coluna):
    plt.figure()
    df[coluna].plot()
    plt.title(f"Evolucao de {coluna}")
    plt.savefig(f"output/{coluna}.png")
    plt.close()