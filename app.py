import streamlit as st
import pandas as pd
import plotly.express as px
import database
from datetime import datetime, timedelta, timezone

fuso_br = timezone(timedelta(hours=-3))

# A Regra de Ouro: Page Config sempre no topo absoluto!
st.set_page_config(page_title="ERP - Gestão Financeira", layout="wide", initial_sidebar_state="expanded")

# --- 1. O CRACHÁ DE ACESSO (SESSION STATE) ---
if 'usuario_logado' not in st.session_state:
    st.session_state['usuario_logado'] = None

# --- 2. A PORTA DA RUA (TELA DE LOGIN) ---
if st.session_state['usuario_logado'] is None:
    st.title("🔐 Acesso Restrito")
    st.markdown("Bem-vindo ao **Finança Fácil Pessoal**. Identifique-se para entrar.")
    
    with st.container():
        # .lower() evita que o usuário erre a senha por causa de letra maiúscula
        usuario_input = st.text_input("Nome de Usuário").strip().lower() 
        senha_input = st.text_input("Senha", type="password")
        
        if st.button("Entrar", key="btn_login"):
            # Dicionário de usuários provisório (No futuro, isso pode ir para o banco)
            usuarios_permitidos = {"gabriel": "admin123", "joao": "senha1"}
            
            if usuario_input in usuarios_permitidos and usuarios_permitidos[usuario_input] == senha_input:
                st.session_state['usuario_logado'] = usuario_input
                st.rerun() # Destranca a porta e recarrega a página
            else:
                st.error("⚠️ Usuário ou senha incorretos.")

    # --- BOTÃO NUCLEAR TEMPORÁRIO ---
        st.markdown("---")
        if st.button("🚨 RESETAR BANCO DE DADOS DA NUVEM"):
            import os
            if os.path.exists('financas.db'):
                os.remove('financas.db')
                st.success("💥 Banco antigo destruído! Dê F5 na página para recriar o novo.")
            else:
                st.info("O banco já não existe mais aqui.")

# --- 3. O SISTEMA (ESCRITÓRIO INTERNO) ---
else:
    usuario_atual = st.session_state['usuario_logado']
    
    # Configuração corporativa da página
    st.markdown("""
        <meta name="google" content="notranslate">
        <meta http-equiv="Content-Language" content="pt-br">
    """, unsafe_allow_html=True)

    # Botão de Sair no topo direito
    col_espaco, col_sair = st.columns([0.85, 0.15])
    with col_sair:
        if st.button("🚪 Sair", key="btn_sair"):
            st.session_state['usuario_logado'] = None
            st.rerun()
            
    st.title(f"Finança Fácil - Painel de {usuario_atual.capitalize()} 📊")
    st.markdown("---")

    # --- INICIALIZAÇÃO DO BANCO DE DADOS E ALERTAS ---
    database.criar_tabela_lembretes()
    database.criar_tabelas()

    # CORREÇÃO: Puxando apenas os dados do usuário atual!
    lembretes_df = database.buscar_lembretes(usuario_atual)
    df = database.buscar_transacoes(usuario_atual)

    # Sistema de Alertas no topo
    if not lembretes_df.empty:
        # Convertendo a data para cálculo
        lembretes_df['data_vencimento'] = pd.to_datetime(lembretes_df['data_vencimento']).dt.date
        hoje = datetime.now(fuso_br).date()
        
        alertas = []
        for _, row in lembretes_df.iterrows():
            dias_para_vencer = (row['data_vencimento'] - hoje).days
            
            if dias_para_vencer < 0:
                alertas.append(f"🚨 **ATRASADO:** {row['titulo']} venceu há {abs(dias_para_vencer)} dias!")
            elif 0 <= dias_para_vencer <= 3:
                alertas.append(f"⚠️ **URGENTE:** {row['titulo']} vence em {dias_para_vencer} dias!")

        for alerta in alertas:
            if "🚨" in alerta:
                st.error(alerta)
            else:
                st.warning(alerta)

    # ==========================================
    # MENU LATERAL (FILTROS E EXPORTAÇÃO)
    # ==========================================
    with st.sidebar:
        st.markdown("---")
        st.subheader("📅 Agendar Pagamento/Recibo")
        
        with st.expander("Novo Lembrete"):
            titulo_l = st.text_input("O que pagar/receber?")
            valor_texto = st.text_input("Valor Estimado", placeholder="Ex: 1.500,50")
            data_l = st.date_input("Data Limite", datetime.now(fuso_br).date(), format="DD/MM/YYYY", key="input_data_limite_nova")
            
            # CORREÇÃO: Lógica do botão fundida em um bloco só
            if st.button("Agendar", key="botao_agendar_lembrete"):
                try:
                    valor_l = float(valor_texto.replace('.', '').replace(',', '.'))
                    # CORREÇÃO: Enviando o usuario_atual para o banco
                    database.inserir_lembrete(usuario_atual, titulo_l, valor_l, data_l)
                    st.success("Agendado!")
                    st.rerun()
                except ValueError:
                    st.error("Por favor, digite um valor financeiro válido.")

        # Listagem interativa de lembretes
        if not lembretes_df.empty:
            st.markdown("**📌 Próximos Compromissos:**")
            
            for _, row in lembretes_df.iterrows():
                data_formatada = row['data_vencimento'].strftime('%d/%m/%Y')
                
                col_texto, col_pago, col_del = st.columns([0.65, 0.15, 0.20])
                
                with col_texto:
                    valor_br = f"{row['valor']:_.2f}".replace('.', ',').replace('_', '.')
                    st.write(f"**{data_formatada}**\n{row['titulo']} (R$ {valor_br})")
                            
                with col_pago:
                    if st.button("✔️", key=f"pagar_{row['id']}", help="Marcar como Pago (Move para o Caixa)"):
                        # CORREÇÃO: Enviando usuario_atual para ambas as tabelas
                        database.inserir_transacao(usuario_atual, 'Despesa', 'Compromisso', row['titulo'], row['valor'], row['data_vencimento'])
                        database.excluir_lembrete(row['id'], usuario_atual)
                        st.rerun()
                        
                with col_del:
                    if st.button("🗑️", key=f"del_{row['id']}", help="Excluir Lembrete"):
                        # CORREÇÃO: Enviando usuario_atual
                        database.excluir_lembrete(row['id'], usuario_atual)
                        st.rerun()
                        
                st.divider()

        st.header("🔍 Filtros de Análise")

        # Filtros e Exportação
        if not df.empty:
            df['data'] = pd.to_datetime(df['data'])
                
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
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Baixar Relatório (CSV)",
                data=csv,
                file_name=f"relatorio_financeiro_{usuario_atual}.csv",
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
            data_transacao = st.date_input("Data de Competência", datetime.now(fuso_br).date(), format="DD/MM/YYYY", key="input_data_competencia")
            
            submit = st.form_submit_button("Salvar Registro")
            
            if submit:
                try:
                    valor_limpo = valor_str.replace('R$', '').replace(' ', '').replace('.', '').replace(',', '.')
                    valor_final = float(valor_limpo)
                    if valor_final <= 0:
                        st.error("O valor deve ser maior que zero.")
                    else:
                        # CORREÇÃO: Inserindo transação com usuario_atual
                        database.inserir_transacao(usuario_atual, tipo, categoria, descricao, valor_final, data_transacao)
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
            
            df_display = df.copy()
            df_display['data'] = df_display['data'].dt.strftime('%d/%m/%Y')
            
            # Removemos a coluna Usuario na hora de mostrar na tela para ficar mais limpo
            if 'usuario' in df_display.columns:
                df_display = df_display.drop(columns=['usuario'])
                
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
                        # CORREÇÃO: Enviando usuario_atual para garantir segurança
                        database.excluir_transacao(id_selecionado, usuario_atual)
                        st.success(f"Registro ID {id_selecionado} vaporizado com sucesso!")
                        st.rerun()
        else:
            st.info("Nenhum dado encontrado para o período selecionado.")