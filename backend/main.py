from fastapi import FastAPI
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

DB_CONFIG = {
    'host':     os.getenv('DB_HOST'),
    'port':     os.getenv('DB_PORT'),
    'dbname':   os.getenv('DB_NAME'),
    'user':     os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

#_________ endpoint da populacao _________

@app.get('/populacao')
def get_populacao():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT periodo, localidade, valor, unidade
        FROM populacao
        ORDER BY periodo ASC
    ''')
    
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    resultado = []
    for row in rows:
        resultado.append({
            'periodo':      row[0],
            'localidade':   row[1],
            'valor':        float(row[2]),
            'unidade':      row[3]
        })

    return resultado

#_________ endpoint teste _________
 
@app.get('/')
def home():
    return{'status': 'API Funcionando.'} 