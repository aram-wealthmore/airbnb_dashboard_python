# Section Two: Data Processing

## Table of Contents

- [Step 5: Create Flask Endpoints to Access Data](#step-5-create-flask-endpoints-to-access-data)
  - [Goals](#goals)
  - [Prerequisites](#prerequisites)
  - [Step-by-Step Instructions](#step-by-step-instructions)
    - [1. Update `server.py` to Load GeoJSON Data](#1-update-serverpy-to-load-geojson-data)
    - [2. Define the Route for `/locations/average`](#2-define-the-route-for-locationsaverage)
    - [3. Handle Missing GeoJSON Data](#3-handle-missing-geojson-data)
    - [4. Construct the SQL Query](#4-construct-the-sql-query)
    - [5. Execute the SQL Query and Process Results](#5-execute-the-sql-query-and-process-results)
    - [6. Return the Combined Data](#6-return-the-combined-data)
    - [7. Test the Endpoint](#7-test-the-endpoint)
  - [Summary](#summary)

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

app = Flask(__name__)

# Load GeoJSON data
try:
    with open('seed/denver_neighborhoods.geojson') as f:
        geojson_data = json.load(f)
except FileNotFoundError as e:
    print(f"Error loading geojson: {e}")
    geojson_data = None
```

For now since we only have one GeoJSON file, we will load it directly in the `server.py` script. In a future step, we will refactor this to load GeoJSON data dynamically based on the request, and attach it to the response accordingly.

We use a try-except block to handle the case where the GeoJSON file is not found, so if we run into this paticular error, we can debug accordingly. Having specific error handling in place will help us identify and resolve issues quickly.

#### 2. Define the Route for `/locations/average`

Next, we will define the route for our endpoint that will handle the request and return the data.

```python
# server.py

@app.route('/locations/average', methods=['GET'])
def get_average_ratings():
    """
    Endpoint to get average review scores and average prices for neighborhoods.
    """
    if geojson_data is None:
        return jsonify({"error": "GeoJSON data not found"}), 500
```

Remember in the initial step we set the route for "Hello World" to `/`, which means when you go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) you see the message "Hello, World!". Now we are setting up a new route for `/locations/average` that will return the average review scores and prices for neighborhoods at that URL. This is how servers know which code to run when a specific URL is visited, and how we organize our API endpoints.

#### 3. Handle Missing GeoJSON Data

We will ensure that if the GeoJSON data is not loaded, the endpoint returns an appropriate error response.

```python
# server.py

@app.route('/locations/average', methods=['GET'])
def get_average_ratings():
    """
    Endpoint to get average review scores and average prices for neighborhoods.
    """
    if geojson_data is None:
        return jsonify({"error": "GeoJSON data not found"}), 500

    # Proceed with the query if geojson_data is loaded
```

Same with as with the try except block earlier, we are handling the case where the GeoJSON data is not loaded. This way, we can identify the issue and resolve it quickly.

#### 4. Construct the SQL Query

We will construct the SQL query to get the average ratings and prices.

```python
# server.py

    # SQL Query to get average ratings and prices
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
```

This is broken down as follows:

- SELECT the neighborhood name, longitude, and latitude from the `locations` table, and the average review scores and prices from the `listings` table.
  - We use the `AVG()` function to calculate the average review scores and prices, a feature PostgreSQL provides to calculate the average of a set of values.
  - We use the `CASE` statement to handle the case where the price is `NULL` or `'NaN'`. Upon review of the data, we found `NaN` values in the `price` column. We want to exclude these values from the average calculation, so we can get a representative value for the neighborhood with the data we do have collected.
- JOIN the `listings` and `locations` tables on the `location_id` column.
- GROUP BY the neighborhood name, longitude, and latitude.
- ORDER BY the neighborhood name.

---

**_TIP_**- Using `TablePlus`, you can filter using the GUI and then check the SQL Preview to see the SQL query that is generated. This can be a helpful way to understand how to write compliacated queries using a UI then copy and pasting the SQL query into your code.

---

#### 5. Execute the SQL Query and Process Results

We will execute the query, process the results, and store them in a list.

```python
# server.py
    try:
        # Execute the query
        results = execute_query(get_average_ratings_query)

        # Process the results
        location_data = []

        for row in results:
            location_data.append({
                "neighbourhood": row['neighborhood_name'],  # Note: Our GeoJSON uses 'neighbourhood' instead of 'neighborhood_name', so for now we will accommodate this difference by returning 'neighbourhood' instead of 'neighborhood_name'.
                "average_rating": row['average_rating'],
                "average_price": row['average_price']
            })
        # Return the combined data
        return jsonify({"data": location_data, "geojson": geojson_data})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
```

#### 6. Return the Combined Data

In the above step, we use `jsonify` to return the combined data as a JSON response.

This is a standard practice for HTTP APIs, as it ensures that the data is returned in a format that can be easily consumed by clients. While we are using Python on our full stack, we could also use JavaScript, Java, or any other language to consume this data. By returning the data in JSON format, we can easily parse it and use it in any language.

#### 7. Test the Endpoint

Here is the final `server.py` script with all parts combined:

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

@app.route('/locations/average', methods=['GET'])
def get_average_ratings():
    """
    Endpoint to get average review scores and average prices for neighborhoods.
    """
    if geojson_data is None:
        return jsonify({"error": "GeoJSON data not found"}), 500

    # SQL Query to get average ratings and prices
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

        # Process the results
        location_data = []

        for row in results:
            location_data.append({
                "neighbourhood": row['neighborhood_name'],  # Note: Our GeoJSON uses 'neighbourhood' instead of 'neighborhood_name', so for now we will accommodate this difference by returning 'neighbourhood' instead of 'neighborhood_name'.
                "average_rating": row['average_rating'],
                "average_price": row['average_price']
            })

        # Return the combined data
        return jsonify({"data": location_data, "geojson": geojson_data})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

Run the Flask application

```bash
python server.py
```

Open your web browser and navigate to [http://127.0.0.1:5000/locations/average](http://127.0.0.1:5000/locations/average). You should see the GeoJSON data with the average review scores and prices included.

### Summary

In this step, you have:

- Updated the Flask application to load GeoJSON data and handle potential errors.
- Defined a route for the `/locations/average` endpoint.
- Constructed and executed a SQL query to get average review scores and prices.
- Processed the query results and integrated them with GeoJSON data.
- Set up the Flask application to run correctly.

This completes the process of creating a Flask API endpoint to query and return data from PostgreSQL. In the next step, we will create a Dash application to visualize this data.
