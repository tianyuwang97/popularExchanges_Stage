# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options




df = pd.DataFrame({
    "nombre Agent": ["n=4", "n=4", "n=4", "n=4", "n=4", "n=4"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "categorie": ["MEM Best", "MEMA3>MEM", "MEMA4>MEM", "MEMA3+A4>MEM", "MEMA3+A4>MEM", "MEMA3+A4>MEM"]
})

print(df)

fig = px.bar(df, x="nombre Agent", y="Amount", color="categorie", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
