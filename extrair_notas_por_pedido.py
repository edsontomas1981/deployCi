import re
import pdfplumber

def extrair_notas_por_pedido(caminho_pdf):
    pedidos_dict = {}
    padrao = re.compile(
        r'(?P<pedido>\d{6})\s+.*?(?P<notas>(?:\d{4,},\s*)+)(?P<vols>\d+)\s+(?P<peso>\d+)\s+\d+\s+(?P<val_nf>[\d\.,]+)\s+[\d\.,]+\s+[FCR]'
    )

    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if not texto:
                continue
            for linha in texto.split('\n'):
                match = padrao.search(linha)
                if match:
                    pedido = match.group('pedido')
                    notas = re.findall(r'\d{4,}', match.group('notas'))
                    vols = int(match.group('vols'))
                    peso = int(match.group('peso'))
                    val_nf = float(match.group('val_nf').replace('.', '').replace(',', '.'))

                    pedidos_dict[pedido] = {
                        'notas_fiscais': notas,
                        'vols': vols,
                        'peso': peso,
                        'val_nf': val_nf
                    }

    return pedidos_dict
