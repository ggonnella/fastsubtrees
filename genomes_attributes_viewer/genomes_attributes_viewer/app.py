#!/usr/bin/env python3
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash.exceptions import PreventUpdate
import plotly.express as px
import dash_bootstrap_components as dbc
import json
import pandas as pd
import fastsubtrees
import genomes_attributes_viewer as gav

fastsubtrees.PROGRESS_ENABLED = True
fastsubtrees.enable_logger("INFO")

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

with open(f'{gav.workdir}/{gav.SCIENTIFIC_NAMES}') as f:
  data = f.read()
options = json.loads(data)

app.layout = html.Div(style={'marginLeft': '2%',
                             'marginRight': '2%'}, children=[
  html.H1(style={'textAlign': 'center'}, children='Genomes Attributes Viewer'),
  dbc.NavbarSimple(
    children=[
      dbc.NavItem(dbc.NavLink("Comparison", active=True, disabled=True)),
    ],
    brand="Genomes Attributes Viewer",
    color="primary",
    dark=True,
  ),
  html.Br(),
  html.Div(children=[
    dbc.Row([
      dbc.Col(html.H2('Select Attribute'))
    ]),
    dbc.Row([
      dbc.Col(dcc.Dropdown(
        id='attributes-dropdown',
        options=[{'label': 'genome size', 'value': 'genome size'},
                 {'label': 'GC content', 'value': 'GC content'}],
        value='genome size'
      ), align='center', width=3)
    ]),
    html.Br(),
    html.Div(style={'display': 'block'}, children=[
      dbc.Button('Add Taxon', color='primary', n_clicks=0,
                 outline=True, id='add-comparison',
                 style={'marginRight': '2%'}),
      dbc.Button('Compare', color='success', n_clicks=0, outline=True,
                 id='compare')
    ])
  ]),
  html.Br(),
  html.Div(id='container', children=[]),
  html.Br(),
  html.Div(children=[
    dbc.Row([
      dbc.Col(dcc.Graph('boxplot')),
      dbc.Col(dcc.Graph('histogram'))
    ])
  ])
])

@app.callback(
  Output('container', 'children'),
  Input('add-comparison', 'n_clicks'),
  State('container', 'children')
)
def create_container(n_clicks, div_children):
  new_child = html.Div(
    style={
      'width': '50%',
      'display': 'inline-block'
    },
    children=[
      dbc.Col([
        dcc.Dropdown(
          id={
            'type': 'dynamic-dropdown',
            'index': n_clicks
          },
          placeholder='Enter organism name or tax id',
        ),
      ]
      ),
    ]
  )
  div_children.append(new_child)
  return div_children

@app.callback(
  Output({'type': 'dynamic-dropdown', 'index': MATCH}, 'options'),
  Input(component_id={'type': 'dynamic-dropdown', 'index': MATCH}, \
        component_property='search_value')
)
def update_dropdown_values(search_value):
  if not search_value:
    raise PreventUpdate
  else:
    i = 1
    lst = []
    for o in options:
      if i <= 10:
        if search_value in o['label']:
          i += 1
          lst.append(o)
    return lst

@app.callback(
  Output('compare', 'disabled'),
  Input('add-comparison', 'n_clicks')
)
def enable_compare_button(clicks):
  if clicks >= 1:
    return False
  else:
    return True

@app.callback(
  Output('boxplot', 'figure'),
  Output('boxplot', 'style'),
  Output('histogram', 'figure'),
  Output('histogram', 'style'),
  Output('add-comparison', 'disabled'),
  Input('compare', 'n_clicks'),
  Input('attributes-dropdown', 'value'),
  Input(component_id={'type': 'dynamic-dropdown', 'index': ALL},
        component_property='value'),
)
def update_figure(clicks, attribute, taxid):
  attribute = attribute.replace(' ', '_')
  attribute = attribute
  boxplot_dict = {}
  final_values = []
  treefname = f'{gav.workdir}/{gav.TREEFILE}'
  tree = fastsubtrees.Tree.from_file(treefname)
  if clicks >= 1:
    for id in taxid:
      if id is None:
        continue
      boxplot_dict[id + ')'] = []
      my_str = id.partition('(')[-1]
      subtree_root = int(my_str)
      attribute_list = tree.subtree_attribute_data(subtree_root, attribute)
      sublist = list()
      for att in attribute_list:
        if att is not None:
          for i in att:
            sublist.append(i)
      final_values.append(sublist)
      sublist = []
    list_len = [len(i) for i in final_values]
    for i in final_values:
      if len(i) != max(list_len):
        i.extend([None] * (max(list_len) - len(i)))
    for index, key in enumerate(boxplot_dict):
      boxplot_dict[key] = final_values[index]
    boxplot_dict = pd.DataFrame(boxplot_dict)
    boxplot_dict = pd.melt(boxplot_dict, var_name='taxon')
    boxplot = px.box(data_frame=boxplot_dict, x='taxon', y='value', labels={
      'value': attribute,
    })
    pd.melt(boxplot_dict).to_csv(index=False)
    histogram = px.histogram(data_frame=boxplot_dict, x='value', color='taxon')
    return boxplot, {'display': 'block'}, histogram, {'display': 'block'}, True
  else:
    return {}, {'display': 'none'}, {}, {'display': 'none'}, False
