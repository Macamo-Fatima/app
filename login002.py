import streamlit as st
import os
import pandas as pd
from io import BytesIO, StringIO
from decouple import config
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from csv import reader
import plotly.express as px
import xlsxwriter
from xlsxwriter.utility import xl_col_to_name

# Configuração da página
st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")
st.cache_data.clear()
# Configurar chave da OpenAI
os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')
# Estilização personalizada
st.markdown(
    """
    <style>
        /* Remover tema padrão do Streamlit */
        :root {
            --primary-color: #059669 !important;
            --background-color: white !important;
            --secondary-background-color: #f0f2f6 !important;
            --text-color: #064E3B !important;
        }
       
        /* Esconder menu e footer padrão */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Forçar fundo branco em todos os elementos */
        html, body, [class*="css"]  {
            background-color: #059669 !important;
            color: #064E3B !important;
        }
     
        /* Botões - Manter estilo original */
        div.stButton > button {
            background-color: #059669 !important;
            color: white !important;
        }

        div[data-baseweb="input"] {
            border: 1px solid #059669; /* Borda verde */
            border-radius: 4px;
        }        

        /* Desabilitar toggle de tema */
        [data-testid="stAppViewContainer"] > .main > .block-container {
            padding-top: 2rem;
        }
        [data-testid="baseButton-header"] {
            display: none !important;
        }

        .login-icon {
            font-size: 60px;
            color: #059669;
            text-align: center;
            display: block;
        }
          
       .login-button {
            background-color: #059669 !important;
            color: white !important;
            border-radius: 8px;
            width: 100%;
            font-size: 16px;
            padding: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Adiciona a ocultação do menu padrão
hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        button[title="View fullscreen"] {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Configurar autenticação na sessão
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Função de login
def login():
    with st.container():
        with st.form(key="user_form"):
            st.title("🔐 Login no Sistema")
            username = st.text_input("📧 Email:", placeholder="Digite seu email")
            password = st.text_input("🔑 Senha:", type="password", placeholder="Digite sua senha", help="Use 'admin@email.com' e senha '123456' para testar.")
            login_button = st.form_submit_button(label="Entrar no sistema", help="Clique para acessar sua conta")

            if login_button:
                # Validação dos campos obrigatórios
                if  username == "" or password == "":
                    st.error("⚠️ Todos campos são obrigatórios!")
                else:
                    # Validar login no banco de dados
                    if username == "suporte@hire.co.mz" and password == "2020Eraumavez":
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.rerun()  # Atualiza a página para aplicar a autenticação
                    else:
                        st.error("❌ Credenciais inválidas!")

# Se o usuário não estiver autenticado, exibir login
if not st.session_state.authenticated:
    login()
    st.stop()  # Impede que o restante do código seja executado
else:
        
    # Estilização personalizada
    st.markdown(
        """
        <style>
            /* Remover tema padrão do Streamlit */
            :root {
                --primary-color: #059669 !important;
                --background-color: white !important;
                --secondary-background-color: #f0f2f6 !important;
                --text-color: #064E3B !important;
            }

            /* Esconder menu e footer padrão */
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            
            /* Forçar fundo branco em todos os elementos */
            html, body, [class*="css"]  {
                background-color: white !important;
                color: #064E3B !important;
            }

            /* Sidebar - Manter estilo mas garantir fundo branco */
            section[data-testid="stSidebar"] {
                background-color: rgba(5, 150, 105, 0.10) !important;
                border-right: 1px solid #e0e0e0 !important;
            }

            /* Dataframes e tabelas */
            .stDataFrame {
                background-color: white !important;
                border: 1px solid #e0e0e0 !important;
            }

            /* Gráficos - Forçar estilo branco */
            .stPlotlyChart, .stPyplot {
                background-color: white !important;
                border: 1px solid #e0e0e0 !important;
                border-radius: 8px;
                padding: 10px;
            }

            /* Botões - Manter estilo original */
            div.stButton > button {
                background-color: #059669 !important;
                color: white !important;
            }

        
            div[data-baseweb="input"] {
                border: 1px solid #059669; /* Borda verde */
                border-radius: 4px;
            }        

            /* Desabilitar toggle de tema */
            [data-testid="stAppViewContainer"] > .main > .block-container {
                padding-top: 2rem;
            }
            [data-testid="baseButton-header"] {
                display: none !important;
            }

            
            /* Muda a cor da bolinha do radio button quando selecionado */
            div[data-testid="stRadio"] div[role="radiogroup"] label span {
                background-color: #059669 !important;
                border-color: #059669 !important;
            }

            /* Muda a cor da marca dentro do checkbox */
            div[data-testid="stCheckbox"] div[role="checkbox"] {
                background-color: #059669 !important;
                border-color: #059669 !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Adicione isto logo após as importações para desabilitar o menu padrão
    hide_streamlit_style = """
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            button[title="View fullscreen"] {visibility: hidden;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Título
    st.header("Gerador Inteligente de Planilhas 📊")

    # Entrada do usuário
    st.write("Descreva a estrutura da planilha que você deseja criar:")
    user_input = st.text_area("Exemplo: 'Uma planilha com colunas Nome, Nota1, Nota2 e Média (com fórmula) contendo 10 registros. Adicione filtros.'")

    # Sidebar com configurações
    st.sidebar.header("Configurações da Planilha")
    model_options = ['gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo', 'gpt-4o-mini', 'gpt-4o']
    selected_model = 'gpt-4'
    file_format = "Excel"
    file_name = st.sidebar.text_input("Nome do Arquivo", "nome_da_planilha")
    excel_language = st.sidebar.radio("Idioma do Excel", ["Inglês", "Português"], index=0)
    # include_graph = st.sidebar.checkbox("Gerar gráficos automaticamente")

    # Modelo de IA
    model = ChatOpenAI(model=selected_model)

    # Prompt da IA
    prompt_template = PromptTemplate.from_template(
        """
        Você é uma IA especializada em gerar planilhas baseadas em descrições. Com base no pedido abaixo, crie uma tabela fictícia coerente:
        
        Descrição: "{user_input}"
        
        **Regras:**     

         1. Retorne os dados em formato CSV válido com cabeçalho.
         2. As colunas devem refletir exatamente a descrição fornecida.
         3. Gere exatamente 5 registros fictícios realistas.
         4. Para cálculos (média, soma, etc):
          - Use fórmulas do Excel em português se o idioma for português (ex: =MÉDIA(B2:C2)).
          - Use fórmulas do Excel em inglês se o idioma for inglês (ex: =AVERAGE(B2:C2)).
          - Mantenha referências relativas para permitir arrastar a fórmula.
          - Não calcule os valores, deixe as fórmulas visíveis.
        5. Se houver menção a gráficos na descrição:
          - Adicione colunas extras com valores calculados (sufixo '_Valor') para uso em gráficos
          - Inclua pelo menos uma coluna categórica e uma numérica
        6. Formate números decimais com ponto (ex: 7.5).
        7. Não inclua explicações, apenas o CSV gerado.
        
        Resposta:
        """
    )
def translate_formulas(formula, language):
    """Traduz as fórmulas para o idioma do Excel selecionado."""
    excel_functions = {
        "Inglês": {"MÉDIA": "AVERAGE", "SOMA": "SUM", "SE": "IF", "CONTAR": "COUNT"},
        "Português": {"MÉDIA": "MÉDIA", "SOMA": "SOMA", "SE": "SE", "CONTAR": "CONTAR"}
    }
    for pt_func, en_func in excel_functions["Inglês"].items():
        if language == "Inglês":
            formula = formula.replace(pt_func, en_func)
    return formula

# Geração da planilha ao clicar no botão
if st.button("\u21bb Gerar Planilha"):
    if user_input.strip():
        with st.spinner("Gerando a planilha..."):
            try:
                prompt = prompt_template.format(user_input=user_input)
                response = model.predict(prompt)
                
                csv_data = StringIO(response.strip())
                csv_reader = reader(csv_data)
                lines = list(csv_reader)
                header = lines[0]
                data = lines[1:]
                
                df = pd.DataFrame(data, columns=header)
                # Traduzir fórmulas
                if excel_language == "Inglês":
                    for col in df.columns:
                        if df[col].astype(str).str.startswith("=").any():
                            df[col] = df[col].apply(lambda x: translate_formulas(x, "Inglês")) 
                
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='Planilha Gerada')
                    workbook = writer.book
                    worksheet = writer.sheets['Planilha Gerada']
                    worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)
                    
                    # Verificar se há menção a gráficos
                    if any(word in user_input.lower() for word in ['gráfico', 'grafico', 'chart', 'plot', 'gráficos']):
                        chart_sheet = workbook.add_worksheet("Gráficos")
                        value_cols = [col for col in df.columns if '_Valor' in col or df[col].str.replace('.', '', 1).str.isnumeric().all()]
                        cat_cols = [col for col in df.columns if col not in value_cols]
                        
                        if value_cols and cat_cols:
                            chart = workbook.add_chart({'type': 'column'})
                            for i, val_col in enumerate(value_cols):
                                col_letter = xl_col_to_name(df.columns.get_loc(val_col))
                                chart.add_series({
                                    'name': val_col,
                                    'categories': f"='Planilha Gerada'!$A$2:$A${len(df) + 1}",
                                    'values': f"='Planilha Gerada'!${col_letter}$2:${col_letter}${len(df) + 1}",
                                })
                            chart.set_title({'name': 'Gráficos de Dados'})
                            chart_sheet.insert_chart('B2', chart)
                
                file_name += ".xlsx"
                st.success("✅ Planilha gerada com sucesso!")
                st.download_button("⬇️ Baixar Planilha", data=buffer.getvalue(), file_name=file_name, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                
                st.subheader("Pré-visualização")
                st.dataframe(df.head(5))
                
                if any(word in user_input.lower() for word in ['gráfico', 'grafico', 'chart', 'plot', 'gráficos']):
                    st.subheader("📈 Gráficos Gerados")
                    for val_col in value_cols:
                        fig = px.bar(df, x=cat_cols[0], y=val_col, title=f"{val_col} por {cat_cols[0]}", color=cat_cols[0])
                        st.plotly_chart(fig)
            except Exception as e:
                st.error(f"Erro ao gerar a planilha: {e}")

   
