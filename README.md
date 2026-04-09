<div align="center">
<pre> 
      ___           ___                                    ___           ___           ___   
     /__/\         /__/\        ___           ___         /  /\         /  /\         /  /\  
     \  \:\        \  \:\      /  /\         /__/\       /  /:/_       /  /:/_       /  /::\ 
      \  \:\        \  \:\    /  /:/         \  \:\     /  /:/ /\     /  /:/ /\     /  /:/\:\
  ___  \  \:\   _____\__\:\  /__/::\          \  \:\   /  /:/ /:/_   /  /:/ /::\   /  /:/~/:/
 /__/\  \__\:\ /__/::::::::\ \__\/\:\__   ___  \__\:\ /__/:/ /:/ /\ /__/:/ /:/\:\ /__/:/ /:/ 
 \  \:\ /  /:/ \  \:\~~\~~\/    \  \:\/\ /__/\ |  |:| \  \:\/:/ /:/ \  \:\/:/~/:/ \  \:\/:/  
  \  \:\  /:/   \  \:\  ~~~      \__\::/ \  \:\|  |:|  \  \::/ /:/   \  \::/ /:/   \  \::/   
   \  \:\/:/     \  \:\          /__/:/   \  \:\__|:|   \  \:\/:/     \__\/ /:/     \  \:\   
    \  \::/       \  \:\         \__\/     \__\::::/     \  \::/        /__/:/       \  \:\  
     \__\/         \__\/                       ~~~~       \__\/         \__\/         \__\/  
 </pre></div>  

# Assistente Financeiro PI

Aplicação web desenvolvida em **Python + Streamlit** para **registro, consulta e análise de movimentações financeiras** em um contexto de **Projeto Integrador**. O sistema utiliza **SQLite** como banco de dados local e oferece uma interface simples para cadastro de receitas e despesas, visualização de indicadores, filtros temporais, gráficos interativos e exportação de dados em CSV.

> **Status do projeto:** MVP acadêmico funcional.

---

## Sumário

- [Visão geral](#visão-geral)
- [Objetivos do projeto](#objetivos-do-projeto)
- [Escopo implementado](#escopo-implementado)
- [Arquitetura da solução](#arquitetura-da-solução)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Tecnologias utilizadas](#tecnologias-utilizadas)
- [Modelo de dados](#modelo-de-dados)
- [Fluxo de funcionamento](#fluxo-de-funcionamento)
- [Funcionalidades](#funcionalidades)
- [Regras de validação](#regras-de-validação)
- [Segurança e boas práticas já aplicadas](#segurança-e-boas-práticas-já-aplicadas)
- [Limitações atuais](#limitações-atuais)
- [Como executar o projeto](#como-executar-o-projeto)
- [Como testar](#como-testar)
- [Licença e autoria](#licença-e-autoria)

---

## Visão geral

O **Assistente Financeiro PI** foi desenvolvido para centralizar o controle básico de movimentações financeiras em uma interface visual e objetiva. A proposta do projeto é permitir que o usuário:

- registre **receitas** e **despesas**;
- categorize lançamentos;
- acompanhe indicadores financeiros consolidados;
- filtre dados por **ano** e **mês**;
- visualize gráficos de distribuição e fluxo de caixa;
- exporte os registros para **CSV**;
- exclua registros existentes a partir do identificador do lançamento.

A aplicação foi construída com foco em **simplicidade de uso**, **portabilidade** e **rapidez de implementação**, sendo adequada para fins acadêmicos, prototipação e evolução futura.

---

## Objetivos do projeto

Este projeto busca demonstrar, de forma prática, conceitos importantes de desenvolvimento de software aplicados a um cenário financeiro, incluindo:

- construção de interface interativa com **Streamlit**;
- persistência de dados com **SQLite**;
- manipulação e análise com **Pandas**;
- visualização com **Plotly Express**;
- separação básica entre camada de interface e camada de acesso a dados.

---

## Escopo implementado

O projeto atualmente cobre o seguinte escopo funcional:

| Área | Implementação atual |
|---|---|
| Cadastro | Registro de receitas e despesas com categoria, descrição, valor e data |
| Persistência | Armazenamento local em banco SQLite |
| Visualização | KPIs de receitas, despesas e saldo |
| Filtros | Consulta por ano e mês |
| Relatórios | Tabela com histórico das transações |
| Gráficos | Pizza por categoria de despesa e barras para fluxo de caixa |
| Exportação | Geração de arquivo CSV a partir do conjunto filtrado |
| Exclusão | Remoção de registros por ID |

---

## Arquitetura da solução

A aplicação segue uma arquitetura simples, adequada para um MVP:

### 1. Camada de interface
Responsável por toda a experiência do usuário dentro do Streamlit:
- formulário de cadastro;
- filtros laterais;
- exibição de KPIs;
- gráficos interativos;
- tabela de histórico;
- botão de exportação;
- gerenciamento de exclusão.

### 2. Camada de dados
Responsável por:
- abrir conexão com o banco SQLite;
- criar a tabela principal;
- inserir registros;
- consultar transações;
- excluir registros.

### 3. Camada de teste inicial
Um script simples de verificação do banco (`teste.py`) é utilizado para criar as tabelas e validar a inicialização básica do projeto.

---

## Estrutura do repositório

```text
Assistente-financeiro-PI/
├── .devcontainer/
├── .gitignore
├── README.md
├── app.py
├── database.py
├── requirements.txt
└── teste.py
```

### Descrição dos arquivos principais

| Arquivo | Responsabilidade |
|---|---|
| `app.py` | Interface principal da aplicação, filtros, KPIs, gráficos, tabela, exportação e exclusão |
| `database.py` | Conexão com SQLite, criação de tabela e operações básicas de persistência |
| `teste.py` | Script simples para inicialização/validação do banco |
| `requirements.txt` | Dependências Python do projeto |
| `.devcontainer/` | Configuração do ambiente de desenvolvimento em contêiner |

---

## Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python | Linguagem principal do projeto |
| Streamlit | Construção da interface web interativa |
| SQLite | Banco de dados local e embarcado |
| Pandas | Manipulação e filtragem de dados |
| Plotly Express | Criação de gráficos interativos |

### Dependências principais

As dependências instaladas incluem, entre outras, os pacotes:

- `streamlit`
- `pandas`
- `plotly`
- `numpy`
- `GitPython`
- dependências transitivas do ecossistema Streamlit/Plotly

---

## Modelo de dados

A aplicação utiliza uma tabela principal chamada `transacoes`.

### Estrutura da tabela

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | `INTEGER PRIMARY KEY AUTOINCREMENT` | Identificador único do lançamento |
| `tipo` | `TEXT NOT NULL` | Define se a movimentação é `Receita` ou `Despesa` |
| `categoria` | `TEXT NOT NULL` | Classificação da movimentação |
| `descricao` | `TEXT` | Observação opcional sobre o lançamento |
| `valor` | `REAL NOT NULL` | Valor monetário do lançamento |
| `data` | `DATE NOT NULL` | Data de competência da transação |

### Categorias atualmente disponíveis

- Folha de Pagamento
- Infraestrutura e TI
- Impostos e Taxas
- Marketing
- Vendas e Serviços
- Manutenção
- Outros

---

## Fluxo de funcionamento

O comportamento atual da aplicação segue este fluxo:

1. Ao iniciar, a aplicação configura a página e garante a criação da tabela no banco.
2. Em seguida, todos os registros são carregados do SQLite.
3. No menu lateral, o usuário pode filtrar os dados por ano e mês.
4. O formulário principal permite registrar uma nova movimentação.
5. Após o cadastro, os dados são persistidos e a interface é recarregada.
6. O painel exibe KPIs, gráficos e histórico com base nos filtros aplicados.
7. O usuário pode exportar o conjunto filtrado em CSV.
8. Também é possível excluir um lançamento existente a partir do ID.

---

## Funcionalidades

### Cadastro de lançamentos
- Registro de **receitas** e **despesas**.
- Entrada de categoria, descrição, valor e data.
- Conversão de valor monetário digitado no padrão brasileiro para `float`.

### Indicadores financeiros
- Total de receitas.
- Total de despesas.
- Saldo em caixa.

### Filtros temporais
- Filtro por **ano**.
- Filtro por **mês**.
- Aplicação dos filtros na análise, tabela e exportação.

### Visualização analítica
- **Gráfico de pizza** para distribuição de despesas por categoria.
- **Gráfico de barras** para consolidação de receitas e despesas.
- **Tabela** com histórico de transações formatada para exibição.

### Exportação
- Download dos dados filtrados em arquivo **CSV**.

### Gerenciamento de registros
- Exclusão de um lançamento a partir do **ID** selecionado.

---

## Regras de validação

O código atual já aplica algumas validações importantes:

| Regra | Comportamento |
|---|---|
| Valor obrigatório | O campo deve ser preenchido em formato numérico válido |
| Valor positivo | O sistema impede o cadastro de valores menores ou iguais a zero |
| Tipo de movimentação | Limitado às opções `Receita` e `Despesa` na interface |
| Categoria | Limitada às opções definidas no formulário |
| Data | Selecionada por componente próprio do Streamlit |

---

## Segurança e boas práticas já aplicadas

Mesmo sendo um projeto enxuto, o código já adota algumas práticas positivas:

### Consultas parametrizadas no SQLite
As operações de inserção e exclusão utilizam parâmetros no SQL, reduzindo o risco de **SQL Injection**.

### Separação básica de responsabilidades
- `app.py` cuida da interface e da experiência do usuário.
- `database.py` centraliza o acesso ao banco.

### Banco local simples de distribuir
O uso de SQLite facilita execução local, testes rápidos e prototipação sem infraestrutura externa.

---

## Limitações atuais

Para deixar a documentação honesta e profissional, é importante registrar as limitações observadas na implementação atual:

| Ponto | Situação atual | Impacto |
|---|---|---|
| Precisão monetária | O campo `valor` usa `REAL` | Pode gerar imprecisão para operações financeiras mais rigorosas |
| Indicador visual de saúde | O saldo é exibido como KPI, mas o “semáforo” visual não está efetivamente implementado | A interface não diferencia visualmente saldo positivo e negativo |
| Escalabilidade | A consulta traz todos os registros e os filtros são aplicados depois no Pandas | Pode perder eficiência com base de dados maior |
| Segurança de acesso | Não há autenticação nem controle de perfis | Projeto adequado para uso local/protótipo, não para operação corporativa real |
| Auditoria | Não há trilha de alterações ou logs de operação | Dificulta rastreabilidade |
| Edição de registros | Há exclusão, mas não existe edição de lançamentos | Limita manutenção de dados |
| Testes | Não há suíte automatizada de testes, apenas um script simples de inicialização | Cobertura de qualidade ainda inicial |

---

## Como executar o projeto

### Pré-requisitos

- Python 3 instalado
- `pip` disponível no ambiente

### 1. Clonar o repositório

```bash
git clone https://github.com/Gabriel-Silva-eng/Assistente-financeiro-PI.git
cd Assistente-financeiro-PI
```

### 2. Criar e ativar ambiente virtual

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows (PowerShell)

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Executar a aplicação

```bash
streamlit run app.py
```

Após a execução, o Streamlit abrirá a aplicação em ambiente local no navegador.

---

## Como testar

O repositório possui um teste inicial simples para criação da estrutura do banco:

```bash
python teste.py
```

Esse script executa a criação das tabelas e imprime uma mensagem de sucesso caso a inicialização ocorra corretamente.

> Observação: este script funciona como um **smoke test** inicial, mas ainda não substitui uma suíte de testes automatizados.

---

## Licença e autoria

Projeto desenvolvido para fins acadêmicos como **Projeto Integrador em Engenharia da Computação da UNIVESP**.

| Nome | RA | Papel |
|------|----|-------|
| Gabriel Siqueira Silva | 24200844 | Líder / Scrum Master |
| Raoni Kirschner Sava | 24218257 | Dev Back-end |
| Gabriele Cristine Ribeiro Aluvino | 24211510 | Dev Back-end |
| Lucas Rabelo Fabiano | 24219010 | Dev Front-end |
| Nelson de Paula Santos Júnior | 24206410 | Dev Front-end / Gráficos |
| Rafael José Benedito da Conceição | 24204145 | Documentação / QA |
| Reginaldo Francisco Pedrosa | 24217557 | QA / Testes |
| Reinaldo Samuel de Souza Silva | 24211225 | QA / Testes |

---

## Resumo executivo

O **Assistente Financeiro PI** é um projeto acadêmico funcional que demonstra, de forma objetiva, a construção de um painel financeiro com cadastro, consulta, análise visual e persistência local. A solução é adequada como MVP e como base de aprendizado em desenvolvimento full stack com Python, Streamlit e SQLite, mantendo espaço claro para evolução arquitetural, segurança, testes e escalabilidade.
