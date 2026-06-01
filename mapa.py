import folium


def gerar_mapa(get_data):
    tabacarias = get_data("tabacarias")

    mapa = folium.Map(location=[41.23, -8.62], zoom_start=12)

    for _, row in tabacarias.iterrows():
        try:
            nome = row.get("Nome", "Tabacaria")
            morada = row.get("Morada", "")
            cidade = row.get("Cidade", "")
            horario = row.get("Horario", "")
            categoria = row.get("Categoria", "")

            latitude = float(row.get("Latitude"))
            longitude = float(row.get("Longitude"))

            popup = f"""
            <b>{nome}</b><br>
            Morada: {morada}<br>
            Cidade: {cidade}<br>
            Horário: {horario}<br>
            Categoria: {categoria}
            """

            folium.Marker(
                location=[latitude, longitude],
                popup=popup,
                tooltip=nome
            ).add_to(mapa)

        except:
            continue

    mapa_html = mapa._repr_html_()

    return f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Mapa de Tabacarias</title>
    </head>
    <body>
        <h1>Mapa de Tabacarias</h1>
        {mapa_html}
        <br>
        <a href="/">Voltar</a>
    </body>
    </html>
    """