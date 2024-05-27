# Section Two: Data Processing

## Step 6: Create Average Review Map in Dash

In this step, we will refactor our `dashboard.py` to fetch data from our server endpoint and display a map color-coded by average review scores. The map will show the average price and neighborhood name when you hover over it.

### Goals

- Fetch data from the server endpoint.
- Use the GeoJSON response and the array of location data to display a map.
- Color code the map by average review score.
- Display average price and neighborhood name on hover.

### Prerequisites

Ensure your Flask server and Docker PostgreSQL database are, and that the endpoint `/locations/average` is accessible. If not, start it using:

```bash
# Check if the PostgreSQL container is running
docker-compose ps

# If not, start it
docker-compose up -d

# Start the Flask server
python server.py

# Test the endpoint
curl http://127.0.0.1:5000/locations/average

# Expected output
# {
#   "data": [
#     {
#       "neighbourhood": "Five Points", // Remember, we are using neighbourhood instead of  neighborhood_name to match our GeoJSON data
#       "average_rating": 4.5,
#       "average_price": 100.0
#       "latitude": 39.7547,
#         "longitude": -104.9773,
#     },
#     ...
#   ],
#   "geojson": {
#     "type": "FeatureCollection",
#     "features": [
#       {
#         "type": "Feature",
#         "properties": {
#           "neighbourhood": "Five Points"
#         },
#         "geometry": {
#           "type": "Polygon",
#           "coordinates": [
#             ...
#           ]
#         }
#       },
#       ...
#     ]
#   }
# }
```

### Step-by-Step Instructions

#### 1. Set Up Basic Structure in `dashboard.py`

First, we will set up the basic structure for our Dash application, removing the dummy data and preparing to fetch data from the server.

```python
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
# print(locations[:5]) # If you want to see the first 5 locations, uncomment this line

app.layout = html.Div(children=[
    html.H1(children='AirBnB Average Reviews in Denver'),
    dcc.Graph(id='average-review-map')
])

if __name__ == '__main__':
    app.run_server(debug=True)
```

This sets up the basic structure of our Dash application and fetches data from the server.

#### 2. Create a Reusable Function for the Map Component

Next, we will create a reusable function that takes in the array of location data and the GeoJSON data as properties and returns a graph component for Dash.

```python
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

app.layout = html.Div(children=[
    html.H1(children='AirBnB Average Reviews in Denver'),
    dcc.Graph(
        id='average-review-map',
        figure=create_map(locations, geojson_data)
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
```

This code creates a reusable function `create_map` that generates a map component for Dash using the location data and GeoJSON data.

#### 3. Update the Map Component with Hover Information

We will now update the map component to include hover information for average price and neighborhood name.

```python
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

app.layout = html.Div(children=[
    html.H1(children='AirBnB Average Reviews in Denver'),
    dcc.Graph(
        id='average-review-map',
        figure=create_map(locations, geojson_data)
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
```

This code updates the `create_map` function to include hover information for average price and neighborhood name, displaying it on the map when you hover over a neighborhood.

#### 4. Test the Dash Application

Run the Dash application:

```bash
python dashboard.py
```

Open your web browser and navigate to [http://127.0.0.1:8050](http://127.0.0.1:8050). You should see a map of Denver color-coded by average review scores, with average price and neighborhood name displayed on hover.

### Summary

In this step, you have:

- Set up the basic structure of a Dash application.
- Fetched data from the server endpoint.
- Created a reusable map component for Dash.
- Displayed a map color-coded by average review scores with hover information for average price and neighborhood name.

This completes the process of creating a Dash application to visualize data fetched from a Flask API endpoint.
