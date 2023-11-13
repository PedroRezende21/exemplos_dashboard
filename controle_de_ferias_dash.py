from dash import Dash, html, dcc, Input, Output, State, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
import os
import locale
from datetime import datetime

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

app = Dash(__name__)
app.scripts.config.serve_locally = True
server = app.server

current_dir = os.path.abspath(os.path.dirname(__file__))

# ===== style ======= #

tab_card = {'height': '100%'}

# MAIN CONFIG serve para configurar de maneira geral todos os graficos de uma só vez!

main_config = {
    "hovermode": "x unified",
    "legend": {"yanchor": "top",
                "y": 0.9,
                "xanchor": "left",
                "x": 0.1,
                "title": {"text": None},
                "font": {"color": "white"},
                "bgcolor": "rgba(0,0,0,0.5)"},
    "margin": {"l": 10, "r": 10, "t": 10, "b": 10}
}

config_graph = {"displayModeBar": False, "showTips": False}

template_theme1 = "flatly"
template_theme2 = "darkly"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY

base_de_dados = pd.read_excel(f'{current_dir}\\1 - Controle de Férias-2023 - 10OUT2023.ods', sheet_name='Cad')
lancamentos = pd.read_excel(f'{current_dir}\\1 - Controle de Férias-2023 - 10OUT2023.ods', sheet_name='Lan')

# ===== TRATAMENTO DOS DADOS =====

base_de_dados = base_de_dados[3:]
base_de_dados = base_de_dados.iloc[:, 1:]
base_de_dados.loc[3, 'Unnamed: 10'] = 'Tempo De Empresa'
base_de_dados.loc[3, 'Unnamed: 11'] = 'Data do direito Próxima Férias'
base_de_dados.loc[3, 'Unnamed: 14'] = 'Férias Totalmente Gozadas'
base_de_dados.loc[3, 'Unnamed: 15'] = 'Férias GozadasNº'
base_de_dados.loc[3, 'Unnamed: 16'] = 'Férias Geradas'
base_de_dados.loc[3, 'Unnamed: 17'] = 'Férias Devidas'
base_de_dados.loc[3, 'Unnamed: 18'] = 'Alerta De Vencimento Das Próximas Férias'
base_de_dados.columns = base_de_dados.iloc[0].values
base_de_dados = base_de_dados[1:].reset_index(drop= True)
base_de_dados['Posto/Grad'] = base_de_dados['Posto/Grad'].str.split('-').str[0]
base_de_dados.rename(columns={'NIP': 'Matrícula'}, inplace=True)
base_de_dados['Matrícula'] = base_de_dados['Matrícula'].astype(str)
base_de_dados['Data base para direito das férias'] = base_de_dados['Data base para direito das férias'].astype('datetime64[D]')
#base_de_dados['Admissão'] = base_de_dados['Admissão'].dt.strftime(r'%d/%m/%Y')
#base_de_dados['Data do direito Próxima Férias'] = base_de_dados['Data do direito Próxima Férias'].astype('datetime64[D]')
#base_de_dados['Próxima Férias'] = base_de_dados['Próxima Férias'].dt.strftime(r'%d/%m/%Y')
base_de_dados['Limite Gozo'] = base_de_dados['Limite Gozo'].astype('datetime64[D]')
#Convertendo os tipos de dados de cada coluna:
base_de_dados['Tempo De Empresa'] = base_de_dados['Tempo De Empresa'].astype(float)
base_de_dados['Dias de Férias'] = base_de_dados['Dias de Férias'].astype(int)
base_de_dados['Dias restantes'] = base_de_dados['Dias restantes'].astype(int)
base_de_dados['Férias GozadasNº'] = base_de_dados['Férias GozadasNº'].astype(int)
base_de_dados['Férias Geradas'].fillna(0, inplace=True)
base_de_dados['Férias Geradas'] = base_de_dados['Férias Geradas'].astype(int)
base_de_dados['Férias Devidas'].fillna(0, inplace=True)
base_de_dados['Férias Devidas'] = base_de_dados['Férias Devidas'].astype(int)
# Calcular o número de dígitos de cada número
base_de_dados["n_digits"] = base_de_dados["Matrícula"].str.len()
for linha in range(len(base_de_dados)):
    numerodezeros = 8 - int(base_de_dados.loc[linha, 'n_digits'])
    numerodealgarismo = int(base_de_dados.loc[linha, 'n_digits'])
    # Inserir zeros à esquerda
    base_de_dados.loc[linha, "Matrícula"] = "0" * numerodezeros + base_de_dados.loc[linha, "Matrícula"]

lancamentos = lancamentos[3:]
lancamentos = lancamentos.iloc[:, 1:]
lancamentos.loc[3, 'Unnamed: 1'] = 'Matrícula'
lancamentos.loc[3, 'Unnamed: 9'] = 'Papeleta de Afastamento'
lancamentos.loc[3, 'Unnamed: 10'] = 'Período De Gozo Início'
lancamentos.loc[3, 'Unnamed: 11'] = 'Período de Gozo Fim'
lancamentos.loc[3, 'Unnamed: 13'] = 'Data Pagamento'
lancamentos.loc[3, 'Unnamed: 14'] = 'Dias'
lancamentos.loc[3, 'Unnamed: 17'] = 'Situação Ref. Pagt.'
lancamentos.columns = lancamentos.iloc[0].values
lancamentos = lancamentos[1:].reset_index(drop= True)
lancamentos['quantidade'] = 1
lancamentos['Posto/Grad'] = lancamentos['Posto/Grad'].str.split('-').str[0]
lancamentos['Período De Gozo Início'] = lancamentos['Período De Gozo Início'].astype('datetime64[D]')
lancamentos['Período de Gozo Fim'] = lancamentos['Período de Gozo Fim'].astype('datetime64[D]')
lancamentos['Retorno'] = lancamentos['Retorno'].astype('datetime64[D]')
lancamentos['Data Pagamento'] = lancamentos['Data Pagamento'].astype('datetime64[D]')
# Calcular o número de dígitos de cada número
lancamentos['Matrícula'] = lancamentos['Matrícula'].astype(str)
lancamentos["n_digits"] = lancamentos["Matrícula"].str.len()
for linha in range(len(lancamentos)):
    numerodezeros = 8 - int(lancamentos.loc[linha, 'n_digits'])
    numerodealgarismo = int(lancamentos.loc[linha, 'n_digits'])
    # Inserir zeros à esquerda
    lancamentos.loc[linha, "Matrícula"] = "0" * numerodezeros + lancamentos.loc[linha, "Matrícula"]
hoje = pd.to_datetime(datetime.date(datetime.today()))
lancamentos['Dias de férias totais gozadas'] = None
for nome in lancamentos['Nome'].unique():
    df_nome = lancamentos.loc[lancamentos['Nome'] == nome]
    df_nome = df_nome.loc[df_nome['Período de Gozo Fim'] <= hoje]
    dias_totais = df_nome['Dias'].sum()
    lancamentos.loc[lancamentos['Nome'] == nome,'Dias de férias totais gozadas'] = dias_totais
base_de_dados = base_de_dados.drop('n_digits', axis= 1)
lancamentos = lancamentos.drop(['n_digits', 'Situação Ref. Pagt.', 'Observações'], axis= 1)
lancamentos_original = lancamentos
lancamentos = lancamentos.dropna(how= 'any')

# ============================================== GRÁFICO 1 ===============================================
quant_por_cia3 = lancamentos.groupby(['Mês','Ano', 'Companhia']).sum().reset_index(inplace=False)
quant_por_cia3['Mês/Ano'] = quant_por_cia3['Mês'].astype(str) + '/' + quant_por_cia3['Ano'].astype(str)
quant_por_cia3 = quant_por_cia3.drop(['Mês', 'Ano'], axis=1)
# Reorganize as colunas para que "Mês/Ano" fique à esquerda
quant_por_cia3 = quant_por_cia3[['Mês/Ano'] + [col for col in quant_por_cia3.columns if col != 'Mês/Ano']]
quant_por_cia3 = quant_por_cia3.groupby(['Mês/Ano', 'Companhia']).sum()
quant_por_cia3 = quant_por_cia3.unstack()['quantidade']
quant_por_cia3 = quant_por_cia3.fillna(value=0)
grafico1 = px.bar(quant_por_cia3, x = quant_por_cia3.index,
                y = quant_por_cia3.columns,
                barmode = 'group')
grafico1.update_traces(marker_line_width=1, textposition="auto")
grafico1.update_layout(title_font_family='Times',
                        title_font_color='black',
                        xaxis_title='Mês',
                        xaxis_title_font_size=16,
                        yaxis_title='Quantidade de Militares',
                        yaxis_title_font_size=16,
                        font_family='Times',
                        font_color='black',
                        legend_title_font_family='Times',
                        legend_title_font_color='black',
                        legend_font_size=12,
                        legend_font_family='Times',
                        legend_font_color= 'black',
                        plot_bgcolor='white',
                        paper_bgcolor='white')


# ============================================== GRÁFICO 2 ===============================================
lancamentos['quantidade'] = 1
quant_por_cia = lancamentos.loc[lancamentos['Dias de férias totais gozadas'] == 30]
quant_por_cia = quant_por_cia.groupby(['Companhia']).sum()
if quant_por_cia.shape[0] != 0:
    grafico2 = px.pie(quant_por_cia, values='quantidade', names = quant_por_cia.index, color = quant_por_cia.index,
                hole=0.5)
    grafico2.update_traces(textposition='inside', textinfo='percent+label', hoverinfo='percent+value+name',
                    marker=dict(line=dict(color='#FFFFFF', width=2)))
    grafico2.update_layout(
        font_family='Times',
        title_font_size=24,
        font_color='#555555',
        title_font_family='Times',
        title_font_color='#333333',
        legend_title_font_color='#333333',
        legend=dict(title='Cidades', font=dict(size=12)),
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor='white',
        plot_bgcolor='white',
    )
    
# ============================================== GRÁFICO 3 ===============================================
posto_grad = lancamentos.loc[lancamentos['Período De Gozo Início'] <= hoje]
posto_grad = lancamentos.loc[lancamentos['Dias de férias totais gozadas'] == 30]
posto_grad = posto_grad.groupby(['Posto/Grad']).sum()
if posto_grad.shape[0] != 0:
    grafico3 = px.bar(posto_grad, x = posto_grad.index, y = posto_grad['quantidade'], color = posto_grad.index)
    grafico3.update_traces(marker_line_width=1, text=posto_grad['quantidade'], textposition="auto")
    grafico3.update_layout(title_font_family='Times',
                            title_font_color='black',
                            xaxis_title='Mês',
                            xaxis_title_font_size=16,
                            yaxis_title='Quantidade de Militares',
                            yaxis_title_font_size=16,
                            font_family='Times',
                            font_color='black',
                            title_font_size=24,
                            legend_title_font_family='Times',
                            legend_title_font_color='black',
                            legend_font_size=12,
                            legend_font_family='Times',
                            legend_font_color= 'black',
                            plot_bgcolor='white',
                            paper_bgcolor='white')

# ============================================== GRÁFICO 4 ===============================================
militaresferias = lancamentos.loc[(lancamentos['Retorno'] > hoje) & (lancamentos['Período De Gozo Início'] < hoje), :]
militaresferias = militaresferias.groupby(['Posto/Grad']).sum()
if militaresferias.shape[0] != 0:
    grafico4 = px.bar(militaresferias, x = militaresferias.index, y = militaresferias['quantidade'], color = militaresferias.index)
    grafico4.update_traces(marker_line_width=1, text=militaresferias['quantidade'], textposition="auto")
    grafico4.update_layout(title_font_family='Times',
                            title_font_size=24,
                                title_font_color='black',
                                xaxis_title='Posto/Graduação',
                                xaxis_title_font_size=16,
                                yaxis_title='Quantidade de Militares',
                                yaxis_title_font_size=16,
                                font_family='Times',
                                font_color='black',
                                legend_title_font_family='Times',
                                legend_title_font_color='black',
                                legend_font_size=12,
                                legend_font_family='Times',
                                legend_font_color= 'black',
                                plot_bgcolor='white',
                                paper_bgcolor='white')
    
# ============================================== GRÁFICO 5 ===============================================

efetivo = len(base_de_dados['Matrícula'])
gozaram_30 = lancamentos.loc[lancamentos['Dias de férias totais gozadas'] == 30]
efetivo30 = len(gozaram_30['Matrícula'])
df_efetivo = pd.DataFrame(columns= ['Quantidade'], data = [efetivo, efetivo30])
df_efetivo['Tipo'] = ['Efetivo GPTFNRG', 'Militares que gozaram 30 dias']
if df_efetivo.shape[0] != 0:
    grafico5 = px.pie(df_efetivo, values= 'Quantidade', names= 'Tipo', color= 'Tipo', hole= 0.5)
    grafico5.update_traces(marker_line_width=1, text = df_efetivo['Quantidade'], textposition="auto")
    grafico5.update_layout(title_font_family='Times',
                            title_font_color='black',
                            xaxis_title='Mês',
                            xaxis_title_font_size=16,
                            yaxis_title='Quantidade de Militares',
                            yaxis_title_font_size=16,
                            font_family='Times',
                            font_color='black',
                            legend_title_font_family='Times',
                            legend_title_font_color='black',
                            legend_font_size=16,
                            legend_font_family='Times',
                            legend_font_color= 'black',
                            plot_bgcolor='white',
                            paper_bgcolor='white')
    
# ============================================== GRÁFICO 6 ===============================================

df_turma = lancamentos.loc[lancamentos['Dias de férias totais gozadas'] == 30]
df_turma = df_turma.groupby(['Turma de Férias']).sum()
if df_turma.shape[0]:
    grafico6 = px.pie(df_turma, values='quantidade', names = df_turma.index, color = df_turma.index,
                hole=0.5 )
    grafico6.update_traces(textposition='inside', textinfo='percent+label', hoverinfo='percent+value+name',
                    marker=dict(line=dict(color='#FFFFFF', width=2)))
    grafico6.update_layout(
        font_family='Times',
        title_font_size=24,
        font_color='#555555',
        title_font_family='Times',
        title_font_color='#333333',
        legend_title_font_color='#333333',
        legend=dict(title='Cidades', font=dict(size=12)),
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor='white',
        plot_bgcolor='white',
    )

# ============================================== INDICADOR 1 ===============================================

efetivo_especial = lancamentos_original.loc[lancamentos_original['Turma de Férias'] == 'Turma Especial']
efetivo_fora = lancamentos_original.loc[lancamentos_original['Turma de Férias'] == 'Fora de Turma']
efetivo_turma1 = lancamentos_original.loc[lancamentos_original['Turma de Férias'] == '1ª Turma']
efetivo_turma2 = lancamentos_original.loc[lancamentos_original['Turma de Férias'] == '2ª Turma']
efetivo_especial = len(efetivo_especial['Nome'].unique())
efetivo_fora = len(efetivo_fora['Nome'].unique())
efetivo_turma1 = len(efetivo_turma1['Nome'].unique())
efetivo_turma2 = len(efetivo_turma2['Nome'].unique())
especial_30 = gozaram_30.loc[gozaram_30['Turma de Férias'] == 'Turma Especial']
fora_30 = gozaram_30.loc[gozaram_30['Turma de Férias'] == 'Fora de Turma']
turma1_30 = gozaram_30.loc[gozaram_30['Turma de Férias'] == '1ª Turma']
turma2_30 = gozaram_30.loc[gozaram_30['Turma de Férias'] == '2ª Turma']
especial_30 = len(especial_30['Nome'].unique())
fora_30 = len(fora_30['Nome'].unique())
turma1_30 = len(turma1_30['Nome'].unique())
turma2_30 = len(turma2_30['Nome'].unique())

# Dados das turmas
turmas = ["Fora de Turma", "Turma Especial", "1ª Turma", '2ª Turma']
pessoas_total = [efetivo_fora, efetivo_especial, efetivo_turma1, efetivo_turma2]
pessoas_gozaram = [fora_30, especial_30, turma1_30, turma2_30]

# Calcula o percentual de férias gozadas para cada turma
percentuais = [(g / t) * 100 for g, t in zip(pessoas_gozaram, pessoas_total)]

# Cria o gráfico de indicadores
indicador_turmas = go.Figure()

for turma, percentual in zip(turmas, percentuais):
    indicador_turmas.add_trace(
        go.Indicator(
            mode="number+delta",
            value=percentual,
            title={"text": f"{percentual:.2f}%<br><span style='font-size:0.8em;color:gray'>{turma}</span>"},
            delta={"relative": True},
            domain={"row": 0, "column": turmas.index(turma)}
        )
    )

# Atualiza o layout do gráfico
indicador_turmas.update_layout(
    grid={"rows": 1, "columns": len(turmas), "pattern": "independent"},
    template="plotly_white"
)

# ============================================== TABELA 1 ===============================================

ainda_falta = lancamentos.loc[lancamentos['Dias de férias totais gozadas'] != 30].reset_index(drop= True)
ainda_falta = ainda_falta[['Matrícula', 'Posto/Grad', 'Nome', 'Dias de férias totais gozadas']]
ainda_falta = ainda_falta.dropna()
ainda_falta['Dias de férias totais gozadas'] = ainda_falta['Dias de férias totais gozadas'].astype(int)
nomes = ainda_falta['Nome'].unique()

def selecionar_menor_dia(df, lista_de_nomes):
    novo_ainda_falta = pd.DataFrame(columns= df.columns, data= {'Matrícula': df['Matrícula'], 'Posto/Grad': df['Posto/Grad'], 'Nome': df['Nome'], 'Dias restantes': None})
    for nome in lista_de_nomes:
        df_min = df.loc[df['Nome'] == nome]
        dias_restantes = df_min['Dias de férias totais gozadas'].min()    
        novo_ainda_falta['Dias de férias totais gozadas'].loc[novo_ainda_falta['Nome'] == nome] = dias_restantes
        novo_ainda_falta = novo_ainda_falta.drop_duplicates()
    return novo_ainda_falta

selecionar_menor_dia(ainda_falta, nomes)

# ============================================== TABELA 2 ===============================================

ainda_falta_geral = lancamentos_original.loc[lancamentos_original['Matrícula'] != '00000nan']
ainda_falta_geral =  ainda_falta_geral[['Matrícula', 'Posto/Grad', 'Nome', 'Dias de férias totais gozadas']]
ainda_falta_geral['Dias de férias totais gozadas'] = ainda_falta_geral['Dias de férias totais gozadas'].astype(int)
nomes_geral = ainda_falta_geral['Nome'].unique()
relageral = selecionar_menor_dia(ainda_falta_geral, nomes_geral)
relageral['Dias restantes'] = 30 - relageral['Dias de férias totais gozadas']
relageral = relageral[['Matrícula', 'Posto/Grad', 'Nome', 'Dias restantes']]
relageral = relageral.sort_values(by= 'Dias restantes', ascending= False).reset_index(drop= True)

# =========  Layout  =========== #
if quant_por_cia3.shape[0] == 0:
    grafico1 = None
if quant_por_cia.shape[0] == 0:
    grafico2 = None
if quant_por_cia.shape[0] == 0:
    grafico3 = None
if militaresferias.shape[0] == 0:
    grafico4 = None
if df_efetivo.shape[0] == 0:
    grafico5 = None
if df_turma.shape[0] == 0:
    grafico6 = None

app.layout = dbc.Container(children=[

    # ========== Row 1 ============

    dbc.Row([
        # Titulo
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend("Sessão de Pessoal - GPTFNRG")
                        ], sm=10),
                        dbc.Col([
                            html.I(className='fas fa-chart-bar',
                                   style={'font-size': '300%'})
                        ], sm=4, align='center')
                    ]),
                    dbc.Row([
                        dbc.Col([
                            ThemeSwitchAIO(aio_id="theme", themes=[
                                           url_theme1, url_theme2]),
                            html.Legend("Controle de férias")
                        ])
                    ], style={'margin-top': '10px'}),
                ])
            ], style=tab_card),
        ], sm=4, lg=2),

        # Gráfico 1
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                        dbc.Col(
                            html.Legend('Quantidade de militares de férias em cada mês')
                        )
                    ),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='grafico1', className='dbc', config=config_graph, figure=grafico1)
                        ], sm=12, md=12)
                    ])
                ])
            ], style=tab_card)
        ], sm=12, lg=10),
    ], className='g-2 my-auto', style={'margin-top': '7px'}),

# ============ Row 2 ===========
    dbc.Row([

        # Gráfico 2
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend('Distribuição entre as companhias que já gozaram 30 dias de férias ')
                        ]),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='grafico2',figure=grafico2, className='dbc', config=config_graph)
                        ], sm=12, md=12)
                    ])
                ])
            ], style=tab_card)
        ], sm=12, lg=4),

           
# Gráfico 3
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend('Quantidade de militares que já gozaram 30 dias de férias por Posto/Grad')
                            ]),
                        ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='grafico3', className='dbc', config=config_graph, figure = grafico3)
                            ], sm= 12, md= 12)
                        ])
                    ])
                ], style=tab_card)
            ], sm=12, lg=8),
    ], className='g-2 my-auto', style={'margin-top': '7px'}),

# ============ Row 3 ===========

# Gráfico 4
dbc.Row([

    # Coluna 1
    dbc.Col([
        dbc.Card(
            # Corpo do cartão
            [
                dbc.CardBody([
                    # Linha 1
                    dbc.Row([
                        # Coluna 1
                        dbc.Col([
                            # Legenda
                            html.Legend('Militares que estão de férias hoje')
                        ]),
                    ]),
                    # Linha 2
                    dbc.Row([
                        # Coluna 1
                        dbc.Col([
                            # Gráfico
                            dcc.Graph(id='grafico4',figure= grafico4, className='dbc', config=config_graph)
                        ], sm= 12, md= 12)
                    ])
                ])
            ], style=tab_card),
    ], sm=12, lg=4),

    # Coluna 2
    dbc.Col([
        dbc.Card(
            # Corpo do cartão
            [
                dbc.CardBody([
                    # Linha 1
                    dbc.Row([
                        # Coluna 1
                        dbc.Col([
                            # Legenda
                            html.Legend('Relação do pessoal que já gozou algum período de férias, e seus respectivos dias restantes.')
                        ]),
                    ]),
                    # Linha 2
                    dbc.Row([
                        # Coluna 1
                        dbc.Col([
                            # Tabela
                            dash_table.DataTable(page_size=12,
                                style_data={
                                    'whiteSpace': 'normal',
                                    'height': 'auto',
                                },
                                data=selecionar_menor_dia(ainda_falta, nomes).to_dict('records'),
                                columns=[{'id': c, 'name': c} for c in selecionar_menor_dia(ainda_falta, nomes).columns]),
                        ])
                    ])
                ])
            ], style=tab_card, className='w-100'),
    ], sm=12, lg=8)

], className='g-2 my-auto', style={'margin-top': '7px'}),

# ============ Row 4 ===========

# Gráfico 5
dbc.Row([

    # Coluna 1
    dbc.Col([
        dbc.Card(
            # Corpo do cartão
            [
                dbc.CardBody([
                    # Linha 1
                    dbc.Row([
                        # Coluna 1
                        dbc.Col([
                            # Legenda
                            html.Legend('Distribuição percentual de quem já gozou os 30 dias de férias')
                        ]),
                    ]),
                    # Linha 2
                    dbc.Row([
                        # Coluna 1
                        dbc.Col([
                            # Gráfico
                            dcc.Graph(id='grafico5',figure= grafico5, className='dbc', config=config_graph)
                        ], sm= 12, md= 12)
                    ])
                ])
            ], style=tab_card, className='w-100'),
    ], sm=12, lg=7),

    # Coluna 2
    dbc.Col([
        dbc.Card(
            # Corpo do cartão
            [
                dbc.CardBody([
                    # Linha 1
                    dbc.Row([
                        # Coluna 1
                        dbc.Col([
                            # Legenda
                            html.Legend('Relação do pessoal geral dos dias restantes.')
                        ]),
                    ]),
                    # Linha 2
                    dbc.Row([
                        # Coluna 1
                        dbc.Col([
                            # Tabela
                            dash_table.DataTable(page_size=12,
                                style_data={
                                    'whiteSpace': 'normal',
                                    'Width': 'auto',
                                    'columnDefs': [{'targets': [-1],
                                                    'align': 'right',}]
                                },
                                style_cell={
                                'minWidth': '0px',
                                'maxWidth': '100%',
    },
                                data = relageral.to_dict('records'),
                                columns=[{'id': c, 'name': c} for c in relageral.columns]),
                        ])
                    ])
                ])
            ], style=tab_card, className='w-100'),
    ], sm=12, lg=5)
], className='g-2 my-auto', style={'margin-top': '7px'}),

# ============ Row 5 ===========

# Gráfico 6
dbc.Row([

    # Coluna 1
    dbc.Col([
        dbc.Card(
            # Corpo do cartão
            [
                dbc.CardBody([
                    # Linha 1
                    dbc.Row([
                        # Coluna 1
                        dbc.Col([
                            # Legenda
                            html.Legend('Distribuição percentual entre as turmas de férias, quem já gozou os 30 dias.')
                        ]),
                    ]),
                    # Linha 2
                    dbc.Row([
                        # Coluna 1
                        dbc.Col([
                            # Gráfico
                            dcc.Graph(id='indicador_turmas',figure = indicador_turmas, className='dbc', config=config_graph)
                        ], sm= 12, md= 12)
                    ])
                ])
            ], style=tab_card, className='w-100'),
    ], sm=12, lg=12),
], className='g-2 my-auto', style={'margin-top': '7px'})

], fluid=True, style={'height': '100vh'})

# =========== callbacks ===========

if __name__ == '__main__':
    app.run_server(host='192.168.2.103', port=8050, debug=True)
