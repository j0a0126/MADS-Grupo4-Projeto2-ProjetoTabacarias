import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import re


def norm(s):
    return str(s or "").strip().lower()


def achar_coluna(df, *nomes):
    """
    Procura uma coluna no DataFrame ignorando maiúsculas/minúsculas e espaços.
    """
    if df is None or df.empty:
        return None

    mapa = {norm(coluna): coluna for coluna in df.columns}

    for nome in nomes:
        chave = norm(nome)
        if chave in mapa:
            return mapa[chave]

    return None


def para_numero(valor):
    """
    Converte valores como:
    1.5
    1,5
    1,50 €
    €1,50
    para float.
    """
    if valor is None:
        return None

    texto = str(valor).strip()

    if texto == "" or texto.lower() == "nan":
        return None

    texto = texto.replace("€", "")
    texto = texto.replace(" ", "")
    texto = texto.replace(",", ".")

    texto = re.sub(r"[^0-9.\-]", "", texto)

    try:
        return float(texto)
    except:
        return None


def para_data(valor):
    """
    Converte datas vindas do Google Sheets.
    """
    if valor is None:
        return None

    if hasattr(valor, "date"):
        try:
            return valor.date()
        except:
            pass

    texto = str(valor).strip()

    if texto == "" or texto.lower() == "nan":
        return None

    try:
        return datetime.fromisoformat(texto).date()
    except:
        pass

    formatos = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%d.%m.%Y",
        "%Y-%m-%d %H:%M:%S",
        "%d/%m/%Y %H:%M:%S"
    ]

    for formato in formatos:
        try:
            return datetime.strptime(texto, formato).date()
        except:
            continue

    return None


def preparar_vendas(vendas_df):
    """
    Prepara os dados da tabela vendas.
    """
    if vendas_df is None or vendas_df.empty:
        return pd.DataFrame()

    vendas_df = vendas_df.copy()
    vendas_df.columns = [str(c).strip() for c in vendas_df.columns]

    col_id = achar_coluna(vendas_df, "ID")
    col_nif_utilizador = achar_coluna(vendas_df, "NIF_Utilizador", "NIF Utilizador")
    col_nif_tabacaria = achar_coluna(vendas_df, "NIF_Tabacaria", "NIF Tabacaria")
    col_valor = achar_coluna(vendas_df, "Valor")
    col_descricao = achar_coluna(vendas_df, "Descricao", "Descrição")
    col_data = achar_coluna(vendas_df, "Data")
    col_categoria = achar_coluna(vendas_df, "Categoria_Venda", "Categoria Venda")

    linhas = []

    for _, row in vendas_df.iterrows():
        nif_tabacaria = row.get(col_nif_tabacaria) if col_nif_tabacaria else None
        valor = para_numero(row.get(col_valor)) if col_valor else None
        data = para_data(row.get(col_data)) if col_data else None
        descricao = row.get(col_descricao) if col_descricao else ""
        categoria = row.get(col_categoria) if col_categoria else ""
        venda_id = row.get(col_id) if col_id else ""
        nif_utilizador = row.get(col_nif_utilizador) if col_nif_utilizador else ""

        if nif_tabacaria is None or str(nif_tabacaria).strip() == "":
            continue

        if valor is None:
            continue

        if valor <= 0:
            continue

        linhas.append({
            "id": str(venda_id),
            "nif_utilizador": str(nif_utilizador),
            "nif_tabacaria": str(nif_tabacaria).strip(),
            "valor": valor,
            "descricao": str(descricao).strip(),
            "data": data,
            "categoria": str(categoria).strip().upper()
        })

    return pd.DataFrame(linhas)


def preparar_tabacarias(tabacarias_df):
    """
    Cria mapa NIF -> Nome da tabacaria.
    """
    if tabacarias_df is None or tabacarias_df.empty:
        return {}

    tabacarias_df = tabacarias_df.copy()
    tabacarias_df.columns = [str(c).strip() for c in tabacarias_df.columns]

    col_nif = achar_coluna(tabacarias_df, "NIF")
    col_nome = achar_coluna(tabacarias_df, "Nome")

    mapa = {}

    for _, row in tabacarias_df.iterrows():
        nif = row.get(col_nif) if col_nif else None
        nome = row.get(col_nome) if col_nome else None

        if nif is not None and str(nif).strip() != "":
            mapa[str(nif).strip()] = str(nome).strip() if nome else str(nif).strip()

    return mapa


def nome_categoria(categoria):
    mapa = {
        "P": "Produto",
        "S": "Serviço",
        "D": "Diversos"
    }

    return mapa.get(str(categoria).upper().strip(), str(categoria))


def fig_html(fig, div_id, include_js=False):
    return fig.to_html(
        full_html=False,
        include_plotlyjs="cdn" if include_js else False,
        div_id=div_id,
        config={"responsive": True}
    )


def grafico_tempo(df, include_js=False):
    if df.empty:
        return ""

    df_valid = df[df["data"].notna()].copy()

    if df_valid.empty:
        return ""

    # Limitar o gráfico ao período do projeto: até junho de 2026
    data_inicio = datetime(2026, 1, 1).date()
    data_limite = datetime(2026, 6, 30).date()
    df_valid = df_valid[(df_valid["data"] >= data_inicio) & (df_valid["data"] <= data_limite)]

    if df_valid.empty:
        return ""

    vendas = df_valid.groupby("data")["valor"].sum().sort_index()

    fig = go.Figure(data=[
        go.Scatter(
            x=list(vendas.index),
            y=list(vendas.values),
            mode="lines+markers",
            fill="tozeroy",
            line=dict(color="green", width=2)
        )
    ])

    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Valor (€)",
        height=500,
        margin=dict(l=20, r=20, t=20, b=40),
        autosize=True
    )

    fig.update_xaxes(
        range=[data_inicio, data_limite]
    )

    return fig_html(fig, "grafico_tempo", include_js)


def grafico_quantidade_por_tabacaria(df, mapa_tabacarias, include_js=False):
    if df.empty:
        return ""

    dados = df.groupby("nif_tabacaria").size().sort_values(ascending=True)
    nomes = [mapa_tabacarias.get(str(nif), str(nif)) for nif in dados.index]

    fig = go.Figure(data=[
        go.Bar(
            y=nomes,
            x=dados.values,
            orientation="h",
            marker_color="steelblue"
        )
    ])

    fig.update_layout(
        xaxis_title="Número de vendas",
        yaxis_title="Tabacaria",
        height=550,
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=40)
    )

    return fig_html(fig, "grafico_quantidade_tabacaria", include_js)


def grafico_valor_por_tabacaria(df, mapa_tabacarias, include_js=False):
    if df.empty:
        return ""

    dados = df.groupby("nif_tabacaria")["valor"].sum().sort_values(ascending=True)
    nomes = [mapa_tabacarias.get(str(nif), str(nif)) for nif in dados.index]

    fig = go.Figure(data=[
        go.Bar(
            y=nomes,
            x=dados.values,
            orientation="h",
            marker_color="coral"
        )
    ])

    fig.update_layout(
        xaxis_title="Valor (€)",
        yaxis_title="Tabacaria",
        height=550,
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=40)
    )

    return fig_html(fig, "grafico_valor_tabacaria", include_js)


def grafico_categoria(df, include_js=False):
    if df.empty:
        return ""

    dados = df.groupby("categoria")["valor"].sum()

    labels = [nome_categoria(c) for c in dados.index]

    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=dados.values,
            textposition="inside",
            textinfo="label+percent"
        )
    ])

    fig.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=50, b=40)
    )

    return fig_html(fig, "grafico_categoria", include_js)


def grafico_evolucao_categoria(df, include_js=False):
    if df.empty:
        return ""

    df_valid = df[df["data"].notna()].copy()

    if df_valid.empty:
        return ""

    # Limitar o gráfico ao período do projeto: até junho de 2026
    data_inicio = datetime(2026, 1, 1).date()
    data_limite = datetime(2026, 6, 30).date()
    df_valid = df_valid[(df_valid["data"] >= data_inicio) & (df_valid["data"] <= data_limite)]

    if df_valid.empty:
        return ""

    dados = df_valid.groupby(["data", "categoria"])["valor"].sum().reset_index()

    fig = go.Figure()

    for categoria in dados["categoria"].unique():
        dados_categoria = dados[dados["categoria"] == categoria].sort_values("data")

        fig.add_trace(go.Scatter(
            x=dados_categoria["data"],
            y=dados_categoria["valor"],
            mode="lines+markers",
            name=nome_categoria(categoria),
            fill="tozeroy"
        ))

    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Valor (€)",
        height=500,
        hovermode="x unified",
        margin=dict(l=20, r=20, t=20, b=40)
    )

    fig.update_xaxes(
        range=[data_inicio, data_limite]
    )

    return fig_html(fig, "grafico_evolucao_categoria", include_js)


def grafico_descricao(df, include_js=False):
    if df.empty:
        return ""

    df_desc = df.copy()
    df_desc["descricao"] = df_desc["descricao"].astype(str).str.strip()
    df_desc = df_desc[df_desc["descricao"] != ""]

    if df_desc.empty:
        return ""

    dados = df_desc.groupby("descricao")["valor"].sum().sort_values(ascending=False).head(10)
    dados = dados.sort_values(ascending=True)

    fig = go.Figure(data=[
        go.Bar(
            y=list(dados.index),
            x=list(dados.values),
            orientation="h",
            marker_color="mediumpurple"
        )
    ])

    fig.update_layout(
        xaxis_title="Valor (€)",
        yaxis_title="Descrição",
        height=550,
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=40)
    )

    return fig_html(fig, "grafico_descricao", include_js)


def gerar_dashboard(get_data):
    vendas_df = get_data("vendas")
    tabacarias_df = get_data("tabacarias")

    df = preparar_vendas(vendas_df)
    mapa_tabacarias = preparar_tabacarias(tabacarias_df)

    total_vendas = df["valor"].sum() if not df.empty else 0
    numero_tabacarias = len(tabacarias_df) if tabacarias_df is not None else 0
    vendas_registadas = len(df)

    graficos = []

    g1 = grafico_tempo(df, include_js=True)
    if g1:
        graficos.append(f"""
        <div class="grafico-box grafico-box-full">
            <div class="grafico-title">Volume de Faturação ao Longo do Tempo</div>
            <div class="grafico-content">{g1}</div>
        </div>
        """)

    g2 = grafico_quantidade_por_tabacaria(df, mapa_tabacarias)
    if g2:
        graficos.append(f"""
        <div class="grafico-box">
            <div class="grafico-title">Quantidade de Vendas por Tabacaria</div>
            <div class="grafico-content">{g2}</div>
        </div>
        """)

    g3 = grafico_valor_por_tabacaria(df, mapa_tabacarias)
    if g3:
        graficos.append(f"""
        <div class="grafico-box">
            <div class="grafico-title">Volume de Vendas por Tabacaria</div>
            <div class="grafico-content">{g3}</div>
        </div>
        """)

    g4 = grafico_categoria(df)
    if g4:
        graficos.append(f"""
        <div class="grafico-box">
            <div class="grafico-title">Vendas por Categoria</div>
            <div class="grafico-content">{g4}</div>
        </div>
        """)

    g5 = grafico_evolucao_categoria(df)
    if g5:
        graficos.append(f"""
        <div class="grafico-box">
            <div class="grafico-title">Evolução das Vendas por Categoria</div>
            <div class="grafico-content">{g5}</div>
        </div>
        """)

    g6 = grafico_descricao(df)
    if g6:
        graficos.append(f"""
        <div class="grafico-box grafico-box-full">
            <div class="grafico-title">Top 10 Vendas por Descrição</div>
            <div class="grafico-content">{g6}</div>
        </div>
        """)

    graficos_html = "".join(graficos)

    if not graficos_html:
        graficos_html = """
        <div class="grafico-box grafico-box-full">
            <div class="grafico-content">
                <p>Sem gráficos disponíveis.</p>
                <p>Verifica se a tabela <strong>vendas</strong> tem as colunas:</p>
                <ul>
                    <li>ID</li>
                    <li>NIF_Utilizador</li>
                    <li>NIF_Tabacaria</li>
                    <li>Valor</li>
                    <li>Descricao</li>
                    <li>Data</li>
                    <li>Categoria_Venda</li>
                </ul>
            </div>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <title>Dashboard de Tabacarias</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                background-color: #f5f5f5;
                color: #333;
            }}

            header {{
                background-color: #2c3e50;
                color: white;
                padding: 20px 30px;
            }}

            header h1 {{
                margin: 0;
                font-size: 28px;
            }}

            header p {{
                margin-top: 8px;
                font-size: 15px;
            }}

            main {{
                padding: 20px 30px;
            }}

            .botao {{
                display: inline-block;
                margin-bottom: 15px;
                padding: 8px 14px;
                background-color: #2c3e50;
                color: white;
                text-decoration: none;
                border-radius: 4px;
            }}

            .botao:hover {{
                background-color: #1a252f;
            }}

            .info {{
                margin-bottom: 15px;
                background-color: white;
                padding: 12px;
                border-left: 4px solid #2c3e50;
                border-radius: 4px;
            }}

            .cards {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 15px;
                margin-bottom: 20px;
            }}

            .card {{
                background-color: white;
                padding: 18px;
                border-radius: 6px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                border-left: 4px solid #2c3e50;
            }}

            .card h3 {{
                margin: 0 0 10px 0;
                color: #2c3e50;
                font-size: 16px;
            }}

            .card p {{
                font-size: 24px;
                font-weight: bold;
                margin: 0;
            }}

            .dashboard-container {{
                max-width: 1400px;
                margin: 0 auto;
            }}

            .graficos-grid {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
                margin-bottom: 20px;
            }}

            .grafico-box {{
                background: white;
                padding: 0;
                border-radius: 8px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.08);
                overflow: hidden;
            }}

            .grafico-box-full {{
                grid-column: 1 / -1;
            }}

            .grafico-title {{
                font-size: 14px;
                font-weight: 600;
                color: #2c3e50;
                padding: 16px 16px 0 16px;
                text-transform: uppercase;
                letter-spacing: 0.3px;
            }}

            .grafico-content {{
                padding: 16px;
            }}

            .grafico-box .plotly-graph-div {{
                width: 100% !important;
            }}

            @media (max-width: 1024px) {{
                .graficos-grid {{
                    grid-template-columns: 1fr;
                }}

                .grafico-box-full {{
                    grid-column: 1;
                }}
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>Dashboard de Tabacarias</h1>
            <p>Estatísticas e gráficos com base nos dados de vendas registados.</p>
        </header>

        <main>
            <a class="botao" href="/">Voltar</a>

            <div class="info">
                O dashboard apresenta indicadores gerais e gráficos de análise das vendas.
            </div>

            <div class="cards">
                <div class="card">
                    <h3>Total de vendas</h3>
                    <p>{total_vendas:.2f} €</p>
                </div>

                <div class="card">
                    <h3>Número de tabacarias</h3>
                    <p>{numero_tabacarias}</p>
                </div>

                <div class="card">
                    <h3>Vendas registadas</h3>
                    <p>{vendas_registadas}</p>
                </div>
            </div>

            <div class="dashboard-container">
                <div class="graficos-grid">
                    {graficos_html}
                </div>
            </div>
        </main>
    </body>
    </html>
    """