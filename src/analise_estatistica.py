import numpy as np

def calcular_estatisticas(df):
    resultados = {}

    for coluna in df.select_dtypes(include=[np.number]).columns:
        resultados[coluna] = {
            "media": df[coluna].mean(),
            "desvio": df[coluna].std(),
            "max": df[coluna].max(),
            "min": df[coluna].min()
        }

    return resultados