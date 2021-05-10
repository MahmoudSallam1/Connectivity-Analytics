import plotly.express as px
import plotly.graph_objects as go


def plotly_line(df, x, y, color, title):
    fig = px.line(df, x=x, y=y, color=color, title=title)
    return fig


def plotly_bar(df, x, y, color, title):
    fig = px.bar(df, x=x, y=y, color=color, title=title)
    return fig


def plotly_go_bar_rotated_labels(df, x, title):
    y = df[df['event_type'] == 'Connected']
    y = y['count'].values

    z = df[df['event_type'] == 'Disconnected']
    z = z['count'].values

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x,
        y=y,
        name='Connected',
        marker_color='indianred'
    ))
    fig.add_trace(go.Bar(
        x=x,
        y=z,
        name='Disconnected',
        marker_color='lightsalmon'
    ))
    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='stack', xaxis_tickangle=-45, title=title)
    fig.show()


def plotly_go_bar(df, x, title):
    y = df[df['event_type'] == 'Connected']
    y = y['count'].values

    z = df[df['event_type'] == 'Disconnected']
    z = z['count'].values

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x,
        y=y,
        name='Connected',
        marker_color='indianred'
    ))
    fig.add_trace(go.Bar(
        x=x,
        y=z,
        name='Disconnected',
        marker_color='lightsalmon'
    ))
    fig.update_layout(barmode='stack', title=title)
    fig.show()
