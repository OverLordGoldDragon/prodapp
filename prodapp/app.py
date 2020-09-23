# -*- coding: utf-8 -*-
# http://127.0.0.1:8050/
import os
import argparse
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

from flask import send_from_directory
from dash.dependencies import Input, Output
from app_state import AppState, Countdown

Div = html.Div
ctx = dash.callback_context

import plotly.io as pio
pio.kaleido.scope.default_width = 1000

#%%
app = dash.Dash(__name__, update_title=None)
app.css.config.serve_locally = True
#%%
def interpolate_index(self, **kwargs):
    kwargs['title'] = 'ProdApp'
    return dash.Dash.interpolate_index(self, **kwargs)
app.interpolate_index = interpolate_index.__get__(app)
#%%
btn0 = dict(className='playbtn', n_clicks=0)
btn1 = dict(className='playbtn', n_clicks=0,
            style={'position': 'absolute', 'left': '35%', 'top': '62%'})
btn2 = dict(className='playbtn', n_clicks=0,
            style={'position': 'absolute', 'left': '49%', 'top': '62%'})
graph_cfg = {'config': {'displayModeBar': False,
                        'displaylogo': False}}
ctd_graph_cfg = graph_cfg.copy()
ctd_graph_cfg.update({
    'style': {'width': '100%', 'height': '100%', 'padding': 0, 'margin': 0},
})
#%%
graphDiv = Div(
    style={'width': '80%', 'position': 'absolute', 'left': '5%'},
    children=[
        Div(className='grbkg', children=[
            dcc.Graph(id='prod-graph', **graph_cfg)
        ]),
        html.Button('+5',  id='+5',  **btn0),
        html.Button('+10', id='+10', **btn0),
        html.Button('+15', id='+15', **btn0)
    ],
)
ctdDiv = Div(
    style={'position': 'absolute', 'top': '65%', 'left': '82%'},
    children=[
        Div(className='clockContainer',
            style={'top': '50%', 'width': '200px', 'height': '200px'},
            children=[
                Div(className='clockOuter'),
                Div(className='clockInner'),
                Div(style={'height': '100%', 'width': '100%'},
                    children=[
                        dcc.Input(id='clockInput', value='0:00', type='text',
                                  className='clockTxt'),
                        Div(id='clockOutput', children=['0:00'],
                            className='clockTxt'),
                        ]),
                html.Button(u'\u25B6', id='start', **btn1),
                html.Button(u'\u2B6F', id='reset', **btn2),
            ],
        ),
        dcc.Interval(id='counter',
                     interval=1000,
                     n_intervals=0),
])
orbDiv = Div(
    style={'position': 'absolute', 'top': '16%', 'right': '0', 'width': '20%'},
    children=[
        Div(className='plane smain', children=[
            Div(className='circle'),
            Div(className='circle'),
            Div(className='circle'),
            Div(className='circle'),
            Div(className='circle'),
            Div(className='circle'),
        ]),
    ],
)
#%%
app.layout = Div(
    className='row',
    children=[
        html.Link(rel='stylesheet',
                  href='/static/style.css?version=98'),
        Div(className='main bkgrad', children=[
            graphDiv,
            ctdDiv,
            ]),
        Div(className='right', children=[orbDiv]),
        Div(id='dummy', style={'display': 'none'}),
])
#%%
bar_cfg = {'layout': dict(
    barmode="relative",
    colorway=['#FF0303', '#56AFF3'],
    showlegend=False,
)}
layout_cfg = {
    'xaxis': dict(tickmode='linear', tick0=0, dtick=1),
    'yaxis': dict(range=[0, 60]),
    'margin': dict(l=0, r=10, b=0, t=40),
    'plot_bgcolor': 'white',
}
xaxes_cfg = dict(
    title={'text': ''},
    showgrid=True,
    gridcolor='rgba(0, 0, 0, .12)',
    tickson='boundaries',
    tickfont={'size': 12},
    tickangle=0,
)
yaxes_cfg = xaxes_cfg.copy()
del yaxes_cfg['tickfont']
#%%
def get_data_objects():
    return [go.Bar(x=state.hour, y=state.super_productivity,
                   name='SuperProductivity'),
            go.Bar(x=state.hour, y=state.productivity,
                   name='Productivity')]

@app.callback(Output('prod-graph', 'figure'),
              [Input('+5',  'n_clicks'),
               Input('+10', 'n_clicks'),
               Input('+15', 'n_clicks')])
def update_prod(cl5, cl10, cl15):
    # data_before = get_data_objects()  # animation attempt for smooth transitions
    state.update(ctx)
    data_after = get_data_objects()

    fig = go.Figure(data=data_after,  # change to `data_before` for anim
                    # frames=[go.Frame(data=data_before),
                    #         go.Frame(data=data_after)],
                    **bar_cfg)
    fig.update_layout(title={'x': .5, 'text': state.date}, **layout_cfg)
    fig.update_xaxes(**xaxes_cfg)
    fig.update_yaxes(**yaxes_cfg)

    if state.savepath is not None:
        state.save()
        fig.write_image(state.imsavepath)
    return fig
#%%# Countdown callbacks #####################################################
@app.callback([Output('clockOutput', 'children'),
               Output('clockOutput', 'style'),
               Output('clockInput', 'style'),
               Output('start', 'children')],
              [Input('counter', 'n_intervals'),
               Input('start', 'n_clicks'),
               Input('reset', 'n_clicks')])
def update_countdown(ticks, start_cl, reset_cl):
    ctd.update_t(ctx)

    if ctd.paused:
        co_style = {'display': 'none'}
        ci_style = {'display': 'inherit'}
    else:
        co_style = {'display': 'inherit'}
        ci_style = {'display': 'none'}

    start_txt = u'\u25B6' if ctd.paused else '| |'  # u'\u25A0' alt pause
    return ctd.t_str, co_style, ci_style, start_txt
#%%
@app.callback(Output('clockInput', 'value'),
              [Input('start', 'n_clicks'),
               Input('reset', 'n_clicks')])
def update_clockInput(start_cl, reset_cl):
    if 'reset.n_clicks' in dash.callback_context.triggered[0]['prop_id']:
        return "{}:{:02d}".format(ctd.t_max // 60, ctd.t_max % 60)
    return ctd.t_str
#%%
@app.callback(Output('dummy', 'children'),
              [Input('clockInput', 'value')])
def update_t_from_clockInput(t_input):
    ctd.t = t_input
    if ctd.at_reset:
        ctd.t_max = ctd.t
#%%# Local CSS loading #######################################################
@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)
#%%# Execution ###############################################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run productivity app.")
    parser.add_argument('--savepath', default='auto',
                        help="Path (.csv) to save app data to.")
    parser.add_argument('--loadpath', default='auto',
                        help="Path (.csv) to load app data from.")
    parser.add_argument('--imsavepath', default='auto',
                        help="Path (.png) to save app figure to.")
    parser.add_argument('--read-only', action='store_true',
                        help=("Run app in read-only mode (cannot save / update "
                              "loaded file, if any)"))

    args = parser.parse_args()
    state = AppState(**vars(args))

    # read configs to set in Countdown
    t_max, t_min, bleeps = 600, 0, 2  # defaults
    with open('config.ini', 'r') as f:
        txt = [line.strip(' \n') for line in f.read().split('\n')]
        for line in txt:
            if line.startswith('t_max'):
                t_max  = int(line.split('=')[-1])
            elif line.startswith('t_min'):
                t_min  = int(line.split('=')[-1])
            elif line.startswith('bleeps'):
                bleeps = int(line.split('=')[-1])

    ctd = Countdown(t_max=t_max, t_min=t_min, bleeps=bleeps)
    app.run_server(debug=False)
