import requests
import psycopg2
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# ______configuracoes do banco______

DB_CONFIG = {
    "host":     os.getenv('DB_HOST'),
    "port":     os.getenv('DB_PORT'),
    "dbname":   os.getenv('DB_NAME'),
    "user":     os.getenv('DB_USER'),
    "password": os.getenv('DB_PASSWORD')
}

# ______url da api do ibge______

URL = (
     "https://servicodados.ibge.gov.br/api/v3/agregados"
    "/6022/periodos/-12/variaveis/606?localidades=N1[all]"
)

# ______buscar dados da api______

def buscar_dados():
    response = requests.get(URL)
    dados = response.json()

    return dados

# ______teste temporario______

def transformar_dados(dados):
    registros =     []
    serie =         dados[0]['resultados'][0]['series'][0]
    localidade =    serie['localidade']['nome']
    unidade =       dados[0]['unidade']

    for periodo, valor in serie['serie'].items():
        registros.append({
            'periodo':      periodo,
            'localidade':   localidade,
            'valor':        float(valor),
            'unidade':      unidade
        })

    return registros

# ______ carregar dados no postgresql ______

def carregar_dados(registros):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    for r in registros:
        cursor.execute("""
            INSERT INTO populacao (periodo, localidade, valor, unidade)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (r['periodo'], r['localidade'], r['valor'], r['unidade'])
        )

    conn.commit()
    cursor.close()
    conn.close()

    print(f'{len(registros)} registros inseridos no banco de dados')

# ______teste temporario______


# ______teste temporario______

if __name__ == "__main__":
    dados = buscar_dados()
    registros = transformar_dados(dados)
    carregar_dados(registros)
