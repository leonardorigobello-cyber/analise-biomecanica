import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from fpdf import FPDF

# =========================
# Caminhos do projeto
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

output_path = os.path.join(BASE_DIR, "output")
graficos_path = os.path.join(output_path, "graficos")
relatorios_path = os.path.join(output_path, "relatorios")
arquivo = os.path.join(BASE_DIR, "data", "Resultados 1200.xlsx")

os.makedirs(graficos_path, exist_ok=True)
os.makedirs(relatorios_path, exist_ok=True)

print("📂 Lendo arquivo:", arquivo)
df = pd.read_excel(arquivo, header=None)

print("\nArquivo original:")
print(df)

# ----------------------------
# pegar grupos da primeira linha
# ----------------------------
grupos = df.iloc[0,1:]

# ----------------------------
# pegar variáveis
# ----------------------------
variaveis = df.iloc[2:9,0]
dados = df.iloc[2:9,1:]

dados = dados.replace("x", np.nan)
dados = dados.apply(pd.to_numeric, errors="coerce")

dados = dados.T
dados.columns = variaveis
dados["Grupo"] = grupos.values
dados = dados.dropna(axis=1, how="all")

print("\nDados organizados:")
print(dados)

variaveis = dados.columns[:-1]

# ----------------------------
# regressão
# ----------------------------
def regressao(valores):
    y = np.array(valores)
    mask = ~np.isnan(y)
    y = y[mask]

    if len(y) < 2:
        return "Dados insuficientes"

    x = np.arange(len(y)).reshape(-1,1)
    modelo = LinearRegression().fit(x,y)
    r2 = modelo.score(x,y)
    return f"R² = {r2:.3f}"

# ----------------------------
# maior e menor valor
# ----------------------------
def maior_menor_valor(var):
    maior = dados[var].max()
    menor = dados[var].min()

    grupo_maior = dados[dados[var] == maior]["Grupo"].values[0]
    grupo_menor = dados[dados[var] == menor]["Grupo"].values[0]

    return maior, grupo_maior, menor, grupo_menor

# ----------------------------
# gráficos
# ----------------------------
for var in variaveis:

    plt.figure(figsize=(8,6))
    sns.barplot(
        data=dados,
        x="Grupo",
        y=var,
        hue="Grupo",
        legend=False,
        palette="viridis"
    )
    plt.xticks(rotation=90)
    plt.title(str(var))
    plt.tight_layout()
    plt.savefig(os.path.join(graficos_path, f"{var}.png"))
    plt.close()

    valores = dados[["Grupo", var]].dropna(subset=[var])

    if len(valores) < 2:
        continue

    grupos_unicos = valores["Grupo"].values
    valores_num = valores[var].values

    matriz = np.abs(valores_num[:, None] - valores_num[None, :])

    plt.figure(figsize=(12,10))
    sns.heatmap(
        matriz,
        annot=True,
        cmap="viridis",
        xticklabels=grupos_unicos,
        yticklabels=grupos_unicos,
        fmt=".2f",
        annot_kws={"size":8},
        square=True,
        cbar_kws={"label": var}
    )

    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.title(f"Heatmap - {var}")
    plt.tight_layout()
    plt.savefig(os.path.join(graficos_path, f"heatmap_{var}.png"))
    plt.close()

# ----------------------------
# relatório
# ----------------------------
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial","B",16)
pdf.cell(0,10,"Relatorio Biomecanico",0,1,"C")
pdf.ln(10)

for var in variaveis:
    valores = dados[var].values

    media = np.nanmean(valores)
    desvio = np.nanstd(valores)
    minimo = np.nanmin(valores)
    maximo = np.nanmax(valores)

    r2 = regressao(valores)
    maior, grupo_maior, menor, grupo_menor = maior_menor_valor(var)

    pdf.set_font("Arial","B",12)
    pdf.cell(0,10,str(var),0,1)

    pdf.set_font("Arial","",11)
    pdf.cell(0,8,f"Media: {media:.2f}",0,1)
    pdf.cell(0,8,f"Desvio: {desvio:.2f}",0,1)
    pdf.cell(0,8,f"Min: {minimo:.2f}",0,1)
    pdf.cell(0,8,f"Max: {maximo:.2f}",0,1)
    pdf.cell(0,8,f"Regressao ML: {r2}",0,1)
    pdf.cell(0,8,f"Maior valor: {grupo_maior} ({maior:.2f})",0,1)
    pdf.cell(0,8,f"Menor valor: {grupo_menor} ({menor:.2f})",0,1)

    pdf.image(os.path.join(graficos_path, f"{var}.png"), w=120)

    heatmap_path = os.path.join(graficos_path, f"heatmap_{var}.png")
    if os.path.exists(heatmap_path):
        pdf.ln(5)
        pdf.image(heatmap_path, w=120)

    pdf.ln(10)

pdf.output(os.path.join(relatorios_path, "relatorio_biomecanica.pdf"))

print("\n✅ Relatório gerado com sucesso!")