from flask import Flask, request
import pygsheets
import pandas as pd
import json
import os
import time
from dotenv import load_dotenv

from templates import gerar_pagina
from integridade import gerar_relatorio_integridade
from dashboard import gerar_dashboard
from mapa import gerar_mapa

load_dotenv()

app = Flask(__name__)

is_production = os.getenv("isProduction") == "true"

if is_production:
    service_file_path = "/etc/secrets/credenciais_google.json"
    chave_file_path = "/etc/secrets/chave.json"
else:
    service_file_path = "secrets/credenciais_google.json"
    chave_file_path = "secrets/chave.json"


# Cache simples para reduzir consumo de memória, ligações ao Google e tempo de resposta
SHEET_NAME = "BaseDados_Tabacarias"
CACHE_TTL = 300  # 5 minutos

_sheet_cache = None
_chaves_cache = None
_data_cache = {}


def ligar_google_sheets():
    """
    Liga ao Google Sheets apenas uma vez por instância.
    Evita autorizar e abrir o ficheiro em todas as chamadas.
    """
    global _sheet_cache

    if _sheet_cache is None:
        gc = pygsheets.authorize(service_file=service_file_path)
        _sheet_cache = gc.open(SHEET_NAME)

    return _sheet_cache


def get_data(nome_tabela):
    """
    Lê uma folha do Google Sheets com cache temporária.
    Isto é importante no Render Free, porque reduz memória e pedidos repetidos.
    """
    agora = time.time()

    if nome_tabela in _data_cache:
        instante, df_cache = _data_cache[nome_tabela]

        if agora - instante < CACHE_TTL:
            return df_cache.copy()

    sheet = ligar_google_sheets()
    worksheet = sheet.worksheet_by_title(nome_tabela)
    dados = worksheet.get_all_records()
    df = pd.DataFrame(dados)

    _data_cache[nome_tabela] = (agora, df)

    return df.copy()


def carregar_chaves():
    """
    Carrega o ficheiro de chaves apenas uma vez.
    """
    global _chaves_cache

    if _chaves_cache is None:
        with open(chave_file_path, "r", encoding="utf-8") as f:
            _chaves_cache = json.load(f)

    return _chaves_cache


def tabela_html(nome_tabela):
    """
    Gera HTML da tabela com escape ativo para segurança.
    """
    df = get_data(nome_tabela)

    return df.to_html(
        index=False,
        classes="tabela",
        escape=True
    )


@app.route("/", methods=["GET", "POST"])
def index():
    mensagem = ""

    try:
        chaves = carregar_chaves()

        if request.method == "POST":
            chave = request.form.get("chave", "").strip()

            if chave == "":
                return gerar_pagina("Tabacarias", tabela_html("tabacarias"), mensagem)

            if chave not in chaves:
                mensagem = "Chave inválida."
                return gerar_pagina("Tabacarias", tabela_html("tabacarias"), mensagem)

            destino = chaves[chave]

            if destino == "integridade":
                return gerar_relatorio_integridade(get_data)

            if destino == "dashboard":
                return gerar_dashboard(get_data)

            if destino == "mapa":
                return gerar_mapa(get_data)

            return gerar_pagina(destino, tabela_html(destino), mensagem)

        return gerar_pagina("Tabacarias", tabela_html("tabacarias"), mensagem)

    except Exception as e:
        print("ERRO REAL:", repr(e))
        return f"Erro na aplicação: {repr(e)}"


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )