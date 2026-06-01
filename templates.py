def gerar_pagina(titulo, tabela_html, mensagem=""):
    return f"""
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <title>Projeto 2 - Tabacarias</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f5f5f5;
            }}

            h1 {{
                color: #333;
            }}

            form {{
                margin-bottom: 20px;
            }}

            input {{
                padding: 8px;
                width: 230px;
            }}

            button {{
                padding: 8px 14px;
                cursor: pointer;
            }}

            .erro {{
                color: red;
                font-weight: bold;
            }}

            .tabela {{
                border-collapse: collapse;
                width: 100%;
                background-color: white;
            }}

            .tabela th, .tabela td {{
                border: 1px solid #ccc;
                padding: 8px;
                text-align: left;
            }}

            .tabela th {{
                background-color: #333;
                color: white;
            }}
        </style>
    </head>
    <body>
        <h1>Projeto 2 - Análise de Tabacarias</h1>

        <p>
            Esta aplicação permite consultar informação pública sobre tabacarias
            e aceder a dados restritos através de chaves.
        </p>

        <form method="POST">
            <input type="text" name="chave" placeholder="Introduza a chave">
            <button type="submit">Entrar</button>
        </form>

        <p class="erro">{mensagem}</p>

        <h2>{titulo}</h2>

        {tabela_html}
    </body>
    </html>
    """