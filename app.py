import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from modules.Visualization import *
from modules.processing import *

# import dash_bootstrap_components as dbc
# external_stylesheets = [dbc.themes.DARKLY]
app = dash.Dash(__name__)

# set color scheme for plotly plots
colors = {
    'background': 'white',
    'text': 'black'
}

# read dataframe from csv and process it
df = pd.read_csv('assets/connectivity_task.csv')
df = clean_df(df)
df = process(df)

# connectivity ration on different aggregation levels
# 1. aggregated days
days_aggregated = connectivity_ratio(df, 'event_day')

# 2. aggregated organisations
org_aggregated = connectivity_ratio_ordered(df, 'organisation_name')

# 3. aggregated organisations
org_place_aggregated = connectivity_ratio_ordered(df, ['organisation_name', 'place_name'])

# 3. aggregated asset names
asset_names_aggregated = connectivity_ratio_ordered(df, 'asset_name')

# 4. aggregated week days
weekdays_aggregated = connectivity_ratio_ordered(df, 'week_day')

# plots for aggregated Dfs
figs = []

# Line Plot
figs.append(plotly_line(days_aggregated, x='event_day', y='count', color='event_type',
                        title='Connected Frequency Vs Disconnected by Day'))


# Bar Plots
def plolty_go_bar(df, x, title):
    y = df[df['event_type'] == 'Connected']
    y = y['count'].values

    z = df[df['event_type'] == 'Disconnected']
    z = z['count'].values

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x,
        y=y,
        name='Connected',
        marker_color='#5F9EA0'
    ))
    fig.add_trace(go.Bar(
        x=x,
        y=z,
        name='Disconnected',
        marker_color='#CD5C5C'
    ))
    fig.update_layout(barmode='stack', title=title)
    figs.append(fig)


bar_aggs = [org_aggregated, asset_names_aggregated, weekdays_aggregated]
x = ['organisation_name', 'asset_name', 'week_day']
bar_titles = ['Organisations Connectivity', 'Assests Connectivity', 'WeekDays Connectivity']
for i in range(len(bar_aggs)):
    plolty_go_bar(bar_aggs[i], bar_aggs[i][x[i]], bar_titles[i])

# apply colors on figure layout, #005f69, #001f3f

[fig.update_layout(
    plot_bgcolor='#001f3f',
    paper_bgcolor='#001f3f',
    font_color='beige'
) for fig in figs]

# App Layout
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H3(
        children='Plotly Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Connectivity Data Analytics.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Div(children=[

        html.Div(dcc.Dropdown(
            id='slct_org',
            options=[{'label': i, 'value': i} for i in org_place_aggregated['organisation_name'].unique()],
            value='Gonzalez-Hancock'),
            style={'width': "40%"}
        ),

        html.Div(dcc.Graph(
            id='places_org',
            figure={},
            style={'width': '800'}
        ), style={'display': 'inline-block'}),

        html.Div(dcc.Graph(
            id=figs[1].layout.title.text,
            figure=figs[1],
            style={'width': '800'}),
            style={'display': 'inline-block'})], style={'width': '100%', 'display': 'inline-block'}),

    html.Div(dcc.Graph(
        id=figs[0].layout.title.text,
        figure=figs[0])),

    html.Div(dcc.Graph(
        id=figs[2].layout.title.text,
        figure=figs[2]
    )),
    html.Div(dcc.Graph(
        id=figs[3].layout.title.text,
        figure=figs[3]
    ))

])


@app.callback(
    Output(component_id='places_org', component_property='figure'),
    Input(component_id='slct_org', component_property='value')
)
def update_graph(selected_organisation):
    filtered_org = org_place_aggregated[org_place_aggregated['organisation_name'] == selected_organisation]
    bar_fig = px.bar(filtered_org, x='place_name', y='count', color='event_type',
                     title=f'Places Connectivity in {selected_organisation} Organization')
    bar_fig.update_layout(
        plot_bgcolor='#001f3f',
        paper_bgcolor='#001f3f',
        font_color='beige')
    return bar_fig


if __name__ == '__main__':
    app.run_server(debug=True)
