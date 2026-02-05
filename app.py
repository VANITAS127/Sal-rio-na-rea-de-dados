import streamlit as st
import pandas as pd
import plotly.express as px

#agr vem a criação da pagina,
# agr embaixo é aquele bagulho que mostra as janelas.
st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon='💵',
    layout='wide')

#agr vem os dados
df = pd.read_csv('https://raw.githubusercontent.com/VANITAS127/Sal-rio-na-rea-de-dados/refs/heads/main/Dados_finais')   

    #agr irei criar uma parte reservada para filtros
st.sidebar.header("Filtros")

#primeiramente o ano
anos_disponiveis = sorted(df['Ano'].unique())
#esse daqui é pra criar os bagulho visivel de seleção de ano
anos_selecionado = st.sidebar.multiselect('Ano', anos_disponiveis, default=anos_disponiveis)

#agr senioridade
senioridade_disponivel = sorted(df['Nível de experiência'].unique())
senioridade_selecionada = st.sidebar.multiselect('Nível de experiência', senioridade_disponivel, default=senioridade_disponivel)

 #agr o tipo de contrato
contrato_disponivel = sorted(df['Tipo de emprego'].unique())
contrato_selecionado = st.sidebar.multiselect('Tipo de emprego', contrato_disponivel, default=contrato_disponivel)

#agr tamanho da empresa
tamanho_disponivel = sorted(df['Tamanho'].unique())
tamanho_selecionado = st.sidebar.multiselect('Tamanho', tamanho_disponivel, default=tamanho_disponivel)

#acima tem o set page agr irei criar oq irá filtrar de fato os dados
df_filtrado = df[
    (df['Ano'].isin(anos_selecionado)) &
    (df['Nível de experiência'].isin(senioridade_selecionada)) &
    (df['Tipo de emprego'].isin(contrato_selecionado)) &   
    (df['Tamanho'].isin(tamanho_selecionado))
]

#titulos
st.title("📊Dashboard de Salários na Área de Dados📈")
st.markdown('Um dashboard simples e interativo para analisar os salários, use os filtros para uma busca mais precisa')

#agr as metricas papai
st.subheader("Métricas Gerais(Salário em usd)")
 
if not df_filtrado.empty:
    salário_medio = df_filtrado['Salário em dólares americanos'].mean()
    salário_maximo = df_filtrado['Salário em dólares americanos'].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado['Cargo'].mode()[0]

else:
    salário_medio = 0
    salário_maximo = 0
    total_registros = 0
    cargo_mais_frequente = 'N/A'

col1, col2, col3, col4 = st.columns(4)
col1.metric('Salário Médio', f'${salário_medio:,.2f}')
col2.metric('Salário Máximo', f'${salário_maximo:,.2f}')
col3.metric('Total de Registros', f'{total_registros:,}')
col4.metric('Cargo Mais Frequente', cargo_mais_frequente)

st.markdown("---")

#graficos baby
st.subheader("Gráficos")
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('Cargo')['Salário em dólares americanos'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        grafico_cargos = px.bar(
             top_cargos,
            x='Salário em dólares americanos',
            y='Cargo',
            orientation='h',
            title='Top 10 Cargos com Maior Salário Médio',
            labels={'Salário em dólares americanos': 'Salário Médio (USD)', 'Cargo': 'Cargo'}
        )
        grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para os filtros selecionados.")

with col_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado,
            x='Salário em dólares americanos',
            nbins=30,
            title='Distribuição dos Salários',
            labels={'Salário em dólares americanos': 'Salário (USD)', 'count': ''}
        )
        grafico_hist.update_layout(title_x=0.1)
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para os filtros selecionados.")

col_graf3, col_graf4 = st.columns(2)
with col_graf3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
        remoto_contagem.columns = ['tipo_de_trabalho', 'quantidade']
        grafico_remoto = px.pie(
            remoto_contagem,
            names='tipo_de_trabalho',
            values='quantidade',
            title='Distribuição de Trabalho Remoto vs Presencial',
            hole=0.5
        )    
        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para os filtros selecionados.")

with col_graf4:
    if not df_filtrado.empty:
        cargo_especifico = df_filtrado[df_filtrado['Cargo']== 'Data Scientist']
        Média_filtrada = cargo_especifico.groupby('pais_iso3')['Salário em dólares americanos'].mean().reset_index()

        grafico_cho = px.choropleth(Média_filtrada,
            locations='pais_iso3',
            color='Salário em dólares americanos',
            color_continuous_scale='Plasma',
            title='Média salarial por país',
            labels={'Salário em dólares americanos':'Salário', 'pais_iso3':'País'}
            )
        grafico_cho.update_layout(title_x=0.1)
        st.plotly_chart(grafico_cho, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para os filtros selecionados.")

#Dados adicionais
st.subheader("Dados Adicionais")
st.dataframe(df_filtrado)