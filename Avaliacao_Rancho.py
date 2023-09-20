import pandas as pd
import os
from datetime import datetime, timedelta, time
from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from collections import OrderedDict

arquivos = os.listdir('Dados')


def parser(data):
    return datetime.strptime(data, r"%d/%m/%Y")


cardapios = pd.read_excel('Cardapios\Cardapios.xlsx')
cardapios['Data'] = cardapios['Data'].astype(str)

avaliacoes = pd.DataFrame()

for arquivo in arquivos:
    avaliacao = pd.read_csv(f'Dados\{arquivo}', encoding='iso-8859-1',
                            sep=';', parse_dates=['Data'], date_parser=parser)
    avaliacao_tratada = avaliacao.drop(
        ['Status', 'Tempo', 'NomePerg.1', 'MAC', 'Id', 'FormatoData', 'escala1', 'Finalizador', 'NomePesquisa'], axis=1)
    tamanho = len(arquivo) - 4
    avaliacao_tratada['Ciclo'] = arquivo[:tamanho]
    avaliacoes = avaliacoes.append(avaliacao_tratada)
    # display(avaliacao_tratada)


avaliacoes = avaliacoes.loc[avaliacoes['Data'] > '2022-07-17', :]

avaliacoes = avaliacoes.reset_index()

avaliacoes['Data'] = avaliacoes['Data'].astype(str)

avaliacoes['Horax'] = ""
avaliacoes['Minuto'] = ""
avaliacoes['Dia'] = ""
avaliacoes['Mes'] = ""
avaliacoes['Data-Hora'] = ""
avaliacoes['Refeicao'] = ""
avaliacoes['Cardapio'] = ""

for j in range(len(cardapios)):
    data = str(cardapios['Data'][j])
    fuso = cardapios['Fuso'][j]
    almoco = cardapios['Almoço'][j]
    jantar = cardapios['Jantar'][j]

    for i in range(len(avaliacoes)):
        if str(avaliacoes['Data'][i]) == data:
            hora = str(avaliacoes['Hora'][i][0]) + \
                str(avaliacoes['Hora'][i][1])
            hora = int(hora) + fuso
            if hora > 23:
                hora = hora - 24
            if hora < 0:
                hora = hora + 24
            hora = str(hora)
            avaliacoes['Horax'][i] = hora

            if int(hora) < 16:
                avaliacoes['Refeicao'][i] = 'Almoço'
                avaliacoes['Cardapio'][i] = almoco
            else:
                avaliacoes['Refeicao'][i] = 'Jantar'
                avaliacoes['Cardapio'][i] = jantar

            minuto = str(avaliacoes['Hora'][i][3]) + \
                str(avaliacoes['Hora'][i][4])
            avaliacoes['Minuto'][i] = minuto

            segundo = str(avaliacoes['Hora'][i][6]) + \
                str(avaliacoes['Hora'][i][7])

            dia1 = str(avaliacoes['Data'][i][8]) + \
                str(avaliacoes['Data'][i][9])
            avaliacoes['Dia'][i] = dia1

            mes = str(avaliacoes['Data'][i][5]) + str(avaliacoes['Data'][i][6])
            avaliacoes['Mes'][i] = mes

            ano = str(avaliacoes['Data'][i][0]) + str(avaliacoes['Data'][i][1]) + \
                str(avaliacoes['Data'][i][2]) + str(avaliacoes['Data'][i][3])

            data_hora = datetime(int(ano), int(mes), int(
                dia1), int(hora), int(minuto), int(segundo))
            avaliacoes['Data-Hora'][i] = data_hora


avaliacoes['Resposta'] = avaliacoes['Perg. 1']*2
avaliacoes['Grau'] = ""

dict = {2: "Ruim", 4: "Regular", 6: "Bom", 8: "Muito bom", 10: "Excelente"}

avaliacoes = avaliacoes.loc[avaliacoes['Resposta'] > 0, :]

avaliacoes = avaliacoes.reset_index()

for y in range(len(avaliacoes)):
    grau = avaliacoes['Resposta'][y]
    avaliacoes['Grau'][y] = dict[grau]

# alimentar grafico de barras
avaliacao_diaria = avaliacoes.groupby(
    ['Data', 'Ciclo', 'Refeicao', 'Cardapio']).sum()
avaliacao_diaria = avaliacao_diaria.reset_index()
avaliacao_diaria['Resposta'] = avaliacao_diaria['Resposta'] / \
    avaliacao_diaria['Quantidade']
avaliacao_diaria = avaliacao_diaria.drop(
    ['level_0', 'index', 'Perg. 1'], axis=1)

avaliacao_diaria_almoco = avaliacao_diaria.loc[avaliacao_diaria['Refeicao'] == 'Almoço', :]
avaliacao_diaria_jantar = avaliacao_diaria.loc[avaliacao_diaria['Refeicao'] == 'Jantar', :]

# display(avaliacao_diaria_almoco)

avaliacao_mensal = avaliacoes.groupby(['Mes']).mean()
avaliacao_mensal = avaliacao_mensal.reset_index()
avaliacao_mensal = avaliacao_mensal.drop(
    ['level_0', 'index', 'Perg. 1'], axis=1)
avaliacao_diaria_tratado = avaliacao_diaria.loc[avaliacao_diaria['Data']
                                                > '2022-07-17', :]
por_cardapio_piores = avaliacao_diaria_tratado.groupby(['Cardapio']).mean(
    'Resposta').sort_values(by='Resposta', ascending=True)
por_cardapio_melhores = avaliacao_diaria_tratado.groupby(['Cardapio']).mean(
    'Resposta').sort_values(by='Resposta', ascending=False)
por_cardapio_melhores = por_cardapio_melhores.drop(['Quantidade'], axis=1)
por_cardapio_piores = por_cardapio_piores.drop(['Quantidade'], axis=1)
por_cardapio_melhores = por_cardapio_melhores.reset_index()
por_cardapio_piores = por_cardapio_piores.reset_index()


app = Dash(__name__)  # Criando o aplicato Dash no flask

# alimentar grafico de barras - almoco

fig1 = px.bar(data_frame=avaliacao_diaria_almoco, x='Data', y='Resposta', custom_data=[
              'Quantidade', 'Cardapio'], color='Ciclo', title='Feedback do almoço', barmode='group')

fig1.update_traces(
    hovertemplate="<br>".join([
        "Data: %{x}",
        "Resposta: %{y}",
        "Quantidade: %{customdata[0]}",
        "Cardapio: %{customdata[1]}"
    ])
)

# alimentar grafico de barras - jantar

fig2 = px.bar(data_frame=avaliacao_diaria_jantar, x='Data', y='Resposta', custom_data=[
              'Quantidade', 'Cardapio'], color='Ciclo', title='Feedback do jantar', barmode='group')

fig2.update_traces(
    hovertemplate="<br>".join([
        "Data: %{x}",
        "Resposta: %{y}",
        "Quantidade: %{customdata[0]}",
        "Cardapio: %{customdata[1]}"
    ])
)

# alimentar grafico de pizza - geral

fig3 = px.pie(avaliacoes, values='Quantidade', names='Grau')

# alimentar grafico de linha - geral

fig4 = px.line(avaliacao_mensal, x="Mes", y="Resposta",
               title="Avaliação Mensal", markers=True)
fig4.update_layout(yaxis_range=[0, 10])

lista_mes = list(avaliacoes['Mes'].unique())
lista_mes.append('Todos')

# layout
app.layout = html.Div(children=[

    html.H1(children='Pesquisa de Avaliação de Rancho',
            style={"text-align": "center"}),

    html.Div(children='Acompanhamento diário do rancho do Navio-Escola "Brasil" - XXXVI VIGM',
             style={"text-align": "center"}, id='subtitulo'),

    html.Div(children="___________________________________________________________________________________________________________________________________________________________________________________________________", style={
             "text-align": "center"}),

    html.Div(children="Meses:", style={"text-align": "left"}),

    dcc.RadioItems(lista_mes, value="Todos", id='meses'),

    html.Div(children='Melhores Cardápios', style={"text-align": "center"}),

    dash_table.DataTable(
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        data=por_cardapio_melhores.head(5).to_dict('records'),
        columns=[{'id': c, 'name': c} for c in por_cardapio_melhores.columns]),

    html.Div(children='Piores Cardápios', style={"text-align": "center"}),

    dash_table.DataTable(
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        data=por_cardapio_piores.head(5).to_dict('records'),
        columns=[{'id': c, 'name': c} for c in por_cardapio_piores.columns]),

    dcc.Graph(
        id='pizza',
        figure=fig3
    ),


    dcc.Graph(
        id='barra-almoco',
        figure=fig1
    ),

    dcc.Graph(
        id='barra-jantar',
        figure=fig2
    ),


    dcc.Graph(
        id='linha',
        figure=fig4
    ),
])

# callback


@app.callback(
    Output('pizza', 'figure'),
    Input('meses', 'value'),
)
def selecionar_nota(mes):  # a variável nota irá receber o valor do input
    if mes == 'Todos':
        fig3 = px.pie(avaliacoes, values='Quantidade', names='Grau')
    else:
        testex = avaliacoes.loc[avaliacoes['Mes'] == mes, :]
        fig3 = px.pie(testex, values='Quantidade', names='Grau')
    return fig3
    pass


if __name__ == '__main__':
    app.run_server(debug=False)

avaliacoes.to_excel('xxxx.xlsx')
