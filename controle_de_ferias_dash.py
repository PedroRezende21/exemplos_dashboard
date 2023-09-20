from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
import os
import locale

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

base_de_dados = pd.read_excel(f'{current_dir}\\Controle de Férias-S1.xlsx', sheet_name='Cad')
lancamentos = pd.read_excel(f'{current_dir}\\controle de Férias-S1.xlsx', sheet_name='Lan')
dados_pessoal = pd.read_excel(f'{current_dir}\\Controle de Férias GptFNRG 2023 - 05SET2023.ods', sheet_name= 'FERIAS 2023')

#tratando:
dados_pessoal = dados_pessoal[['POSTO/GRAD.','CORPO','NIP','NOME GUERRA','CIA']]
dados_pessoal = dados_pessoal[:388]
dados_pessoal['NIP'] = dados_pessoal['NIP'].astype(int)
dados_pessoal['NIP'] = dados_pessoal['NIP'].astype(str)
dados_pessoal["n_digits"] = dados_pessoal["NIP"].str.len()
for linha in range(len(dados_pessoal)):
    numerodezeros = 8 - int(dados_pessoal.loc[linha, 'n_digits'])
    numerodealgarismo = int(dados_pessoal.loc[linha, 'n_digits'])
    # Inserir zeros à esquerda
    dados_pessoal.loc[linha, "NIP"] = "0" * numerodezeros + dados_pessoal.loc[linha, "NIP"]

#tratando:
base_de_dados = base_de_dados[3:]
base_de_dados = base_de_dados.iloc[:, 1:]
base_de_dados.columns = base_de_dados.iloc[0].values
base_de_dados = base_de_dados[1:].reset_index(drop= True)
base_de_dados['Posto/Grad'] = base_de_dados['Posto/Grad'].str.split('-').str[0]
base_de_dados['Matrícula'] = base_de_dados['Matrícula'].astype(str)
base_de_dados['Data base para direito das férias'] = base_de_dados['Data base para direito das férias'].astype('datetime64[D]')
#base_de_dados['Admissão'] = base_de_dados['Admissão'].dt.strftime(r'%d/%m/%Y')
base_de_dados['Data do direitoPróxima Férias'] = base_de_dados['Data do direitoPróxima Férias'].astype('datetime64[D]')
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

#tratando:
lancamentos = lancamentos[3:]
lancamentos = lancamentos.iloc[:, 1:]
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

base_de_dados = base_de_dados.drop('n_digits', axis= 1)
lancamentos = lancamentos.drop('n_digits', axis= 1)
dados_pessoal = dados_pessoal.drop('n_digits', axis= 1)

# ============================================== GRÁFICO 1 ===============================================
quant_por_mes = lancamentos.groupby(['Mês']).sum()
media_geral = quant_por_mes['quantidade'].mean()
grafico1 = px.bar(
    x=quant_por_mes.index,
    y=quant_por_mes['quantidade']
)
grafico1.update_traces(marker_line_width=1, text=quant_por_mes['quantidade'], textposition="auto")
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
quant_por_cia = lancamentos.groupby(['Companhia']).sum()
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
    plot_bgcolor='white')

# ============================================== GRÁFICO 3 ===============================================
quant_por_cia = lancamentos.groupby(['Mês', 'Companhia']).sum()
quant_por_cia = quant_por_cia.fillna(value= 0)
quant_por_cia = quant_por_cia.unstack()['quantidade']
grafico3 = px.bar(quant_por_cia, x = quant_por_cia.index,
                y = quant_por_cia.columns,
                barmode = 'group')
grafico3.update_traces(marker_line_width=1, text=quant_por_mes['quantidade'], textposition="auto")
grafico3.update_layout(title_font_family='Times',
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

# ============================================== GRÁFICO 4 ===============================================
posto_grad = lancamentos.groupby(['Posto/Grad']).sum()
grafico4 = px.bar(posto_grad, x = posto_grad.index, y = posto_grad['quantidade'], color = posto_grad.index)
grafico4.update_traces(marker_line_width=1, text=quant_por_mes['quantidade'], textposition="auto")
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

# =========  Layout  =========== #
app.layout = dbc.Container(children=[

    # ========== Row 1 ============

    dbc.Row([

        # Gráfico 1
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

        # Gráfico 2
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                        dbc.Col(
                            html.Legend('Quantidade de militares que gozaram férias por mês')
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

        # Gráfico 3
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend('Distribuição entre as companhias que já gozaram férias')
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

        # Gráfico 4
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend('Quantidade de férias por Posto/Grad')
                        ]),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='grafico4', className='dbc', config=config_graph, figure=grafico4)
                        ], sm= 12, md= 12)
                    ])
                ])
            ], style=tab_card)
        ], sm=12, lg=8),
    ], className='g-2 my-auto', style={'margin-top': '7px'}),

# ============ Row 3 ===========

        # Gráfico 5
        dbc.Row([

            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(id='grafico5',figure= None, className='dbc', config=config_graph)
                            ], sm= 12, md= 12)
                        ])
                    ])
                ], style=tab_card )  
            ], sm=12, lg=7)
        ], className='g-2 my-auto', style={'margin-top': '7px'})

    ], fluid=True, style={'height': '100vh'})

# =========== callbacks ===========

if __name__ == '__main__':
    app.run_server(debug=True)