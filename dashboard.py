#Bibliotecas
#============requerements===========


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go

import numpy as np
import pandas as pd
import json

#============CONSTANTE DE LATITUDE E LONGITUDE=============
CENTER_LAT, CENTER_LON = -20.3222, -40.3381


#================site com a base em csv de covid ==============
#https://covid.saude.gov.br/
#================TRATANDO OS DADOS CSV===================
# df = pd.read_csv("HIST_PAINEL_COVIDBR_2023_Parte1_04abr2023.csv", sep=';')
# df_states = df[(~df["estado"].isna()) & (df["codmun"].isna())]
# df_brasil = df[df["regiao"] == "Brasil"]
# df_states.to_csv("df_states.csv")
# df_brasil.to_csv("df_brasil.csv")

#========LENDO ARQUIVO TRATADO=========
df_states = pd.read_csv("df_states.csv")
df_brasil = pd.read_csv("df_brasil.csv")

df_states_ = df_states[df_states["data"] == "2023-02-21"]
#============LENDO ARQUIVOS JSON para saber os tipos de dados==================
brazil_states = json.load(open("./geojson/brazil_geo.json", "r"))

#---------Estado do grafico de barras---------
df_data = df_states[df_states["estado"] == "ES"]
# type(brazil_states)
# brazil_states.keys()
# type.brazil_states["features"]

#dicionario de selecoes
select_columns = {"casosAcumulado":"Casos Acumulados",
                  "casosNovos":"Novos Casos",
                  "obitosAcumulado": "Óbitos Totais",
                  "obitosNovos": "Óbitos por Dia"}


#==================CRIANDO O MAPA==================
#INSTANCIANDO O DASH-----USANDO O TEMA CYBORG-----
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

#elemento que vai conter o mapa
fig = px.choropleth_mapbox(df_states_, locations="estado", color="casosNovos",
                        center={"lat": CENTER_LAT, "lon": CENTER_LON},zoom=5,
                         geojson=brazil_states, color_continuous_scale="Redor",
                         opacity=0.4, hover_data={"casosAcumulado": True, 
                        "casosNovos": True, "obitosNovos": True, "estado": True})

#Estilo do Mapa
fig.update_layout(
    paper_bgcolor="#242424",
    autosize=True,
    margin=go.Margin(l=0, r=0, t=0, b=0),
    showlegend=False,
    mapbox_style="carto-darkmatter"
)

#======Gráfico 2=======

fig2 = go.Figure(layout={"template":"plotly_dark"})
fig2.add_trace(go.Scatter(x=df_data["data"], y=df_data["casosAcumulado"]))
fig2.update_layout(
    paper_bgcolor="#242424",
    plot_bgcolor="#242424",
    autosize=True,
    margin=dict(l=10, r=10, t=10, b=10)

)

#==============CONSTRUINDO LAYOUT==============

app.layout = dbc.Container(
    dbc.Row([
       
        dbc.Col([
            html.Div([
                html.Img(id="logo", src=app.get_asset_url("logo_initiare.png"),height=50),
                html.H4("Criado por AGNELO"),
                html.H5("Evolução COVID-19"),
                dbc.Button("BRASIL", color="primary", id="location-button", size="lg")
            ], style={}),
            html.P("Infome a data na qual deseja obter informações:", style={"margin-top":"40px"}),
            html.Div(id="div-test", children=[
                dcc.DatePickerSingle(
                    id="date-picker",
                    min_date_allowed=df_brasil["data"].min(),
                    max_date_allowed=df_brasil["data"].max(),
                    initial_visible_month=df_brasil["data"].min(),
                    date=df_brasil["data"].max(),
                    display_format="MMMM D, YYYY",
                    style={"border":"0px solid brack"}
                ),
            ]),
            #cards de informações
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Casos Recuperados"),
                            html.H3(style={"color":"#adfc92"}, id="casos-recuperados-text"),
                            html.Span("Em acompanhamento"),
                            html.H5(id="em-acompanhamento-text"),
    
                        ])
                    ], color="light", outline=True, style={"margin-top":"10px",
                                                           "box-shadow":"0 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0)",
                                                           "color":"#FFFFFF"})
                ], md=4),

                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Casos Confirmados"),
                            html.H3(style={"color":"#389fd6"}, id="casos-confirmados-text"),
                            html.Span("Novos Casos na Data"),
                            html.H5(id="novos-casos-text"),
    
                        ])
                    ], color="light", outline=True, style={"margin-top":"10px",
                                                           "box-shadow":"0 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0)",
                                                           "color":"#FFFFFF"})
                ], md=4),

                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Óbitos Confirmados"),
                            html.H3(style={"color":"#DF2935"}, id="obitos-text"),
                            html.Span("Óbitos na Data"),
                            html.H5(id="obitos-na-data-text"),
    
                        ])
                    ], color="light", outline=True, style={"margin-top":"10px",
                                                           "box-shadow":"0 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0)",
                                                           "color":"#FFFFFF"})
                ], md=4),
            ]),

            #seletor de tipos
            html.Div([
                
                html.P("Selecione o tipo de dados que deseja visualizar:", style={"margin-top": "25px"}),
                dcc.Dropdown(id="location-dropdown",
                             options=[{"label": j, "value": i} for i, j in select_columns.items()],
                             value="casosNovos",
                             style={"margin-top": "10px"}
                             ),
                #grafico
                dcc.Graph(id="line-graph", figure=fig2)
            ])

            
        ], md=5, style={"padding":"25px", "backgound-color":"#242424"}),
        dbc.Col([
            dcc.Loading(id="loadding-1", type="default",
                        children=[dcc.Graph(id="choropleth-map", figure=fig, style={"height": "100vh", "margin-right": "10px"})
                                  ]
                                  )
            
        ], md=7)
    
    ])
, fluid=True)

#==========INTERATIVIDADE===============
#decoradores
@app.callback( 
        [
        Output("casos-recuperados-text", "children"),
        Output("em-acompanhamento-text", "children"),
        Output("casos-confirmados-text", "children"),
        Output("novos-casos-text", "children"),
        Output("obitos-text", "children"),
        Output("obitos-na-data-text", "children"),
        ],
        [Input("date-picker", "date"), Input("location-button", "children")]
)

#função dos indicadores de covid

def display_status(date, location):
    if location=="BRASIL":
        df_data_on_date = df_brasil[(df_brasil["data"] ==date)]
    else:
        df_data_on_date = df_states[(df_states["estado"]==location) & (df_states["data"]==date)]
    
    df_data_on_date["Recuperadosnovos"]
    
    recuperados_novos = "-" if df_data_on_date["Recuperadosnovos"].isna().values[0] else f'{int(df_data_on_date["Recuperadosnovos"].values[0]):,}'.replace(",",".")
    acompanhamentos_novos = "-" if df_data_on_date["emAcompanhamentoNovos"].isna().values[0] else f'{int(df_brasil["emAcompanhamentoNovos"].values[0]):,}'.replace(",",".")
    casos_acumulados = "-" if df_data_on_date["casosAcumulado"].isna().values[0] else f'{int(df_data_on_date["casosAcumulado"].values[0]):,}'.replace(",", ".")
    casos_novos = "-" if df_data_on_date["casosNovos"].isna().values[0] else f'{int(df_data_on_date["casosNovos"].values[0]):,}'.replace(",",".")
    obitos_acumulado = "-" if df_data_on_date["obitosAcumulado"].isna().values[0] else f'{int(df_data_on_date["obitosAcumulado"].values[0]):,}'.replace(",",".")
    obitos_novos = "-" if df_data_on_date["obitosNovos"].isna().values[0] else f'{int(df_data_on_date["obitosNovos"].values[0]):,}'.replace(",",".")

    return (recuperados_novos, acompanhamentos_novos, casos_acumulados, casos_novos, obitos_acumulado, obitos_novos)

#selecionar o dropdown e o grafico se alterar

@app.callback(Output("line-graph", "figure"), 
    [
        Input("location-dropdown", "value"), Input("location-button", "children"),
    ])

def plot_line_graph(plot_type, location):
    if location == "BRASIL":
        df_data_on_location = df_brasil.copy()
    else:
        df_data_on_location = df_states[df_states["estado"] == location]
    
    bar_plots = ["casosNovos", "obitosNovos"]

    fig2 = go.Figure(layout={"template": "plotly_dark"})
    if plot_type in bar_plots:
        fig2.add_trace(go.Bar(x=df_data_on_location["data"], y=df_data_on_location[plot_type]))
    else:
        fig2.add_trace(go.Scatter(x=df_data_on_location["data"], y=df_data_on_location[plot_type]))
    
    fig2.update_layout(
        paper_bgcolor='#242424',
        plot_bgcolor='#242424',
        autosize=True,
        margin=dict(l=10, r=10, b=10, t=10),
    )
    return fig2

@app.callback(
    Output("choropleth-map", "figure"),
    [Input("date-picker", "date")]
)

def update_map(date):
    df_data_on_states = df_states[df_states["data"] == date]
    
    fig = px.choropleth_mapbox(df_data_on_states, locations="estado", geojson=brazil_states,
        center={"lat":CENTER_LAT, "lon":CENTER_LON},#OBTIDO DO GOOGLE
        zoom=5, color="casosAcumulado", color_continuous_scale="Redor", opacity=0.55,
        hover_data={"casosAcumulado": True, "casosNovos": True, "obitosNovos":True, "estado":False}
    )

    fig.update_layout(paper_bgcolor="#242424", mapbox_style="carto-darkmatter", autosize=True, margin=go.layout.Margin(l=0, r=0, t=0, b=0), showlegend=False)

    return fig


#callback para selecionar o estado no mapa através de um click
@app.callback(
    Output("location-button", "children"),
    [Input("choropleth-map", "clickData"), Input("location-button", "n_clicks")]
)

def update_location(click_data, n_clicks):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if click_data is not None and changed_id != "location-button.n_clicks":
        state=click_data["points"][0]["location"]
        return "{}".format(state)
    else:
        return "BRASIL"
    
#===============PARA EXECUTAR O PROJETO===============

if __name__=="__main__":
    app.run_server(debug=True)

