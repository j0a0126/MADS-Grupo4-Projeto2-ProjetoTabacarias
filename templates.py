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

            .card {{
                background-color: white;
                padding: 18px;
                border-radius: 6px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }}

            .info {{
                margin-bottom: 15px;
                background-color: white;
                padding: 12px;
                border-left: 4px solid #2c3e50;
                border-radius: 4px;
            }}

            form {{
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
                margin-top: 10px;
            }}

            input {{
                padding: 9px;
                width: 260px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }}

            button {{
                padding: 9px 16px;
                cursor: pointer;
                background-color: #2c3e50;
                color: white;
                border: none;
                border-radius: 4px;
            }}

            button:hover {{
                background-color: #1a252f;
            }}

            .erro {{
                color: #c0392b;
                font-weight: bold;
                margin-top: 10px;
            }}

            .tabela-container {{
                overflow-x: auto;
                background-color: white;
                padding: 15px;
                border-radius: 6px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            }}

            .tabela {{
                border-collapse: collapse;
                width: 100%;
                background-color: white;
                font-size: 14px;
            }}

            .tabela th, .tabela td {{
                border: 1px solid #ddd;
                padding: 9px;
                text-align: left;
            }}

            .tabela th {{
                background-color: #2c3e50;
                color: white;
            }}

            .tabela tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}

            .tabela tr:hover {{
                background-color: #eef3f7;
            }}

            .chaves {{
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin-top: 10px;
            }}

            .chave {{
                background-color: #ecf0f1;
                color: #2c3e50;
                padding: 6px 10px;
                border-radius: 4px;
                font-size: 13px;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>Projeto 2 - Análise de Tabacarias</h1>
            <p>Aplicação web com dados públicos, acesso por chaves, dashboard, integridade e mapa.</p>
        </header>

        <main>
            <div class="card">
                <h2>Acesso aos dados</h2>
                <p>
                    Introduz uma chave para consultar dados restritos ou funcionalidades específicas.
                </p>

                <form method="POST">
                    <input type="password" name="chave" placeholder="Introduza a chave">
                    <button type="submit">Entrar</button>
                </form>

                <p class="erro">{mensagem}</p>
            </div>

            <div class="info">
                <strong>Secção atual:</strong> {titulo}
            </div>

            <div class="tabela-container">
                <h2>{titulo}</h2>
                {tabela_html}
            </div>
        </main>
    </body>
    </html>
    """