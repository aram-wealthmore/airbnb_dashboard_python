# Section Two: Data Processing

## Step 5: Create Flask Endpoints to Access Data

In this step, we will create a Flask API endpoint that queries the PostgreSQL database and returns the average review scores and average prices for neighborhoods. This data will be served at the endpoint `GET /locations/average`.

### Goals

- Set up a Flask application to serve API endpoints.
- Create an endpoint to return the average review scores and average prices for neighborhoods.
- Statically include the `denver_neighborhoods.geojson` data in the response.

### Prerequisites

Ensure you have the PostgreSQL container running in Docker. If not, start it using Docker Compose:

```bash
docker-compose up -d
```

### Step-by-Step Instructions

#### 1. Update `server.py` to Load GeoJSON Data

We will first update `server.py` to load the GeoJSON data that contains the neighborhood information. This data will be included in the response from our API endpoint.

```python
# server.py

from flask import Flask, jsonify
import json
from db_utils import execute_query

app = Flask(__name__)

# Load GeoJSON data
try:
    with open('seed/denver_neighborhoods.geojson') as f:
        geojson_data = json.load(f)
except FileNotFoundError as e:
    print(f"Error: {e}")
    geojson_data = None

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
```

Here, we are loading the GeoJSON data and handling the case where the file might not be found. If the file is not found, `geojson_data` is set to `None` and an error message is printed.

**Note:** In a future section, we will migrate to dynamically pull this data from an API based on the `location.city`, a property that will be added in a migration.

#### 2. Create the `/locations/average` Endpoint Function

Next, we will create the function for our endpoint that will handle the request and return the data.

```python
# server.py

from flask import Flask, jsonify
import json
from db_utils import execute_query

app = Flask(__name__)

# Load GeoJSON data
try:
    with open('seed/denver_neighborhoods.geojson') as f:
        geojson_data = json.load(f)
except FileNotFoundError as e:
    print(f"Error: {e}")
    geojson_data = None

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/locations/average', methods=['GET'])
def get_average_ratings():
    """
    Endpoint to get average review scores and average prices for neighborhoods.
    """
    if geojson_data is None:
        return jsonify({"error": "GeoJSON data not found"}), 500

    get_average_ratings_query = """
    SELECT
        loc.neighborhood_name,
        loc.longitude,
        loc.latitude,
        AVG(l.average_ratings) AS average_rating,
        AVG(CASE WHEN NOT l.price IS NULL AND NOT l.price = 'NaN' THEN l.price END) AS average_price
    FROM
        listings l
    JOIN
        locations loc
    ON
        l.location_id = loc.location_id
    GROUP BY
        loc.neighborhood_name,
        loc.longitude,
        loc.latitude
    ORDER BY
        loc.neighborhood_name;
    """

    try:
        # Execute the query
        results = execute_query(get_average_ratings_query)

        location_data = []

        for row in results:
            location_data.append({
                "neighborhood_name": row['neighborhood_name'],
                "average_rating": row['average_rating'],
                "average_price": row['average_price']
            })

        return jsonify({"data": location_data, "geojson": geojson_data})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

This code defines the function for the `/locations/average` endpoint. It starts by checking if the GeoJSON data is loaded, sets up the SQL query to get the average ratings and prices, executes the query, processes the results, and integrates them with the GeoJSON data.

---

**_NOTE:_** - Notice how that for average_price, we are using a `CASE` statement to handle `NULL` and `'NaN'` values. This is to ensure that we only calculate the average price for valid values. When reviewing the data for this section, I noticed that in some cases, the price was set to `'NaN'` instead of `NULL`. This is a common issue when dealing with data and it is important to handle such cases to avoid errors in calculations. We will come back and clean this data in a future section.

---

#### 3. Add Explanatory Comments and Error Handling

We will now add comments to explain each part of the code and handle potential errors.

```python
# server.py

from flask import Flask, jsonify
import json
from db_utils import execute_query

app = Flask(__name__)

# Load GeoJSON data
try:
    with open('seed/denver_neighborhoods.geojson') as f:
        geojson_data = json.load(f)
except FileNotFoundError as e:
    print(f"Error: {e}")
    geojson_data = None

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/locations/average', methods=['GET'])
def get_average_ratings():
    """
    Endpoint to get average review scores and average prices for neighborhoods.
    """
    if geojson_data is None:
        return jsonify({"error": "GeoJSON data not found"}), 500

    # SQL query to get average rating and price per neighborhood
    get_average_ratings_query = """
    SELECT
        loc.neighborhood_name,
        loc.longitude,
        loc.latitude,
        AVG(l.average_ratings) AS average_rating,
        AVG(CASE WHEN NOT l.price IS NULL AND NOT l.price = 'NaN' THEN l.price END) AS average_price
    FROM
        listings l
    JOIN
        locations loc
    ON
        l.location_id = loc.location_id
    GROUP BY
        loc.neighborhood_name,
        loc.longitude,
        loc.latitude
    ORDER BY
        loc.neighborhood_name;
    """

    try:
        # Execute the query
        results = execute_query(get_average_ratings_query)

        # Process the query results
        location_data = []
        for row in results:
            location_data.append({
                "neighborhood_name": row['neighborhood_name'],
                "average_rating": row['average_rating'],
                "average_price": row['average_price'],
                "longitude": row['longitude'],
                "latitude": row['latitude']
            })

        # Return the data along with the GeoJSON
        return jsonify({"data": location_data, "geojson": geojson_data})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

This code includes detailed comments explaining each part of the function, handles potential errors during the query execution, and processes the query results.

#### 4. Test the Endpoint

Run the Flask application:

```bash
python server.py
```

Open your web browser and navigate to [http://127.0.0.1:5000/locations/average](http://127.0.0.1:5000/locations/average). You should see the GeoJSON data with the average review scores and prices included.

### Summary

In this step, you have:

- Updated the Flask application to load GeoJSON data and handle potential errors.
- Created a function for the `/locations/average` endpoint.
- Executed a SQL query to get average review scores and prices.
- Processed the query results and integrated them with GeoJSON data.
- Set up the Flask application to run correctly.

This completes the process of creating a Flask API endpoint to query and return data from PostgreSQL. In the next step, we will create a Dash application to visualize this data.
