# Análise Biomecânica de Fratura do Maléolo Posterior com MEF

## 📌 Objetivo
Este projeto tem como objetivo analisar o comportamento biomecânico de uma fratura do maléolo posterior do tornozelo utilizando simulação por Método dos Elementos Finitos (MEF), comparando 6 diferentes técnicas de fixação.

---

## 🧠 Metodologia

Os dados foram obtidos a partir de simulações computacionais e processados em Python utilizando:

- Pandas
- NumPy
- Matplotlib
- Seaborn

O fluxo do projeto inclui:

- Importação dos dados (Excel)
- Organização e tratamento dos dados
- Cálculo de parâmetros biomecânicos (Tmax, Tmin, Von Mises, deslocamentos)
- Análise comparativa entre diferentes fixações
- Geração automática de gráficos
- Exportação de relatório técnico em PDF

---

## 📊 Resultados

### Comparação entre técnicas de fixação

![Gráfico](graficos/comparacao_fixacoes.png)
## 📊 Resultados

### 🔹 Deslocamento (DF)
![Deslocamento](graficos/DF.png)

### 🔹 Tensão de Von Mises (Tvon)
![Von Mises](graficos/Tvon.png)

### 🔹 Heatmap de Deslocamento
![Heatmap DF](graficos/heatmap_DF.png)

### 🔹 Heatmap de Tensões (Von Mises)
![Heatmap Tvon](graficos/heatmap_Tvon.png)
---

## 🔍 Insight

A análise dos dados permitiu identificar diferenças relevantes entre as técnicas de fixação, destacando aquelas com menor concentração de tensões e maior estabilidade mecânica, o que pode auxiliar na tomada de decisão clínica.

---

## 🛠️ Tecnologias

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Método dos Elementos Finitos (MEF)

---

## ▶️ Como executar

```bash
pip install -r requirements.txt
python src/main.py