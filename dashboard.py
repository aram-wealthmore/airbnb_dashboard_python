# dashboard.py

from dash import Dash, html, dcc
import requests
import plotly.graph_objects as go

app = Dash(__name__)

# Fetch data from the server
response = requests.get('http://127.0.0.1:5000/locations/average')
data = response.json()


# Process the data
locations = data['data']
geojson_data = data['geojson']

# Debugging: Print processed data
print(locations[:5])
# print(geojson_data[:5])


def create_map(locations, geojson_data):
    """
    Creates a map component for Dash using location data and GeoJSON data.
    """
    fig = go.Figure(go.Choroplethmapbox(
        geojson=geojson_data,
        locations=[location['neighbourhood'] for location in locations],
        z=[location['average_rating'] for location in locations],
        featureidkey="properties.neighbourhood",
        colorscale="Viridis",
        colorbar_title="Average Rating",
        marker_opacity=0.5,
        marker_line_width=0,
        customdata=[[location['average_price']] for location in locations]
    ))

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=10,
        mapbox_center={"lat": 39.7392, "lon": -104.9903},
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    fig.update_traces(
        hovertemplate="<b>%{location}</b><br>Average Rating: %{z:.2f}<br>Average Price: %{customdata[0]:.2f}"
    )

    return fig


def create_table(locations, keys=[{'label': 'Test Label', 'value': 'test_value'}]):
    """
    Creates a table component dynamically based on the keys provided.
    """
    return html.Table([
        html.Thead(
            html.Tr([html.Th(key['label']) for key in keys])
        ),
        html.Tbody([
            html.Tr([
                html.Td(location[key['value']]) for key in keys
            ]) for location in locations
        ])
    ])


app.layout = html.Div(children=[
    html.H1(children='AirBnB Average Reviews in Denver'),
    dcc.Graph(
        id='average-review-map',
        figure=create_map(locations, geojson_data)
    ),

    # Uncomment the following line to display the table
    create_table(locations, keys=[{'label': 'Neighbourhood', 'value': 'neighbourhood'}, {
                                'label': 'Average Rating', 'value': 'average_rating'}, {'label': 'Average Price', 'value': 'average_price'}])
])

if __name__ == '__main__':
    app.run_server(debug=True)
