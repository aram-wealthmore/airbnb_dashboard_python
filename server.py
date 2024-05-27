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
        AVG(l.review_scores_rating) AS average_rating,
        AVG(l.price) AS average_price
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
                "average_price": row['average_price'],
                "longitude": row['longitude'],
                "latitude": row['latitude']
            })

        return jsonify({"data": location_data, "geojson": geojson_data})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
