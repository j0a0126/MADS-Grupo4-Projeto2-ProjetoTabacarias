import folium
import html


def gerar_mapa(get_data):
    try:
        tabacarias = get_data("tabacarias")
        categorias = get_data("categoriasTabacarias")
    except Exception as e:
        return f"""
        <h1>Mapa de Tabacarias</h1>
        <p>Erro ao carregar dados: {html.escape(str(e))}</p>
        <a href="/">Voltar</a>
        """

    if tabacarias.empty:
        return """
        <h1>Mapa de Tabacarias</h1>
        <p>A tabela de tabacarias está vazia.</p>
        <a href="/">Voltar</a>
        """

    # Criar dicionário categoria -> cor
    cores_categorias = {}

    try:
        for _, row in categorias.iterrows():
            nome_categoria = str(row["Nome"]).strip()
            cor = str(row["Cor"]).strip()

            if nome_categoria and cor:
                cores_categorias[nome_categoria] = cor
    except Exception:
        cores_categorias = {}

    # Criar mapa centrado na Maia
    mapa = folium.Map(
        location=[41.2340, -8.6210],
        zoom_start=13,
        width="100%",
        height="600px"
    )

    pontos_adicionados = 0

    for _, row in tabacarias.iterrows():
        try:
            nome = str(row["Nome"])
            categoria = str(row["Categoria"])
            latitude = float(str(row["Latitude"]).replace(",", "."))
            longitude = float(str(row["Longitude"]).replace(",", "."))
            morada = str(row["Morada"])
            cidade = str(row["Cidade"])
            codigo_postal = str(row["CodigoPostal"])
            horario = str(row["Horario"])

            cor = cores_categorias.get(categoria, "blue")

            popup_html = f"""
            <div style="font-family: Arial; width: 260px;">
                <h4 style="margin-bottom: 8px;">{html.escape(nome)}</h4>
                <p><strong>Categoria:</strong> {html.escape(categoria)}</p>
                <p><strong>Morada:</strong> {html.escape(morada)}</p>
                <p><strong>Cidade:</strong> {html.escape(cidade)}</p>
                <p><strong>Código Postal:</strong> {html.escape(codigo_postal)}</p>
                <p><strong>Horário:</strong> {html.escape(horario)}</p>
            </div>
            """

            # Se a cor vier em hexadecimal, usar CircleMarker
            if cor.startswith("#"):
                folium.CircleMarker(
                    location=[latitude, longitude],
                    radius=8,
                    color=cor,
                    fill=True,
                    fill_color=cor,
                    fill_opacity=0.9,
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=nome
                ).add_to(mapa)

            # Se for uma cor normal do Folium, usar Marker
            else:
                folium.Marker(
                    location=[latitude, longitude],
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=nome,
                    icon=folium.Icon(color=cor, icon="info-sign")
                ).add_to(mapa)

            pontos_adicionados += 1

        except Exception as e:
            print("Erro ao adicionar ponto no mapa:", e)

    # Legenda
    legenda = """
    <div style="
        position: fixed;
        bottom: 30px;
        left: 30px;
        z-index: 9999;
        background-color: white;
        padding: 12px;
        border: 1px solid #ccc;
        border-radius: 6px;
        font-family: Arial;
        font-size: 13px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    ">
        <strong>Legenda de Categorias</strong><br>
    """

    for categoria, cor in cores_categorias.items():
        legenda += f"""
        <div style="margin-top: 6px;">
            <span style="
                display: inline-block;
                width: 12px;
                height: 12px;
                background-color: {html.escape(cor)};
                border-radius: 50%;
                margin-right: 6px;
            "></span>
            {html.escape(categoria)}
        </div>
        """

    legenda += "</div>"

    mapa.get_root().html.add_child(folium.Element(legenda))

    mapa_html = mapa._repr_html_()

    return f"""
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <title>Mapa de Tabacarias</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                background-color: #f5f5f5;
            }}

            header {{
                background-color: #2c3e50;
                color: white;
                padding: 20px 30px;
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

            .info {{
                margin-bottom: 15px;
                background-color: white;
                padding: 10px;
                border-left: 4px solid #2c3e50;
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>Mapa de Tabacarias</h1>
            <p>Localização das tabacarias registadas no sistema.</p>
        </header>

        <main>
            <a class="botao" href="/">Voltar</a>

            <div class="info">
                Pontos adicionados ao mapa: <strong>{pontos_adicionados}</strong>
            </div>

            {mapa_html}
        </main>
    </body>
    </html>
    """