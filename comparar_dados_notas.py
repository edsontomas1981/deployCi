def comparar_dados_notas(dados_pdf, dados_planilha):
    divergencias = {
        "notas_apenas_na_planilha": [],
        "notas_apenas_no_pdf": [],
        "notas_com_diferenca": []
    }

    # Mapeia todas as notas do PDF (cada nota aponta para seu pedido e dados)
    notas_pdf_map = {}  # nota_fiscal -> {'pedido': ..., 'vols': ..., 'peso': ...}
    for pedido, dados in dados_pdf.items():
        for nota in dados['notas_fiscais']:
            notas_pdf_map[nota] = {
                'pedido': pedido,
                'vols': dados['vols'],
                'peso': dados['peso']
            }

    # Notas da planilha que não estão no PDF
    for nota, valores_planilha in dados_planilha.items():
        if nota not in notas_pdf_map:
            divergencias["notas_apenas_na_planilha"].append(nota)
        else:
            valores_pdf = notas_pdf_map[nota]
            vols_iguais = valores_planilha['vols'] == valores_pdf['vols']
            peso_diferenca = abs(valores_planilha['peso'] - valores_pdf['peso'])

            if not vols_iguais or peso_diferenca > 5:
                divergencias["notas_com_diferenca"].append({
                    'nota': nota,
                    'vols_pdf': valores_pdf['vols'],
                    'vols_planilha': valores_planilha['vols'],
                    'peso_pdf': valores_pdf['peso'],
                    'peso_planilha': valores_planilha['peso']
                })

    # Notas do PDF que não estão na planilha
    for nota in notas_pdf_map:
        if nota not in dados_planilha:
            divergencias["notas_apenas_no_pdf"].append(nota)

    return divergencias
