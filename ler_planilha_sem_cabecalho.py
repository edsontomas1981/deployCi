import pandas as pd

def ler_planilha_sem_cabecalho(caminho_arquivo):
    df = pd.read_excel(caminho_arquivo, header=None)
    dados = {}
    for idx, row in df.iterrows():
        try:
            nota = str(int(row[0]))  # Nota fiscal
            vols = int(row[1])
            peso = float(row[2])
            dados[nota] = {
                'vols': vols,
                'peso': peso
            }
        except Exception as e:
            print(f"Erro ao processar linha {idx+1}: {row.tolist()} -> {e}")
    return dados
