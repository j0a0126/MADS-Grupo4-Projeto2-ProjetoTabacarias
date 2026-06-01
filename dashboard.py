import plotly.express as px


def gerar_dashboard(get_data):
    vendas = get_data("vendas")
    tabacarias = get_data("tabacarias")

    graficos = ""

    try:
        total_vendas = vendas["Valor"].astype(float).sum()
    except:
        total_vendas = 0

    total_tabacarias = len(tabacarias)
    total_vendas_registadas = len(vendas)

    # Gráfico de vendas por tabacaria
    try:
        vendas_por_tabacaria = vendas.groupby("NIF_Tabacaria")["Valor"].sum().reset_index()
        fig1 = px.bar(
            vendas_por_tabacaria,
            x="NIF_Tabacaria",
            y="Valor",
            title="Valor Total de Vendas por Tabacaria"
        )
        graficos += fig1.to_html(full_html=False)
    except Exception as e:
        graficos += f"<p>Erro ao gerar gráfico de vendas por tabacaria: {e}</p>"

    # Gráfico de vendas por descrição
    try:
        vendas_por_descricao = vendas.groupby("Descricao")["Valor"].sum().reset_index()
        fig2 = px.bar(
            vendas_por_descricao,
            x="Descricao",
            y="Valor",
            title="Vendas por Descrição"
        )
        graficos += fig2.to_html(full_html=False)
    except Exception as e:
        graficos += f"<p>Erro ao gerar gráfico de vendas por descrição: {e}</p>"

    # Gráfico de evolução de vendas por data
    try:
        vendas["Data"] = vendas["Data"].astype(str)
        vendas_por_data = vendas.groupby("Data")["Valor"].sum().reset_index()
        fig3 = px.line(
            vendas_por_data,
            x="Data",
            y="Valor",
            title="Evolução das Vendas"
        )
        graficos += fig3.to_html(full_html=False)
    except Exception as e:
        graficos += f"<p>Erro ao gerar gráfico de evolução de vendas: {e}</p>"

    # Gráfico por categoria de venda
    try:
        vendas_por_categoria = vendas.groupby("Categoria_Venda")["Valor"].sum().reset_index()
        fig4 = px.pie(
            vendas_por_categoria,
            names="Categoria_Venda",
            values="Valor",
            title="Vendas por Categoria"
        )
        graficos += fig4.to_html(full_html=False)
    except Exception as e:
        graficos += f"<p>Erro ao gerar gráfico por categoria de venda: {e}</p>"

    return f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Dashboard de Tabacarias</title>
    </head>
    <body>
        <h1>Dashboard de Tabacarias</h1>

        <h2>Indicadores gerais</h2>
        <p><strong>Total de vendas:</strong> {total_vendas:.2f} €</p>
        <p><strong>Número de tabacarias:</strong> {total_tabacarias}</p>
        <p><strong>Número de vendas registadas:</strong> {total_vendas_registadas}</p>

        {graficos}

        <br>
        <a href="/">Voltar</a>
    </body>
    </html>
    """