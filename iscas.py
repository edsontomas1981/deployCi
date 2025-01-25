import sqlite3
from datetime import datetime

def consultar_isca_percurso(isca):
    conn = sqlite3.connect('bd_norte.db')  # Substitua por nome real do arquivo do banco de dados
    cursor = conn.cursor()

    sql = """
            SELECT manifesto_numero,percurso, data
            FROM comunicacao_interna
            WHERE isca_1 = ? OR isca_2 = ?
            ORDER BY manifesto_numero DESC
          """

    cursor.execute(sql, (isca, isca))  # Passando a isca como parâmetro
    resultado = cursor.fetchall()
    return resultado

def data_sort_key(item):
    return item.get('data', None)  # Retorna None se 'data' não existir

def localiza_iscas():
    dict_iscas = []
    iscas = [
        16044464,16050806,16201616,16202962,16203757,16210490,16211019,16216529,16216955
        ,16400103,16401237,16401541,16401627,16402701,16402779,16403916,16403921,16405266
        ,16405268,16405269,16405270,16405271,16405273,16405292,16405297,16405299,16405301
        ,16405302,16405304,16405305,16405307,16405309,16405310,16405311,16405363,16405365
        ,16405366,16405368,16405369,16405371,16405383,16405388,16405390,16405518,16405523
        ,16405526,16405584,16405589,16405633,16405642,16405659,16405675,16406390,16407040
        ,16407069,16408014,16408206,16409529,16410677,16410679,16410691,16410693,16410740
        ,16410850,16410857,16410858,16410859,16410879,16410882,16412711,16412712,16412741
        ,16412744,16412757,16412758,16412764,16412781,16412784,16413541,16413548,16413549
        ,16413550,16413611,16413639,16413653,16413664,16413665,16413668,16413674
    ]

    for isca in iscas:
        registro = consultar_isca_percurso(isca)
        if registro and len(registro) > 0 and len(registro[0]) == 3:
            dict_iscas.append({
                'id': isca,
                'manifesto': registro[0][0] if registro[0][0] is not None else "Sem Informação",
                'percurso': registro[0][1] if registro[0][1] is not None else "Sem Informação",
                'data': registro[0][2] if registro[0][2] is not None else "Sem Informação"
            })

    return dict_iscas

