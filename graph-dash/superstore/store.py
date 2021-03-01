#!/usr/bin/env python3

import pandas as pd
import numpy as np
import datetime
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

df = pd.read_csv('https://raw.githubusercontent.com/fajarslvn/machine_learning/main/superstore-sales-analysis/superstore_sales.csv')

df['order_date'] = pd.to_datetime(df['order_date'], format='%Y-%m-%d')
df['ship_date'] = pd.to_datetime(df['ship_date'], format='%Y-%m-%d')

def overall_sales():
    df['month_year'] = df['order_date'].apply(lambda x: x.strftime('%Y-%m'))
    overall_sales = df.groupby(['month_year', 'year'])['sales'].sum().reset_index()
    overall_trend = overall_sales.sort_values(by=['sales'], ascending=False)
    return html.Div([
        html.H4('Sales Trend', 
        style={'text-align':'center', 'color':'white'}),

        dcc.Graph(figure = px.bar(overall_trend, x='month_year', y='sales', color='year', barmode='group', height=350, labels={'month_year':'Sales per-Months (Year)', 'sales':'Number of Sales'}).update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor':'rgba(0, 0, 0, 0)'}, font={'color':'#839496'}), config={'displayModeBar': False})
    ])

def get_word(w):
  return w.split(', ')[0]

def get_name(x):
    return x.split(' ')[2]

df['product'] = df['product_name'].apply(lambda x: f'{get_word(x)}')
df.drop(['product_name'], inplace=True, axis=1)

def top_3_prod():
    prod_sales = df.groupby(['product', 'year'])['sales'].sum().reset_index()
    prod_sales5 = prod_sales.sort_values(by=['sales'], ascending=False).iloc[0:4]
    return html.Div([
        html.H4('Top 3 Sales by Products', style={'text-align':'center', 'color':'white'}),
        dcc.Graph(figure = px.bar(prod_sales5, x='product', y='sales', color='year', barmode='group', height=350, 
        labels={'product':'Top 3 Sales by Products', 'sales':'Number of Sales', 'year':'Range by Year'})
             .update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor':'rgba(0, 0, 0, 0)'}, font={'color':'#839496'},xaxis=dict(showgrid=True), yaxis=dict(showgrid=True)), config={'displayModeBar': False})
    ])

def most_sales_prod():
    most_sales = df.groupby(['product', 'year'])['quantity'].sum().reset_index()
    most_sales_top = most_sales.sort_values(by=['quantity'], ascending=False).iloc[0:10]
    return html.Div([
        html.H4('Most Selling Products', style={'text-align':'center', 'color':'white'}),
        html.Ul(children=[html.Li(i) for i in most_sales_top['product']],
        style={'textAlign': 'left', 'color': '#839496','fontSize': 18, 'height':'333px', 'padding-top':'15px'})
    ])

def category():
  df_cat = df.groupby('category')['profit'].sum().reset_index()
  df_cat.sort_values(by=['profit'], ascending=False)
  return html.Div([
    html.H4('Most Profitable Category', style={'text-align':'center', 'color':'white'}),
    dcc.Graph(figure = px.pie(df_cat, values='profit', names='category', height=350, labels={'profit':'Profit'}).update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor':'rgba(0, 0, 0, 0)'}, font={'color':'#839496'}, legend_orientation='h', xaxis=dict(showgrid=True), yaxis=dict(showgrid=True)), config={'displayModeBar': False})
  ])

def ship_mode():
    return html.Div([
        html.H4('Most Preferred Shipping Mode', style={'text-align':'center', 'color':'white'}),
        dcc.Graph(figure = px.histogram(df, x='ship_mode', color='ship_mode', height=350, labels={'ship_mode':'Shipping Mode'})
        .update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor':'rgba(0, 0, 0, 0)'}, font={'color':'#839496'}, xaxis=dict(showgrid=True), yaxis=dict(showgrid=True)), 
        config={'displayModeBar': False})
    ])
  
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR],
                meta_tags=[{'name':'viewport',
                'content':'width=device-width, initial-scale=1.0'}])
                
# server = app.server

app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(
                html.H2('Super Store Dashboard', style={'color':'white'}, 
                className='text-center xs-6 sm-6 md-6 lg-4 xl-4'), 
                xs=12, sm=12, md=12, lg=12, xl=12), 
    style={'padding-top':'30px', 'padding-bottom':'30px'}, justify='around'),

    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    overall_sales()
                    ]), className='col-con'
            )
        ], xs=12, sm=12, md=12, lg=5, xl=5),
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    top_3_prod()
                    ]), className='col-con'
            )
        ], xs=12, sm=12, md=12, lg=4, xl=4),
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    most_sales_prod()
                    ]), className='col-con'
            )
        ], xs=12, sm=12, md=12, lg=3, xl=3),
    ], style={'padding-bottom':'30px'}, justify='around'),
    
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    category()
                    ]), className='col-con'
            )
        ], xs=12, sm=12, md=12, lg=4, xl=4),
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H4('Most Profitable Sub Category', style={'color':'white'}, className='text-center'),
                    dbc.RadioItems(id='radio_sub', value='Sub Category', className='text-center',
                            options=[{'label':'Sub Category', 'value':'Sub Category'}, {'label':'Region', 'value':'Region'},], inline=True),

                    dcc.Graph(id='sub_fig', config={'displayModeBar': False}, className='text-center')
                ]), className='col-con'
            )
        ], xs=12, sm=12, md=12, lg=4, xl=4),
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    ship_mode()
                    ]), className='col-con'
            )
        ], xs=12, sm=12, md=12, lg=4, xl=4),
    ], style={'padding-bottom':'30px'}, justify='around')
], fluid=True)

# Define callback to update graph
@app.callback(Output('sub_fig', 'figure'),
              Input('radio_sub', 'value'))

def update_graph(radio_sub):
  most_profit_sub = df.groupby('sub_category')[['profit', 'product']].sum().reset_index()
  sub_top_profit= most_profit_sub.sort_values(by=['profit'], ascending=False).iloc[0:10]
  region = df.groupby(['year', 'segment', 'region'])['profit'].sum().reset_index()
  region_top = region.sort_values(by=['profit'], ascending=False).iloc[0:10]

  if radio_sub == 'Sub Category':
      fig = px.bar(sub_top_profit, x='sub_category', y='profit', 
                  color='sub_category', height=326, labels={'sub_category':'Sub Category', 'profit':'Profit'})
      fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor':'rgba(0, 0, 0, 0)'}, 
                        xaxis=dict(showgrid=True), yaxis=dict(showgrid=True), font={'color':'#839496'})
      return fig

  elif radio_sub == 'Region':
      fig = px.bar(region_top, x='region', y='profit', 
                  color='region', labels={'region_top':'Region', 'profit':'Profit'})
      fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor':'rgba(0, 0, 0, 0)'}, 
                        xaxis=dict(showgrid=True), yaxis=dict(showgrid=True), font={'color':'#839496'})
      return fig

if __name__ == '__main__':
  app.run_server(debug=False)
  
