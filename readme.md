# Análise de Dados sobre Tabacarias

Aplicação web em Flask que lê dados de um Google Sheets e apresenta tabelas, mapa interativo, dashboard e validação de dados, com controlo de acesso por chaves.

Este projeto foi desenvolvido no âmbito da unidade curricular de **Metodologias Ágeis de Desenvolvimento de Software**, dando continuidade ao Projeto 1 sobre gestão e análise de tabacarias.

> Projeto disponível na plataforma Render.com: [colocar aqui o link do projeto]  
> As chaves de acesso aos dados privados estão disponíveis neste README e no relatório do projeto.

> ⚠️ Desenvolvido com apoio de ferramentas de inteligência artificial, incluindo ChatGPT e outras ferramentas de apoio à programação.

---

## Funcionalidades

| Módulo | Descrição |
|---|---|
| **Tabelas** | Apresentação dos dados de tabacarias, utilizadores, vendas e categorias |
| **Mapa** | Mapa interativo com a localização das tabacarias, gerado com `folium` |
| **Dashboard** | Gráficos e estatísticas sobre vendas com `pandas` + `plotly` |
| **Integridade** | Validação automática dos dados com relatório de erros |
| **Acesso** | Controlo de acesso através de chaves configuradas em `secrets/chave.json` |

---

## Pré-requisitos

- Python 3.7+
- Conta Google
- Acesso ao Google Cloud Console
- Google Sheets partilhado com a conta de serviço
- Ficheiro JSON com as credenciais do Google
- Conta GitHub
- Conta Render.com, caso se pretenda publicar o projeto online

---

## Instalação

```bash
# 1. Entrar na pasta do projeto
cd Projeto2_Tabacarias

# 2. Criar e ativar ambiente virtual
python -m venv venv

# Windows
venv\Scripts\activate

# 3. Instalar dependências
pip install -r requirements.txt
```

---

## Configuração

### 1. Credenciais do Google

No Google Cloud Console:

1. Criar um projeto.
2. Ativar a **Google Sheets API**.
3. Ativar a **Google Drive API**.
4. Criar uma **conta de serviço**.
5. Descarregar o ficheiro JSON das credenciais.
6. Guardar o ficheiro na pasta `secrets/`.
7. Renomear o ficheiro para:

```text
credenciais_google.json
```

Depois, abrir o ficheiro JSON e copiar o email presente em:

```json
"client_email": "..."
```

Esse email deve ser adicionado como **Editor** no Google Sheets usado como base de dados.

No ficheiro `app.py`, a ligação ao Google Sheets é feita através de:

```python
gc = pygsheets.authorize(service_file=service_file_path)
sheet = gc.open("BaseDados_Tabacarias")
```

---

## Base de dados

A base de dados utilizada no projeto está guardada num Google Sheets com o nome:

```text
BaseDados_Tabacarias
```

Este ficheiro contém as seguintes folhas:

| Folha | Descrição |
|---|---|
| `utilizadores` | Dados dos utilizadores registados |
| `categoriasTabacarias` | Categorias das tabacarias |
| `tabacarias` | Dados públicos das tabacarias |
| `vendas` | Registo das vendas realizadas |

---

## Estrutura das tabelas

### `utilizadores`

```text
NIF | Nome | DataNascimento | Genero | CriadoEm
```

### `categoriasTabacarias`

```text
Nome | Cor
```

### `tabacarias`

```text
NIF | Nome | Categoria | Latitude | Longitude | Morada | Cidade | CodigoPostal | Horario | CriadoEm
```

### `vendas`

```text
ID | NIF_Utilizador | NIF_Tabacaria | Valor | Descricao | Data | Categoria_Venda
```

---

## Chaves de acesso

O acesso às diferentes áreas da aplicação é feito através de chaves configuradas no ficheiro:

```text
secrets/chave.json
```

O ficheiro deve ter o seguinte formato:

```json
{
  "tabacarias": "tabacarias",
  "utilizadores": "utilizadores",
  "categorias": "categoriasTabacarias",
  "vendas": "vendas",
  "integridade": "integridade",
  "dashboard": "dashboard",
  "mapa": "mapa"
}
```

### Chaves disponíveis

| Chave | Conteúdo apresentado |
|---|---|
| `tabacarias` | Lista de tabacarias |
| `utilizadores` | Lista de utilizadores |
| `categorias` | Lista de categorias das tabacarias |
| `vendas` | Lista de vendas |
| `integridade` | Relatório de integridade dos dados |
| `dashboard` | Dashboard com gráficos e estatísticas |
| `mapa` | Mapa interativo das tabacarias |

---

## Variáveis de ambiente

Criar um ficheiro `.env` na raiz do projeto:

```env
isProduction=false
```

Em ambiente de produção, como no Render.com, definir:

```env
isProduction=true
```

Quando `isProduction=true`, a aplicação procura os ficheiros secretos em:

```text
/etc/secrets/
```

Quando `isProduction=false`, a aplicação procura os ficheiros na pasta local:

```text
secrets/
```

---

## Execução

### Desenvolvimento local

```bash
python app.py
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:5000
```

---

## Produção no Render

Para publicar no Render.com:

1. Criar um repositório GitHub com o projeto.
2. Criar um novo **Web Service** no Render.
3. Ligar o Render ao repositório GitHub.
4. Configurar os comandos:

```text
Build command:
pip install -r requirements.txt
```

```text
Start command:
python app.py
```

5. Adicionar a variável de ambiente:

```text
isProduction=true
```

6. Adicionar os ficheiros secretos:

```text
credenciais_google.json
chave.json
```

Estes ficheiros devem ficar disponíveis em:

```text
/etc/secrets/
```

---

## Estrutura do projeto

```text
├── app.py                         # Aplicação Flask principal
├── templates.py                   # Geração das páginas HTML
├── integridade.py                 # Validação dos dados
├── dashboard.py                   # Dashboard e gráficos
├── mapa.py                        # Mapa interativo com Folium
├── requirements.txt               # Dependências do projeto
├── readme.md                      # Documentação do projeto
├── .env                           # Variáveis de ambiente
├── .gitignore                     # Ficheiros ignorados pelo Git
└── secrets/
    ├── credenciais_google.json    # Credenciais Google ⚠️ não incluir no GitHub
    └── chave.json                 # Chaves de acesso ⚠️ não incluir no GitHub
```

---

## Validações de integridade

A página de integridade verifica automaticamente a qualidade dos dados existentes nas tabelas.

### Todas as tabelas

- Tabelas vazias
- Cabeçalhos vazios
- Colunas duplicadas
- Campos obrigatórios em falta

### Utilizadores

- NIF vazio
- NIF duplicado
- Nome vazio
- Género inválido

### Categorias de tabacarias

- Categoria sem nome
- Categorias duplicadas

### Tabacarias

- NIF vazio
- NIF duplicado
- Nome vazio
- Categoria inexistente
- Latitude inválida
- Longitude inválida
- Horário vazio

### Vendas

- Venda sem ID
- ID duplicado
- Valor inválido
- Valor menor ou igual a zero
- Venda associada a utilizador inexistente
- Venda associada a tabacaria inexistente
- Categoria de venda inválida

---

## Dashboard

O dashboard apresenta estatísticas e gráficos sobre as vendas das tabacarias.

Inclui:

- Total de vendas
- Número total de tabacarias
- Número total de vendas registadas
- Gráfico de valor total de vendas por tabacaria
- Gráfico de vendas por descrição
- Gráfico de evolução das vendas por data
- Gráfico de vendas por categoria

---

## Mapa

A aplicação inclui um mapa interativo com a localização das tabacarias.

Cada marcador apresenta:

- Nome da tabacaria
- Morada
- Cidade
- Horário
- Categoria

O mapa é gerado através da biblioteca:

```text
folium
```

---

## Controlo de versões

O projeto utiliza Git e GitHub para controlo de versões.

Antes de enviar para o GitHub, deve existir um ficheiro `.gitignore` com:

```gitignore
venv/
__pycache__/
.env
secrets/
*.pyc
```

A pasta `secrets/` não deve ser enviada para o GitHub, pois contém credenciais privadas.

---

## Testes realizados

Foram realizados testes manuais às principais funcionalidades:

| Teste | Resultado esperado |
|---|---|
| Abrir a aplicação sem chave | Mostra a tabela pública das tabacarias |
| Inserir chave inválida | Mostra mensagem de erro |
| Inserir `utilizadores` | Mostra a tabela de utilizadores |
| Inserir `categorias` | Mostra a tabela de categorias |
| Inserir `vendas` | Mostra a tabela de vendas |
| Inserir `integridade` | Mostra relatório de validação |
| Inserir `dashboard` | Mostra gráficos e estatísticas |
| Inserir `mapa` | Mostra mapa interativo |

---

## Tecnologias utilizadas

- Python
- Flask
- Pandas
- Pygsheets
- Google Sheets API
- Google Drive API
- Plotly
- Folium
- HTML/CSS
- GitHub
- Render.com

---

## Entrega final

A entrega final do projeto inclui:

- Aplicação Flask funcional
- Google Sheets configurado como base de dados
- Sistema de acesso por chaves
- Landing page pública
- Tabelas privadas
- Página de integridade dos dados
- Dashboard estatístico
- Mapa interativo das tabacarias
- Repositório GitHub
- Deploy no Render.com
- README atualizado
- Diário de Projeto atualizado

---

## Autores

João Azevedo  
João Serrano  
Gustavo Rodrigues  
Pedro Pires  

**Unidade Curricular:** Metodologias Ágeis de Desenvolvimento de Software  
**Projeto:** Projeto 2 — Tabacarias  
**Instituição:** IPMAIA  
**Data:** 2026
