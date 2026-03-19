from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def gerar_relatorio(resultados):
    c = canvas.Canvas("output/relatorio.pdf", pagesize=letter)

    y = 750
    for chave, valor in resultados.items():
        texto = f"{chave} -> media: {valor['media']:.2f}"
        c.drawString(50, y, texto)
        y -= 20

    c.save()