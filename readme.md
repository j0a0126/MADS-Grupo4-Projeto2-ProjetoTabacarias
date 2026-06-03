# Análise de Dados sobre Tabacarias

Aplicação web em Flask que lê dados de um Google Sheets e apresenta tabelas, mapa interativo, dashboard e validação de dados, com controlo de acesso por chaves.

Projeto disponível na plataforma Render.com: [https://mads-grupo4-projeto2-projetotabacarias.onrender.com]  
As chaves de acesso aos dados privados estão disponíveis neste README e no relatório do projeto.

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

- Python 3.14
- Acesso ao Google Cloud Console
- Google Sheets partilhado com a conta de serviço
- Ficheiro JSON com as credenciais do Google
---

## Base de dados

A base de dados utilizada no projeto está guardada num Google Sheets com o nome:

```text
[https://docs.google.com/spreadsheets/d/1b46eM_6bjc4iFWT81PKz-_Pm3BeFfQqSH6TfScM7yJs/edit?usp=sharing]
```

Este ficheiro contém as seguintes folhas:

| Folha | Descrição |
|---|---|
| `utilizadores` | Dados dos utilizadores registados |
| `categoriasTabacarias` | Categorias das tabacarias |
| `tabacarias` | Dados públicos das tabacarias |
| `vendas` | Registo das vendas realizadas |

---

## Chaves de acesso

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

#
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
    ├── credenciais_google.json    # Credenciais Google 
    └── chave.json                 # Chaves de acesso 
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

## Autores

João Azevedo  
João Serrano  
Gustavo Rodrigues  
Pedro Pires  

**Unidade Curricular:** Metodologias Ágeis de Desenvolvimento de Software  
**Projeto:** Projeto 2 — Tabacarias  
**Instituição:** IPMAIA  
**Data:** 2026
