# 📊 Assistente Financeiro Corporativo (ERP)

Projeto Integrador em Engenharia da Computação focado na criação de um painel financeiro B2B seguro, interativo e orientado a dados.

## 🚀 Tecnologias Utilizadas
* **Front-end / Back-end:** Python com framework Streamlit
* **Banco de Dados:** SQLite (Embutido e Portátil)
* **Visualização de Dados:** Plotly Express (Gráficos interativos)
* **Manipulação de Dados:** Pandas

## ⚙️ Funcionalidades
- [x] Registro blindado contra *SQL Injection*.
- [x] Painel de KPIs dinâmico (Saúde Financeira em tempo real).
- [x] Filtragem temporal avançada (Mês/Ano).
- [x] Exportação de relatórios para CSV.
- [x] Gerenciador seguro para deleção de registros (via Chave Primária).

## 🛠️ Como executar na sua máquina

1. Clone este repositório:
`git clone https://github.com/SeuUsuario/assistente-financeiro-pi.git`

2. Crie e ative um ambiente virtual (Linux/Mac):
`python3 -m venv venv`
`source venv/bin/activate`

3. Instale as dependências:
`pip install -r requirements.txt`

4. Execute a aplicação:
`streamlit run app.py`