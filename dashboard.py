# dashboard.py

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# Create a simple DataFrame
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Grapes"],
    "Amount": [4, 1, 2, 5]
})

# Create a bar chart
fig = px.bar(df, x="Fruit", y="Amount", title="Dummy Fruit Data")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)