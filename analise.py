import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from fpdf import FPDF

# criar pastas se não existirem
os.makedirs("graficos", exist_ok=True)
os.makedirs("relatorios", exist_ok=True)

arquivo = "Resultados.xlsx"

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

# substituir "x" por NaN
dados = dados.replace("x", np.nan)

# converter para número
dados = dados.apply(pd.to_numeric, errors="coerce")

# ----------------------------
# transpor tabela
# ----------------------------
dados = dados.T
dados.columns = variaveis
dados["Grupo"] = grupos.values

# remover colunas totalmente vazias
dados = dados.dropna(axis=1, how="all")

print("\nDados organizados:")
print(dados)

variaveis = dados.columns[:-1]

# ----------------------------
# função regressão
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
# Função para encontrar maior e menor valor
# ----------------------------
def maior_menor_valor(var):
    maior = dados[var].max()
    menor = dados[var].min()

    grupo_maior = dados[dados[var] == maior]["Grupo"].values[0]
    grupo_menor = dados[dados[var] == menor]["Grupo"].values[0]

    return maior, grupo_maior, menor, grupo_menor

# ----------------------------
# gerar gráficos e heatmaps
# ----------------------------
for var in variaveis:

    # ----------------------------
    # gráfico de barras
    # ----------------------------
    plt.figure(figsize=(8,6))  # Aumentando a figura para maior nitidez
    ax = sns.barplot(
        data=dados,
        x="Grupo",
        y=var,
        hue="Grupo",
        legend=False,
        palette="viridis"
    )
    plt.xticks(rotation=90)
    plt.title(str(var))

    # Não adicionando os valores dentro das barras, deixando o gráfico mais limpo
    plt.tight_layout()
    plt.savefig(f"graficos/{var}.png")
    plt.close()

    # ----------------------------
    # HEATMAP ENTRE GRUPOS (ORGANIZADO)
    # ----------------------------
    valores = dados[["Grupo", var]].dropna(subset=[var])

    if len(valores) < 2:
        print(f"⚠ Pulando heatmap de {var}: dados insuficientes")
        continue

    grupos_unicos = valores["Grupo"].values
    valores_num = valores[var].values

    if valores_num.size == 0:
        print(f"⚠ Pulando heatmap de {var}: array vazio")
        continue

    # matriz de diferença entre grupos
    matriz = np.abs(valores_num[:, None] - valores_num[None, :])

    plt.figure(figsize=(12,10))  # figura maior
    sns.heatmap(
        matriz,
        annot=True,
        cmap="viridis",
        xticklabels=grupos_unicos,
        yticklabels=grupos_unicos,
        fmt=".2f",
        annot_kws={"size":8},  # fonte menor
        square=True,
        cbar_kws={"label": var}  # legenda da colorbar
    )

    # rotacionar ticks verticalmente para melhor leitura
    plt.xticks(rotation=90, ha="center")
    plt.yticks(rotation=0)  # y horizontal
    plt.title(f"Heatmap - {var}")
    plt.tight_layout()
    plt.savefig(f"graficos/heatmap_{var}.png")
    plt.close()

# ----------------------------
# gerar relatório PDF
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

    media = np.nan_to_num(media)
    desvio = np.nan_to_num(desvio)
    minimo = np.nan_to_num(minimo)
    maximo = np.nan_to_num(maximo)

    r2 = regressao(valores)

    # Calcular maior e menor valor
    maior, grupo_maior, menor, grupo_menor = maior_menor_valor(var)

    # Adicionar no PDF a frase solicitada
    pdf.set_font("Arial","B",12)
    pdf.cell(0,10,str(var),0,1)

    pdf.set_font("Arial","",11)
    pdf.cell(0,8,f"Media: {media:.2f}",0,1)
    pdf.cell(0,8,f"Desvio: {desvio:.2f}",0,1)
    pdf.cell(0,8,f"Min: {minimo:.2f}",0,1)
    pdf.cell(0,8,f"Max: {maximo:.2f}",0,1)
    pdf.cell(0,8,str(f"Regressao ML: {r2}"),0,1)
    pdf.cell(0,8,f"Maior valor de {var} é o {grupo_maior} ({maior:.2f})",0,1)
    pdf.cell(0,8,f"Menor valor de {var} é o {grupo_menor} ({menor:.2f})",0,1)

    # adicionar gráfico de barras
    pdf.image(f"graficos/{var}.png",w=120)

    # adicionar heatmap se existir
    heatmap_path = f"graficos/heatmap_{var}.png"
    if os.path.exists(heatmap_path):
        pdf.ln(5)
        pdf.image(heatmap_path,w=120)

    pdf.ln(10)

pdf.output("relatorios/relatorio_biomecanica.pdf")

print("\n✅ Relatório gerado com sucesso!")