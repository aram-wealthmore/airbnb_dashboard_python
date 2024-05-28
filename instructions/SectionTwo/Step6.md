# Section Two: Data Processing

## Table of Contents

- [Step 6: Create Average Review Map in Dash](#step-6-create-average-review-map-in-dash)
  - [Goals](#goals)
  - [Prerequisites](#prerequisites)
  - [Step-by-Step Instructions](#step-by-step-instructions)
    - [1. Set Up Basic Structure in `dashboard.py`](#1-set-up-basic-structure-in-dashboardpy)
    - [2. Create a Reusable Function for the Map Component](#2-create-a-reusable-function-for-the-map-component)
    - [3. Update the Map Component with Hover Information](#3-update-the-map-component-with-hover-information)
    - [4. Test the Dash Application](#4-test-the-dash-application)
  - [Summary](#summary)

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

We will do this by importing the necessary libraries, fetching data from the server endpoint, and processing the data to extract the locations and GeoJSON data.

A new tool at this point is the `requests` library. This library allows you to send HTTP requests to a server and receive a response. In this case, we will use it to fetch data from the server endpoint.

Basically, this allows us to 'talk' to the code in our server.py file from our dashboard.py file. This is a common pattern in web development, where you have a front-end (the Dash application) and a back-end (the Flask server), where the back-end communicates with the database (Docker PostgreSQL).

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
```

This code creates a reusable function `create_map` that generates a map component for Dash using the location data and GeoJSON data.

#### 3. Add the Map Component to the Dash Application

Now, we will update the layout of our Dash application to include the map component. We can adjust app.page to include the map component by calling the `create_map` function with the locations and geojson_data as arguments. We already have dcc.Graph with the id `average-review-map` in our layout, so we can update the figure property of this graph to include the map component.

```python
# dashboard.py


app.layout = html.Div(children=[
    html.H1(children='AirBnB Average Reviews in Denver'),
    dcc.Graph(
        id='average-review-map',
        figure=create_map(locations, geojson_data)
    )
])

```

This code updates the layout of the Dash application to include the map component generated by the `create_map` function.

#### 4. Add a data table component

At this point, if you look at the Dash application, you will see a map of Denver color-coded by average review scores. However, we can also add a data table component to display the neighborhood, average rating, and average price for each location. When presenting data in an application versus a report, it is often useful to provide multiple ways to view the data, such as through a map and a table.

Just like we made the function create_map as a reusable function, we can also create a function to generate a data table component. This function will take in the locations data and the keys of the column, and return a data table component for Dash.

```python
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

```

This function takes in two arguments, locations and keys. Locations is the data that we want to display in the table, and keys is a list of dictionaries that contain the label and value of the columns we want to display in the table. The function then generates a table component for Dash using the provided data and keys.

We can take a look at how to use this in practice by adjusting adjusting our app layout to include the table component.

```python
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
```

This code adds a data table component to the Dash application, displaying the neighborhood, average rating, and average price for each location.

#### 5. Test the Dash Application

Once you put it all together, your `dashboard.py` should look like this:

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
# print(geojson_data[:5]) # If you want to see the first 5 locations, uncomment this line


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
```

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
