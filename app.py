import streamlit as st
import pandas as pd
import plotly.express as px
import database
from datetime import date

# Configuração corporativa da página
st.set_page_config(page_title="ERP - Gestão Financeira", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <meta name="google" content="notranslate">
    <meta http-equiv="Content-Language" content="pt-br">
""", unsafe_allow_html=True)

st.title("Finança Fácil - Assistente Financeiro")
st.markdown("---")

# --- INICIALIZAÇÃO E ALERTAS ---
database.criar_tabela_lembretes()
lembretes_df = database.buscar_lembretes()

if not lembretes_df.empty:
    # Convertendo a data para cálculo
    lembretes_df['data_vencimento'] = pd.to_datetime(lembretes_df['data_vencimento']).dt.date
    hoje = date.today()
    
    alertas = []
    for _, row in lembretes_df.iterrows():
        dias_para_vencer = (row['data_vencimento'] - hoje).days
        
        #  Notificação:
        if dias_para_vencer < 0:
            alertas.append(f"🚨 **ATRASADO:** {row['titulo']} venceu há {abs(dias_para_vencer)} dias!")
        elif 0 <= dias_para_vencer <= 3:
            alertas.append(f"⚠️ **URGENTE:** {row['titulo']} vence em {dias_para_vencer} dias!")

    # alertas
    for alerta in alertas:
        if "🚨" in alerta:
            st.error(alerta)
        else:
            st.warning(alerta)

database.criar_tabelas()

df = database.buscar_transacoes()

# ==========================================
# MENU LATERAL (FILTROS E EXPORTAÇÃO)
# ==========================================
with st.sidebar:
    st.markdown("---")
    st.subheader("📅 Agendar Pagamento/Recibo")
    with st.expander("Novo Lembrete"):
        titulo_l = st.text_input("O que pagar/receber?")
        valor_l = st.number_input("Valor Estimado", min_value=0.0)
        data_l = st.date_input("Data Limite", date.today())
        if st.button("Agendar"):
            database.inserir_lembrete(titulo_l, valor_l, data_l)
            st.success("Agendado!")
            st.rerun()

    # Listagem rápida de lembretes no menu lateral
    if not lembretes_df.empty:
        st.markdown("**Próximos Compromissos:**")
        for _, row in lembretes_df.head(5).iterrows():
            st.caption(f"📌 {row['data_vencimento'].strftime('%d/%m')} - {row['titulo']}")
        st.header("🎛️ Filtros de Análise")
    
    if not df.empty:

        df['data'] = pd.to_datetime(df['data'])
        
        # Filtros Dinâmicos 
        anos = df['data'].dt.year.unique().tolist()
        ano_selecionado = st.selectbox("Filtrar por Ano", ["Todos os Anos"] + anos)
        
        meses = df['data'].dt.month.unique().tolist()
        mes_selecionado = st.selectbox("Filtrar por Mês", ["Todos os Meses"] + meses)
        
        if ano_selecionado != "Todos os Anos":
            df = df[df['data'].dt.year == ano_selecionado]
        if mes_selecionado != "Todos os Meses":
            df = df[df['data'].dt.month == mes_selecionado]
            
        st.markdown("---")
        st.subheader("📥 Exportação")
        
        # Transformando DataFrame em um arquivo para Excel
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Baixar Relatório (CSV)",
            data=csv,
            file_name="relatorio_financeiro.csv",
            mime="text/csv"
        )
    else:
        st.info("Banco de dados vazio.")

# ==========================================
# INTERFACE PRINCIPAL
# ==========================================
col1, col2 = st.columns([1.2, 2.5])

with col1:
    st.subheader("Registrar Lançamento")
    with st.form("form_transacao", clear_on_submit=True):
        tipo = st.selectbox("Tipo de Movimentação", ["Despesa", "Receita"])
        categoria = st.selectbox("Centro de Custo / Categoria", [
            "Folha de Pagamento", "Infraestrutura e TI", "Impostos e Taxas", 
            "Marketing", "Vendas e Serviços", "Manutenção", "Outros"
        ])
        descricao = st.text_input("Descrição da Nota/Recibo")
        valor_str = st.text_input("Valor (R$)", placeholder="Ex: 1.500,50")
        data_transacao = st.date_input("Data de Competência", date.today())
        
        submit = st.form_submit_button("Salvar Registro")
        
        if submit:
            try:
                valor_limpo = valor_str.replace('R$', '').replace(' ', '').replace('.', '').replace(',', '.')
                valor_final = float(valor_limpo)
                if valor_final <= 0:
                    st.error("O valor deve ser maior que zero.")
                else:
                    database.inserir_transacao(tipo, categoria, descricao, valor_final, data_transacao)
                    st.success("Registro efetuado com sucesso!")

                    st.rerun() 
            except ValueError:
                st.error("Formato inválido. Digite apenas números e vírgula. Ex: 1500,50")

with col2:
    st.subheader("Visão Geral e Relatórios")
    
    if not df.empty:
        total_receitas = df[df['tipo'] == 'Receita']['valor'].sum()
        total_despesas = df[df['tipo'] == 'Despesa']['valor'].sum()
        saldo_caixa = total_receitas - total_despesas
        
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Total de Receitas", f"R$ {total_receitas:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
        kpi2.metric("Total de Despesas", f"R$ {total_despesas:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
        
        # ==========================================
        # INDICADOR VISUAL DE SAÚDE (Semáforo)
        # ==========================================
        cor_saldo = "🟢" if saldo_caixa >= 0 else "🔴"
        kpi3.metric("Saldo em Caixa", f"{cor_saldo} R$ {saldo_caixa:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        graf1, graf2 = st.columns(2)
        with graf1:
            df_despesas = df[df['tipo'] == 'Despesa']
            if not df_despesas.empty:
                fig_pie = px.pie(df_despesas, values='valor', names='categoria', title='Distribuição de Custos', hole=0.4)
                fig_pie.update_traces(hovertemplate='<b>%{label}</b><br>R$ %{value}<extra></extra>')
                st.plotly_chart(fig_pie, width='stretch')
        
        with graf2:
            df_grouped = df.groupby('tipo')['valor'].sum().reset_index()
            color_map = {'Receita': '#00CC96', 'Despesa': '#EF553B'}
            fig_bar = px.bar(df_grouped, x='tipo', y='valor', color='tipo', title='Fluxo de Caixa', color_discrete_map=color_map)
            fig_bar.update_traces(hovertemplate='<b>%{x}</b><br>R$ %{y}<extra></extra>')
            st.plotly_chart(fig_bar, width='stretch')

        st.subheader("Histórico de Transações")
        
        # Convertendo a data para o padrão brasileiro DD/MM/AAAA
        df_display = df.copy()
        df_display['data'] = df_display['data'].dt.strftime('%d/%m/%Y')
        df_display.columns = ['ID', 'Tipo', 'Categoria', 'Descrição', 'Valor (R$)', 'Data']
        st.dataframe(df_display, hide_index=True, width='stretch')
        
        st.markdown("---")
        st.subheader("⚙️ Gerenciamento de Registros")
        with st.expander("Excluir um lançamento"):
            lista_ids = df['id'].tolist()
            col_del1, col_del2 = st.columns([1, 2])
            with col_del1:
                id_selecionado = st.selectbox("Selecione o ID", lista_ids)
            with col_del2:
                st.write("") 
                st.write("")
                if st.button("🗑️ Excluir Permanentemente"):
                    database.excluir_transacao(id_selecionado)
                    st.success(f"Registro ID {id_selecionado} vaporizado com sucesso!")
                    st.rerun()
    else:
        st.info("Nenhum dado encontrado para o período selecionado.")
