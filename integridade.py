def gerar_relatorio_integridade(get_data):
    erros = []

    try:
        utilizadores = get_data("utilizadores")
        categorias = get_data("categoriasTabacarias")
        tabacarias = get_data("tabacarias")
        vendas = get_data("vendas")

        tabelas = {
            "utilizadores": utilizadores,
            "categoriasTabacarias": categorias,
            "tabacarias": tabacarias,
            "vendas": vendas
        }

        for nome, df in tabelas.items():
            if df.empty:
                erros.append(f"A tabela {nome} está vazia.")

            if df.columns.duplicated().any():
                erros.append(f"A tabela {nome} tem colunas duplicadas.")

            for coluna in df.columns:
                if coluna.strip() == "":
                    erros.append(f"A tabela {nome} tem cabeçalhos vazios.")

        # Validações dos utilizadores
        if "NIF" in utilizadores.columns:
            if utilizadores["NIF"].isnull().any():
                erros.append("Existem utilizadores sem NIF.")

            if utilizadores["NIF"].duplicated().any():
                erros.append("Existem NIFs duplicados na tabela utilizadores.")

        if "Nome" in utilizadores.columns:
            if utilizadores["Nome"].isnull().any():
                erros.append("Existem utilizadores sem nome.")

        if "Genero" in utilizadores.columns:
            generos_validos = {"M", "F", "Outro"}
            for genero in utilizadores["Genero"].astype(str):
                if genero not in generos_validos:
                    erros.append(f"Género inválido encontrado: {genero}")

        # Validações das categorias
        if "Nome" in categorias.columns:
            if categorias["Nome"].isnull().any():
                erros.append("Existem categorias sem nome.")

            if categorias["Nome"].duplicated().any():
                erros.append("Existem categorias duplicadas.")

        # Validações das tabacarias
        if "NIF" in tabacarias.columns:
            if tabacarias["NIF"].isnull().any():
                erros.append("Existem tabacarias sem NIF.")

            if tabacarias["NIF"].duplicated().any():
                erros.append("Existem NIFs duplicados na tabela tabacarias.")

        if "Nome" in tabacarias.columns:
            if tabacarias["Nome"].isnull().any():
                erros.append("Existem tabacarias sem nome.")

        if "Categoria" in tabacarias.columns and "Nome" in categorias.columns:
            categorias_validas = set(categorias["Nome"].astype(str))
            for categoria in tabacarias["Categoria"].astype(str):
                if categoria not in categorias_validas:
                    erros.append(f"Tabacaria com categoria inexistente: {categoria}")

        if "Latitude" in tabacarias.columns:
            for lat in tabacarias["Latitude"]:
                try:
                    lat = float(lat)
                    if lat < -90 or lat > 90:
                        erros.append(f"Latitude inválida: {lat}")
                except:
                    erros.append(f"Latitude com formato inválido: {lat}")

        if "Longitude" in tabacarias.columns:
            for lon in tabacarias["Longitude"]:
                try:
                    lon = float(lon)
                    if lon < -180 or lon > 180:
                        erros.append(f"Longitude inválida: {lon}")
                except:
                    erros.append(f"Longitude com formato inválido: {lon}")

        if "Horario" in tabacarias.columns:
            if tabacarias["Horario"].isnull().any():
                erros.append("Existem tabacarias sem horário.")

        # Validações das vendas
        if "ID" in vendas.columns:
            if vendas["ID"].isnull().any():
                erros.append("Existem vendas sem ID.")

            if vendas["ID"].duplicated().any():
                erros.append("Existem IDs duplicados na tabela vendas.")

        if "Valor" in vendas.columns:
            for valor in vendas["Valor"]:
                try:
                    valor = float(valor)
                    if valor <= 0:
                        erros.append(f"Venda com valor inválido: {valor}")
                except:
                    erros.append(f"Valor com formato inválido: {valor}")

        if "NIF_Utilizador" in vendas.columns and "NIF" in utilizadores.columns:
            nifs_utilizadores = set(utilizadores["NIF"].astype(str))
            for nif in vendas["NIF_Utilizador"].astype(str):
                if nif not in nifs_utilizadores:
                    erros.append(f"Venda com utilizador inexistente: {nif}")

        if "NIF_Tabacaria" in vendas.columns and "NIF" in tabacarias.columns:
            nifs_tabacarias = set(tabacarias["NIF"].astype(str))
            for nif in vendas["NIF_Tabacaria"].astype(str):
                if nif not in nifs_tabacarias:
                    erros.append(f"Venda com tabacaria inexistente: {nif}")

        if "Categoria_Venda" in vendas.columns:
            categorias_venda_validas = {"S", "P", "D"}
            for categoria in vendas["Categoria_Venda"].astype(str):
                if categoria not in categorias_venda_validas:
                    erros.append(f"Categoria de venda inválida: {categoria}")

    except Exception as e:
        erros.append(f"Erro ao validar os dados: {e}")

    if len(erros) == 0:
        lista_erros = "<p>Não foram encontrados erros de integridade.</p>"
    else:
        lista_erros = "<ul>"
        for erro in erros:
            lista_erros += f"<li>{erro}</li>"
        lista_erros += "</ul>"

    return f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Integridade dos Dados</title>
    </head>
    <body>
        <h1>Relatório de Integridade dos Dados</h1>
        <p>Esta página verifica problemas nas tabelas da base de dados.</p>
        {lista_erros}
        <br>
        <a href="/">Voltar</a>
    </body>
    </html>
    """