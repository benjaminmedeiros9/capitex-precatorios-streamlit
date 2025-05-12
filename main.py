# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

# --- CONFIGURAÇÕES DA PÁGINA ---
st.set_page_config(page_title="CAPITEX - Calculadora de Rentabilidade", layout="wide")

# --- FUNÇÃO PARA FORMATAR NÚMEROS COMO MOEDA (PADRÃO BRASILEIRO MANUAL) ---
def formatar_moeda(valor):
    """Formata um valor numérico como moeda no padrão brasileiro (R$ 1.234.567,89) de forma manual."""
    try:
        # Garante que o valor é um float com duas casas decimais
        s = f"{float(valor):.2f}"
        inteiro, decimal = s.split(".")
        
        # Adiciona ponto como separador de milhar
        partes_inteiro = []
        while len(inteiro) > 3:
            partes_inteiro.insert(0, inteiro[-3:])
            inteiro = inteiro[:-3]
        partes_inteiro.insert(0, inteiro)
        inteiro_formatado = ".".join(partes_inteiro)
        
        return f"R$ {inteiro_formatado},{decimal}"
    except Exception: # Fallback para qualquer erro inesperado na formatação manual
        # Em caso de erro, retorna o valor com duas casas decimais, sem formatação de milhar complexa, mas com R$
        return f"R$ {valor:.2f}" 

# --- CSS CUSTOMIZADO PARA MELHORAR RESPONSIVIDADE ---
st.markdown("""
<style>
    /* Ajustes gerais para o container principal */
    .main .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        overflow-x: auto; /* Permitir rolagem horizontal se o conteúdo transbordar */
    }

    /* Ajustes para tabelas (DataFrames) */
    .stDataFrame div[data-testid="stDataFrameResizable"] { /* Container redimensionável do DataFrame */
        overflow-x: auto !important; /* Forçar rolagem horizontal para o container da tabela */
        width: 100%;
    }
    .stDataFrame table {
        width: 100% !important; /* Tabela ocupa a largura do seu container */
        display: table !important;
        table-layout: auto; /* Permitir que o navegador ajuste a largura das colunas */
    }

    /* Ajustes gerais para telas menores */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 0.5rem !important; /* Reduzir padding em telas muito pequenas */
            padding-right: 0.5rem !important;
        }
        body, .stApp { /* Aplicar ao corpo e ao container principal do app */
            font-size: 14px !important; /* Tamanho de fonte base para mobile */
        }
        h1 {
            font-size: 1.5em !important;
            line-height: 1.2;
        }
        h2 {
            font-size: 1.3em !important;
            line-height: 1.2;
        }
        h3 {
            font-size: 1.1em !important;
            line-height: 1.2;
        }
        .stMarkdown, .stDataFrame, .stText, .stAlert { /* Elementos de texto */
            word-wrap: break-word;
            overflow-wrap: break-word;
        }
        
        div[data-testid="stHorizontalBlock"] > div.st-emotion-cache-ocqkz7 { 
            flex-direction: column !important; 
            align-items: flex-start !important; 
        }

        .stImage img {
            max-width: 80px !important; 
            height: auto !important;
            margin-bottom: 0.5rem; 
        }

        .stButton > button, .stDownloadButton > button {
            padding: 0.6rem 1rem !important;
            font-size: 1em !important;
            width: 100%; 
        }
        .stTextInput input, .stNumberInput input {
            padding: 0.6rem !important;
            font-size: 1em !important;
        }
        .stSlider {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- FUNÇÃO DE CÁLCULO DE RENTABILIDADE DO PRECATÓRIO ---
def calcular_rentabilidade_precatorio(valor_precatorio, taxa_selic_anual, anos=5):
    custo_aquisicao_perc = 0.50
    custo_intermediacao_perc = 0.05
    custo_acompanhamento_perc = 0.03
    custo_escritura_perc = 0.01
    custo_habilitacao = 3500.00

    custo_aquisicao = valor_precatorio * custo_aquisicao_perc
    custo_intermediacao = valor_precatorio * custo_intermediacao_perc
    custo_acompanhamento = valor_precatorio * custo_acompanhamento_perc
    custo_escritura = max(valor_precatorio * custo_escritura_perc, 2500.00)

    custo_total_aquisicao = custo_aquisicao + custo_intermediacao + custo_habilitacao + custo_acompanhamento + custo_escritura
    valor_futuro_precatorio = valor_precatorio * ((1 + taxa_selic_anual) ** anos)
    lucro_bruto = valor_futuro_precatorio - custo_total_aquisicao
    rentabilidade_percentual_periodo = (lucro_bruto / custo_total_aquisicao) * 100 if custo_total_aquisicao > 0 else 0
    
    if custo_total_aquisicao > 0 and anos > 0:
        rentabilidade_anual_precatorio = ((valor_futuro_precatorio / custo_total_aquisicao)**(1/anos) - 1) * 100
    else:
        rentabilidade_anual_precatorio = 0

    return {
        'valor_precatorio_inicial': valor_precatorio,
        'taxa_selic_anual_informada': taxa_selic_anual * 100,
        'periodo_investimento_anos': anos,
        'custos_detalhados': {
            'Custo de Aquisição (50%)': custo_aquisicao,
            'Custo de Intermediação (5%)': custo_intermediacao,
            'Custo de Habilitação dos Compradores': custo_habilitacao,
            'Custo de Acompanhamento Processual (3%)': custo_acompanhamento,
            'Custo de Escritura de Cessão (1%, min. R$2.500)': custo_escritura,
        },
        'custo_total_aquisicao': custo_total_aquisicao,
        'valor_estimado_precatorio_atualizado_selic': valor_futuro_precatorio,
        'lucro_bruto_estimado': lucro_bruto,
        'rentabilidade_percentual_estimada_periodo': rentabilidade_percentual_periodo,
        'rentabilidade_anual_estimada_precatorio': rentabilidade_anual_precatorio
    }

# --- INTERFACE DO USUÁRIO ---

with st.container():
    col1, col2 = st.columns([0.2, 0.8])
    with col1:
        st.image("/home/ubuntu/workspace/precatorio_site/images/logo_capitex.png", width=100) 
    with col2:
        st.title("CAPITEX")
        st.subheader("Calculadora de Rentabilidade de Investimentos em Precatórios")

st.markdown("---_---")

st.sidebar.header("Parâmetros da Simulação")
valor_precatorio_input = st.sidebar.number_input(
    "Valor de Face do Precatório (R$):", 
    min_value=0.0, 
    value=100000.0, 
    step=1000.0, 
    format="%.2f"
)
taxa_selic_atual_exemplo = 14.75
taxa_selic_input_usuario = st.sidebar.number_input(
    f"Taxa SELIC Anual (%): (Padrão: {taxa_selic_atual_exemplo})", 
    min_value=0.0, 
    value=taxa_selic_atual_exemplo, 
    step=0.01, 
    format="%.2f"
)
anos_investimento = st.sidebar.slider("Período de Investimento (Anos):", min_value=1, max_value=10, value=5)

if st.sidebar.button("Calcular Rentabilidade"):
    if valor_precatorio_input > 0 and taxa_selic_input_usuario >= 0: # Permitir taxa SELIC 0%
        resultados_precatorio = calcular_rentabilidade_precatorio(valor_precatorio_input, taxa_selic_input_usuario / 100, anos_investimento)
        
        st.subheader("Resultados da Simulação do Precatório")          
        
        st.markdown(f"**Valor de Face do Precatório:** {formatar_moeda(resultados_precatorio['valor_precatorio_inicial'])}")
        st.markdown(f"**Taxa SELIC Anual Informada:** {resultados_precatorio['taxa_selic_anual_informada']:.2f}%")
        st.markdown(f"**Período de Investimento:** {resultados_precatorio['periodo_investimento_anos']} anos")
        
        st.markdown("#### Custos Detalhados da Aquisição")
        for custo, valor in resultados_precatorio['custos_detalhados'].items():
            st.markdown(f"- {custo}: {formatar_moeda(valor)}")
        st.markdown(f"**Custo Total de Aquisição:** {formatar_moeda(resultados_precatorio['custo_total_aquisicao'])}")
        
        st.markdown("#### Projeção de Rentabilidade")
        st.markdown(f"**Valor Estimado do Precatório Atualizado pela SELIC:** {formatar_moeda(resultados_precatorio['valor_estimado_precatorio_atualizado_selic'])}")
        st.markdown(f"**Lucro Bruto Estimado:** {formatar_moeda(resultados_precatorio['lucro_bruto_estimado'])}")
        st.markdown(f"**Rentabilidade Percentual Estimada no Período:** <span style='font-size:1.2em; color:green;'>{resultados_precatorio['rentabilidade_percentual_estimada_periodo']:.2f}%</span>", unsafe_allow_html=True)
        st.markdown(f"**Rentabilidade Anual Estimada do Precatório:** <span style='font-size:1.1em; font-weight: bold; color: yellow; background-color: #333; padding: 2px 5px; border-radius: 3px;'>{resultados_precatorio['rentabilidade_anual_estimada_precatorio']:.2f}% a.a.</span>", unsafe_allow_html=True)

        st.markdown("---_---")
        st.subheader("Comparativo com Outros Investimentos (Estimativa para o mesmo período)")
        
        taxa_poupanca_aa_perc = 6.17 
        taxa_cdb_cdi_aa_perc = (taxa_selic_input_usuario * 0.90) 
        taxa_tesouro_selic_aa_perc = taxa_selic_input_usuario 
        investimento_inicial_comparativo = resultados_precatorio['custo_total_aquisicao']

        valor_futuro_poupanca = investimento_inicial_comparativo * ((1 + taxa_poupanca_aa_perc/100) ** anos_investimento)
        lucro_poupanca = valor_futuro_poupanca - investimento_inicial_comparativo
        rentabilidade_poupanca_periodo = (lucro_poupanca / investimento_inicial_comparativo) * 100 if investimento_inicial_comparativo > 0 else 0
        rentabilidade_poupanca_anual = taxa_poupanca_aa_perc

        valor_futuro_cdb = investimento_inicial_comparativo * ((1 + taxa_cdb_cdi_aa_perc/100) ** anos_investimento)
        lucro_cdb = valor_futuro_cdb - investimento_inicial_comparativo
        rentabilidade_cdb_periodo = (lucro_cdb / investimento_inicial_comparativo) * 100 if investimento_inicial_comparativo > 0 else 0
        rentabilidade_cdb_anual = taxa_cdb_cdi_aa_perc
        
        valor_futuro_tesouro_selic = investimento_inicial_comparativo * ((1 + taxa_tesouro_selic_aa_perc/100) ** anos_investimento)
        lucro_tesouro_selic = valor_futuro_tesouro_selic - investimento_inicial_comparativo
        rentabilidade_tesouro_selic_periodo = (lucro_tesouro_selic / investimento_inicial_comparativo) * 100 if investimento_inicial_comparativo > 0 else 0
        rentabilidade_tesouro_selic_anual = taxa_tesouro_selic_aa_perc

        data_comparativo = {
            'Investimento': ['Precatório (CAPITEX)', 'Poupança', 'CDB (Ex: 90% CDI)', 'Tesouro Selic'],
            'Valor Investido (R$)': [formatar_moeda(resultados_precatorio['custo_total_aquisicao'])] * 4,
            f"Valor Final Estimado após {anos_investimento} anos (R$)": [
                formatar_moeda(resultados_precatorio['valor_estimado_precatorio_atualizado_selic']),
                formatar_moeda(valor_futuro_poupanca),
                formatar_moeda(valor_futuro_cdb),
                formatar_moeda(valor_futuro_tesouro_selic)
            ],
            f"Lucro Estimado no Período (R$)": [
                formatar_moeda(resultados_precatorio['lucro_bruto_estimado']),
                formatar_moeda(lucro_poupanca),
                formatar_moeda(lucro_cdb),
                formatar_moeda(lucro_tesouro_selic)
            ],
            'Rentabilidade Estimada no Período (%)': [
                f"{resultados_precatorio['rentabilidade_percentual_estimada_periodo']:.2f}%",
                f"{rentabilidade_poupanca_periodo:.2f}%",
                f"{rentabilidade_cdb_periodo:.2f}%",
                f"{rentabilidade_tesouro_selic_periodo:.2f}%"
            ],
            'Rentabilidade Anual Estimada (%)': [
                f"<span style='font-weight: bold; color: yellow; background-color: #333; padding: 2px 5px; border-radius: 3px;'>{resultados_precatorio['rentabilidade_anual_estimada_precatorio']:.2f}% a.a.</span>",
                f"{rentabilidade_poupanca_anual:.2f}% a.a.",
                f"{rentabilidade_cdb_anual:.2f}% a.a.",
                f"{rentabilidade_tesouro_selic_anual:.2f}% a.a."
            ]
        }
        df_comparativo = pd.DataFrame(data_comparativo)
        st.markdown(df_comparativo.set_index('Investimento').to_html(escape=False), unsafe_allow_html=True)
        
        st.caption("Nota: As rentabilidades de outros investimentos são estimativas e podem variar. A rentabilidade anual do precatório é uma média estimada para o período.")

    elif valor_precatorio_input <= 0:
        st.sidebar.error("Por favor, insira um valor de face do precatório maior que zero.")
    elif taxa_selic_input_usuario < 0:
        st.sidebar.error("Por favor, insira uma taxa SELIC válida (maior ou igual a zero).")

st.markdown("---_---")
st.caption("Este simulador é uma ferramenta para fins ilustrativos e educacionais. Os resultados são baseados nas informações fornecidas e em estimativas de mercado, não constituindo qualquer tipo de garantia ou recomendação de investimento. Consulte um profissional antes de tomar qualquer decisão financeira.")

