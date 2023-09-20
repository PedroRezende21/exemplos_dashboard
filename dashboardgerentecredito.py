from dash import Dash, html, dcc, Input, Output, State, dash_table
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

# ============================ IMPORTANDO OS DADOS ============================ #
dados = pd.read_excel(f'{current_dir}\\empenhos em aberto.xlsx', sheet_name='SET2023, Saldo - R$ (Conta Con')
cred_disponivel = pd.read_excel(f'{current_dir}\\Crédito disponivel UGR.xlsx')

# ============================ TRATAMENTO DE DADOS ============================ #

dados = dados.drop(0, axis = 0).reset_index(drop = True)
dados.columns = dados.iloc[0, :]
dados = dados.drop(0, axis = 0).reset_index(drop = True)
dados = dados.rename(columns={'631510000' : '631510000 RPNP A LIQ BLOQUEADOS P/DECRETO_93872/86'})
dados = dados.rename(columns={'631100000' : '631100000 RP NAO PROCESSADOS A LIQUIDAR'})
dados = dados.rename(columns={'622920101' : '622920101 EMPENHOS A LIQUIDAR'})
dados = dados.drop(0, axis = 0)
empenhos = dados.loc[dados['UG Responsável'] == 'GRUPAMENTO DE FUZILEIROS NAVAIS DO RIO GRANDE', :]
empenhos = empenhos.loc[empenhos['PI'] != 'B44101002DD' ,:]
empenhos = empenhos.fillna(0)

index_comeco = cred_disponivel.loc[cred_disponivel['Crédito disponivel UGR'] == 'Mês Lançamento: SET/2023'].index
index_comeco = int(index_comeco.values[0])
cred_disponivel = cred_disponivel[index_comeco:]
cred_disponivel['Unnamed: 8'] = cred_disponivel['Unnamed: 8'].fillna(0)
cred_disponivel['Unnamed: 8'] = cred_disponivel['Unnamed: 8'].astype(int)
cred_disponivel['Unnamed: 8'] = cred_disponivel['Unnamed: 8'].astype(str)
cred_disponivel['Unnamed: 1'] = cred_disponivel['Unnamed: 1'] + ' - ' + cred_disponivel['Unnamed: 2']
cred_disponivel['Unnamed: 3'] = cred_disponivel['Unnamed: 3'] + ' - ' + cred_disponivel['Unnamed: 4']
cred_disponivel['Unnamed: 10'] = cred_disponivel['Unnamed: 10'] + ' - ' + cred_disponivel['Unnamed: 11']
cred_disponivel['Unnamed: 12'] = cred_disponivel['Unnamed: 12'] + ' - ' + cred_disponivel['Unnamed: 13']
cred_disponivel['Unnamed: 6'] = cred_disponivel['Unnamed: 6'] + cred_disponivel['Unnamed: 7'] + '000' + cred_disponivel['Unnamed: 8'] + ' - ' + cred_disponivel['Unnamed: 9']
cred_disponivel = cred_disponivel.drop(['Unnamed: 2', 'Unnamed: 4', 'Unnamed: 11', 'Unnamed: 13', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9'], axis = 1).reset_index(drop = True)
cred_disponivel = cred_disponivel.rename(columns={'Unnamed: 1' : 'Unidade Orçamentária'})
cred_disponivel = cred_disponivel.rename(columns={'Unnamed: 3' : 'UG Responsável'})
cred_disponivel = cred_disponivel.rename(columns={'Unnamed: 5' : 'PTRES'})
cred_disponivel = cred_disponivel.rename(columns={'Unnamed: 6' : 'Plano Orçamentário'})
cred_disponivel = cred_disponivel.rename(columns={'Unnamed: 10' : 'PI'})
cred_disponivel = cred_disponivel.rename(columns={'Unnamed: 12' : 'Natureza de Despesa'})
cred_disponivel = cred_disponivel.rename(columns={'Unnamed: 14' : 'Crédito Disponível'})
cred_disponivel = cred_disponivel.rename(columns={'Crédito disponivel UGR' : 'Conta Corrente'})
cred_disponivel = cred_disponivel.drop(0, axis=0).reset_index(drop= True)
cred_disponivel = cred_disponivel.loc[cred_disponivel['UG Responsável'] == '785200 - GRUPAMENTO DE FUZILEIROS NAVAIS DO RIO GRANDE'].reset_index(drop= True)
cred_disponivel = cred_disponivel.loc[cred_disponivel['UG Responsável'] == '785200 - GRUPAMENTO DE FUZILEIROS NAVAIS DO RIO GRANDE'].reset_index(drop= True)
cred_disponivel['Crédito Disponível'] = cred_disponivel['Crédito Disponível'].astype(float)
cred_por_natureza = cred_disponivel.groupby(['Conta Corrente', 'PI', 'Natureza de Despesa']).sum().reset_index()

# ============================ PLOTANDO OS GRÁFICOS ============================ #

df_grafico1 = cred_por_natureza
df_grafico1['PI'] = df_grafico1['PI'].str[:11]
df_grafico1['Natureza de Despesa'] = df_grafico1['Natureza de Despesa'].str[7 + 1:]
grafico1 = px.bar(x=df_grafico1['PI'] + ' ' + df_grafico1['Natureza de Despesa'],
    y=df_grafico1['Crédito Disponível'])
grafico1.update_layout(xaxis_title = 'Conta corrente',
    yaxis_title = 'Crédito Disponível',
    xaxis_ticktext=cred_por_natureza['PI'].str[:11]
    )


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
                            html.Legend("Gestão de crédito - GPTFNRG")
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
                            html.Legend("Controle das contas correntes")
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
                            html.Legend('Saldo disponível em cada conta corrente')
                        )
                    ),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='grafico1', className='dbc', config=config_graph, figure=grafico1)
                        ], sm=12, md=12)
                    ])
                ])
            ], style=tab_card)
        ], sm=12, lg=10)

    ], className='g-2 my-auto', style={'margin-top': '7px'}),

    # ========== Row 2 ============

    dbc.Row([

        dbc.Col([
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            dash_table.DataTable(
                                style_data={
                                    'whiteSpace': 'normal',
                                    'height': 'auto',
                                },
                                data=cred_disponivel.to_dict('records'),
                                columns=[{'id': c, 'name': c} for c in cred_disponivel.columns]),
                        ]
                    )
                ],
                style=tab_card, className='w-100')
        ], sm=12, lg=12)

    ], className='g-2 my-auto', style={'margin-top': '7px'})

], fluid=True, style={'height': '100vh'})

# =========== callbacks ===========


if __name__ == '__main__':
    app.run_server(debug=True)