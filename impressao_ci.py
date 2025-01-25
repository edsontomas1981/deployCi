from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet



def imprimir_ci(dados):
    empresa_nome = "SERAFIM TRANSPORTE DE CARGAS LTDA"
    empresa_endereco = "Rua : Nova Veneza,172 Cumbica – Guarulhos-SP"
    empresa_telefones = "Tel(11)2481-9121/2481-9697/2412-4886/2412-3927"
    assinatura = "Nortecargas – SP"

    # Texto com quebras de linha
    texto_com_quebras = """
    <br />
    <br />
    <br />
    """

    # Configurar o PDF
    pdf_filename = dados['pdf_filename']
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    story = []
    logo_image = Image("logonorte.jpg", width=75, height=12)
    logo_image.hAlign = 'LEFT'


    # Estilos de texto
    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]
    normal_style.alignment = 0  # 0 = left, 1 = center, 2 = right
    normal_style.fontSize = 12  # Tamanho da fonte (por exemplo, 12)


    h1 = styles['Heading1']
    h1.alignment = 1  # 0 = left, 1 = center, 2 = right
    h2 = styles['Heading2']
    h2.alignment = 1  # 0 = left, 1 = center, 2 = right
    h3 = styles['Heading3']     
    h3.alignment = 1  # 0 = left, 1 = center, 2 = right
    h5 = styles['Heading5']         
    h5.alignment = 1  # 0 = left, 1 = center, 2 = right
    h6 = styles['Heading6']         
    h6.alignment = 1  # 0 = left, 1 = center, 2 = right


    # Inserir a imagem no documento
    story.append(logo_image)

    # Criar um objeto Paragraph com o texto
    story.append(Paragraph(texto_com_quebras, normal_style))

    # # Adicionar texto ao documento
    # story.append(Paragraph('Comunicação Interna', h1))
    story.append(Paragraph(empresa_nome, h1))
    story.append(Paragraph(empresa_endereco, h5))
    story.append(Paragraph(empresa_telefones, h5))
    story.append(Paragraph("", normal_style))  # Linha em branco
    # Criar um objeto Paragraph com o texto
    story.append(Paragraph(texto_com_quebras, normal_style))

    story.append(Paragraph(f"Comunicacao Interna Nº {dados['ci_num']}", h3))
    story.append(Paragraph(f"Data : {dados['data']} Percurso : {dados['percurso']}", h5))

    # Criar um objeto Paragraph com o texto     
    story.append(Paragraph(texto_com_quebras, normal_style))

    texto = f"{dados['destinatario']},<br /><br />" \
            f"Estamos enviando o manifesto de transporte de cargas nº {dados['manifesto_numero']}. Este manifesto inclui conhecimentos de frete.<br /><br />" \
            f"De acordo com este manifesto, solicitamos o pagamento de R$ {dados['valor_frete']} ao motorista {dados['motorista']}, referente à Ordem de Pagamento.<br /><br />" \

    if dados['isca_2'] != '':
        texto += f"Além disso, incluímos as seguintes iscas de monitoramento: {dados['isca_1']} e {dados['isca_2']}."
    else:
        texto += f"Também incluímos a seguinte isca de monitoramento: {dados['isca_1']}."

    observacao =f"{dados['observacao']}<br /><br />" \

    story.append(Paragraph(texto, normal_style))

    story.append(Paragraph(texto_com_quebras, normal_style))

    if dados['observacao'] != '':
        story.append(Paragraph(f"Observações", h3))
        story.append(Paragraph(observacao, normal_style))

    # Criar um objeto Paragraph com o texto     
    story.append(Paragraph(texto_com_quebras, normal_style))

    # Criar uma tabela para a assinatura do motorista e da empresa
    data = [[empresa_nome, dados['motorista']],
            ["", ""],  # Espaço em branco para a primeira linha de assinatura
            ["Assinatura da Empresa", "Assinatura do Motorista"]]  # Rótulos das assinaturas

    table_style = [('ALIGN', (0, 0), (-1, -1), 'RIGHT'),  # Alinha à direita horizontalmente
                ('LEFTPADDING', (0, 0), (-1, -1), 50),  # Adiciona espaço à esquerda para alinhar à direita
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]

    tabela_assinatura = Table(data, colWidths=[200, 200])
    tabela_assinatura.setStyle(TableStyle(table_style))

    # Adicionar a tabela ao relatório
    story.append(tabela_assinatura)


    # Gerar o PDF
    doc.build(story)
