from flask import Flask, request
import pygsheets
import pandas as pd
import json
import os
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


def ligar_google_sheets():
    gc = pygsheets.authorize(service_file=service_file_path)
    sheet = gc.open("BaseDados_Tabacarias")
    return sheet


def get_data(nome_tabela):
    sheet = ligar_google_sheets()
    worksheet = sheet.worksheet_by_title(nome_tabela)
    dados = worksheet.get_all_records()
    return pd.DataFrame(dados)


def carregar_chaves():
    with open(chave_file_path, "r", encoding="utf-8") as f:
        return json.load(f)


@app.route("/", methods=["GET", "POST"])
def index():
    mensagem = ""

    try:
        chaves = carregar_chaves()

        if request.method == "POST":
            chave = request.form.get("chave", "").strip()

            if chave == "":
                df = get_data("tabacarias")
                tabela_html = df.to_html(index=False, classes="tabela")
                return gerar_pagina("Tabacarias", tabela_html, mensagem)

            if chave not in chaves:
                mensagem = "Chave inválida."
                df = get_data("tabacarias")
                tabela_html = df.to_html(index=False, classes="tabela")
                return gerar_pagina("Tabacarias", tabela_html, mensagem)

            destino = chaves[chave]

            if destino == "integridade":
                return gerar_relatorio_integridade(get_data)

            elif destino == "dashboard":
                return gerar_dashboard(get_data)

            elif destino == "mapa":
                return gerar_mapa(get_data)

            else:
                df = get_data(destino)
                tabela_html = df.to_html(index=False, classes="tabela")
                return gerar_pagina(destino, tabela_html, mensagem)

        df = get_data("tabacarias")
        tabela_html = df.to_html(index=False, classes="tabela")
        return gerar_pagina("Tabacarias", tabela_html, mensagem)

    except Exception as e:
        print("ERRO REAL:", repr(e))
        return f"Erro na aplicação: {repr(e)}"

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )