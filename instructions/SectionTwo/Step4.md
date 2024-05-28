# Section Two: Data Processing

## Table of Contents

- [Step 4: Load Data into PostgreSQL](#step-4-load-data-into-postgresql)
- [Goals](#goals)
- [Prerequisites](#prerequisites)
- [Step-by-Step Instructions](#step-by-step-instructions)
  - [1. Set Up Environment Variables and .env File](#1-set-up-environment-variables-and-env-file)
  - [2. Write Reusable Database Utility Functions](#2-write-reusable-database-utility-functions)
  - [3. Process and Load Data Using Jupyter Notebook](#3-process-and-load-data-using-jupyter-notebook)
  - [4. Verify Data in TablePlus](#4-verify-data-in-tableplus)
- [Summary](#summary)

## Step 4: Load Data into PostgreSQL

In this step, we will load the data from `seed/initial_data_airbnb.csv` and `seed/denver_neighborhoods.geojson` into a PostgreSQL database. This involves writing utility functions for database operations, setting up environment variables, and using Jupyter notebooks to process and load the data.

### Goals

- Write reusable utility functions for database connections and queries.
- Set up environment variables to manage database credentials securely.
- Process and load data from CSV and GeoJSON files into PostgreSQL using pandas in a Jupyter notebook.

### Prerequisites

Ensure you have the PostgreSQL container running in Docker. You can check the status of the container using the following command:

```bash
docker ps
```

If the container is not running, start it using Docker Compose:

```bash
docker-compose up -d
```

You also want to have TablePlus for an easier way to view the data in the PostgreSQL database.

- [TablePlus Installation](https://tableplus.com/)

### Step-by-Step Instructions

#### 1. Set Up Environment Variables and .env File

First, create a `.env` file in your project directory to store your database credentials securely. Add the following lines to the `.env` file:

```ini
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

The database credentials should match the values you used when setting up the PostgreSQL container. You can find them in the `docker-compose.yml` file.

This file contains sensitive information and should not be shared. It allows us to keep our credentials secure and separate from our code. To do this, we will create a `.gitignore` file to exclude the `.env` file from version control. To create the `.gitignore` file, run the following command:

```bash
echo ".env" > .gitignore
```

This command creates a `.gitignore` file with the `.env` file as the only entry. This ensures that the `.env` file is not included in the Git repository.

Now that we are saving our database credentials in our `.env`, we need to have `docker-compose.yml` use these credentials. Update the `docker-compose.yml` file to use the environment variables:

```yml
version: "3.1"

services:
  db:
    image: postgres:latest
    restart: always
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    ports:
      - "${DB_PORT}:5432"
    volumes:
      - db_data:/var/lib/postgresql/data
```

You will need to restart the PostgreSQL container for the changes to take effect:

```bash
docker-compose down
docker-compose up -d
```

Now, the PostgreSQL container will use the environment variables from the `.env` file to set up the database, allowing you to set your credentials securely without them being exposed in your code.

#### 2. Write Reusable Database Utility Functions

Create a new Python script named `db_utils.py` in your project directory. This script will contain utility functions for connecting to the PostgreSQL database and executing queries.

```python
# db_utils.py

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_db_connection():
    """
    Establishes a connection to the PostgreSQL database using credentials from the .env file.
    Returns the connection object if successful, otherwise raises an exception.
    """
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        return conn
    except psycopg2.DatabaseError as e:
        print(f"Error connecting to the database: {e}")
        raise

def execute_query(query, data=None):
    """
    Executes a SQL query using the provided connection.
    If the query is a SELECT statement, it fetches and returns the results.
    """
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, data)
            if cursor.description:
                result = cursor.fetchall()
            else:
                result = None
            conn.commit()
        return result
    except psycopg2.DatabaseError as e:
        print(f"Error executing query: {e}")
        raise
    finally:
        conn.close()

def execute_batch_query(query, data):
    """
    Executes a batch SQL query using the provided connection. Uses the execute_batch method from psycopg2 instead of
    executing each query in the batch individually.
    """
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            execute_batch(cursor, query, data)
            conn.commit()
    except psycopg2.DatabaseError as e:
        print(f"Error executing batch query: {e}")
        raise
    finally:
        conn.close()
```

This script includes functions to connect to the database and execute queries. The `get_db_connection` function establishes a connection using credentials from the `.env` file, while the `execute_query` function runs SQL queries and handles errors, and the `execute_batch_query` function executes batch SQL queries using the `execute_batch` method from `psycopg2`.

---

**_NOTE_**- This is a lot of code to digest at once, but most database libraries (like pyscorpg2) have `broilerplate` like this that you can copy and paste for your utility functions.

---

#### 3. Process and Load Data Using Jupyter Notebook

Create a new Jupyter notebook named `load_data.ipynb` in your project directory. The first thing we want to do is install `requirements.txt` in our notebook's first cell.

```python
!pip install -r requirements.txt
```

---

**_NOTE_** - Since this is the first time we are using a notebook, we will need to select a kernel. Select the `venv` kernel that you created earlier, which should be listed as an option in the Jupyter notebook interface. VS Code may prompt you to install `ipykernel` if it is not already installed. If you encounter any issues, refer to the instructions in the previous steps to create a virtual environment and install the required packages.

---

Once we have our packages installed, we can import the necessary libraries and the utility functions we created earlier.

```python
# notebooks/load_data.ipynb

import pandas as pd
from db_utils import execute_query, execute_batch_query


# Load the CSV file into a DataFrame
csv_file = 'seed/initial_data_airbnb.csv'
df_listings = pd.read_csv(csv_file)

# Display the first few rows of the DataFrame
df_listings.head()
```

Next, restructure the data into separate DataFrames for `locations`, `hosts`, and `listings`.

```python
# Rename location to neighborhood_name
df_listings = df_listings.rename(columns={'location': 'neighborhood_name'})


# Extract unique locations
df_locations = df_listings[['neighborhood_name', 'latitude',
                            'longitude']].drop_duplicates().reset_index(drop=True)
df_locations['location_id'] = df_locations.index + 1

# Extract unique hosts
df_hosts = df_listings[['host_id', 'host_since',
                        'host_is_superhost']].drop_duplicates().reset_index(drop=True)


# Cleanup: `Rating Category`` should be rating_category
df_listings = df_listings.rename(
    columns={'Rating category': 'rating_category'})

# On df_listings, add foreign key for location_id based off of neighborhood_name
df_listings = pd.merge(df_listings, df_locations[['neighborhood_name', 'location_id']],
                       on='neighborhood_name', how='left')

# Change id to listing_id for clarity and consistency
df_listings = df_listings.rename(columns={'id': 'listing_id'})

# Data normalization:  column \"first_review\" is of type date but expression is of type double precision\
df_listings['first_review'] = pd.to_datetime(df_listings['first_review'])
df_listings['last_review'] = pd.to_datetime(df_listings['last_review'])

# Replace NaT with None
df_listings['first_review'] = df_listings['first_review'].replace({
                                                                  pd.NaT: None})
df_listings['last_review'] = df_listings['last_review'].replace({pd.NaT: None})
```

---

**_NOTE_** - In this section, we had to rename columns, extract unique locations and hosts, merge the location foreign key into the listings DataFrame, and normalize the date columns. We also replaced `NaT` values with `None` to ensure consistency in the data. This was a process of trial and error during development of this tutorial to normalize the data and ensure that it is ready for loading into the database, which for now while you are copying and pasting the code, is a process you will need to go through in the future.

---

Now, create SQL tables and insert the processed data.

```python
# SQL queries to create tables
create_locations_table = """
CREATE TABLE IF NOT EXISTS locations (
    location_id SERIAL PRIMARY KEY,
    neighborhood_name TEXT,
    latitude FLOAT,
    longitude FLOAT
);
"""

create_hosts_table = """
CREATE TABLE IF NOT EXISTS hosts (
    host_id BIGINT PRIMARY KEY,
    host_since DATE,
    host_is_superhost BOOLEAN
);
"""

create_listings_table = """
CREATE TABLE IF NOT EXISTS listings (
    listing_id BIGINT PRIMARY KEY,
    host_id BIGINT REFERENCES hosts(host_id),
    location_id INT REFERENCES locations(location_id),
    property_type TEXT,
    room_type TEXT,
    guest_count INT,
    bathrooms FLOAT,
    beds FLOAT,
    price FLOAT,
    minimum_nights INT,
    maximum_nights INT,
    availability_30 INT,
    availability_60 INT,
    availability_90 INT,
    availability_365 INT,
    number_of_reviews INT,
    number_of_reviews_ltm INT,
    number_of_reviews_l30d INT,
    first_review DATE,
    last_review DATE,
    review_scores_rating FLOAT,
    review_scores_accuracy FLOAT,
    review_scores_cleanliness FLOAT,
    review_scores_checkin FLOAT,
    review_scores_communication FLOAT,
    review_scores_location FLOAT,
    review_scores_value FLOAT,
    instant_bookable BOOLEAN,
    reviews_per_month FLOAT,
    entire_home_apt BOOLEAN,
    rating_category TEXT,
    average_ratings FLOAT
);
"""

# Execute the queries
execute_query(create_locations_table)
execute_query(create_hosts_table)
execute_query(create_listings_table)
```

Finally, insert the data into the corresponding tables.

```python
# Insert data into locations table
location_data = []
for _, row in df_locations.iterrows():
  location_data.append((row['location_id'], row['neighborhood_name'], row['latitude'], row['longitude'], row['neighborhood_name']))

insert_location = """
INSERT INTO locations (location_id, neighborhood_name, latitude, longitude)
SELECT %s, %s, %s, %s
WHERE NOT EXISTS (
  SELECT 1 FROM locations WHERE neighborhood_name = %s
);
"""
execute_batch_query(insert_location, location_data)

# Insert data into hosts table
host_data = []
for _, row in df_hosts.iterrows():
  host_data.append((row['host_id'], row['host_since'], row['host_is_superhost']))

insert_host = """
INSERT INTO hosts (host_id, host_since, host_is_superhost)
VALUES (%s, %s, %s)
ON CONFLICT (host_id) DO NOTHING;
"""
execute_batch_query(insert_host, host_data)

# Insert data into listings table
listing_data = []
for _, row in df_listings.iterrows():
  listing_data.append((
    row['listing_id'], row['host_id'], row['location_id'], row['property_type'], row['room_type'], row['guest_count'],
    row['bathrooms'], row['beds'], row['price'], row['minimum_nights'], row['maximum_nights'], row['availability_30'],
    row['availability_60'], row['availability_90'], row['availability_365'], row['number_of_reviews'],
    row['number_of_reviews_ltm'], row['number_of_reviews_l30d'], row['first_review'], row['last_review'],
    row['review_scores_rating'], row['review_scores_accuracy'], row['review_scores_cleanliness'],
    row['review_scores_checkin'], row['review_scores_communication'], row['review_scores_location'],
    row['review_scores_value'], row['instant_bookable'], row['reviews_per_month'], row['entire_home_apt'],
    row['rating_category'], row['average_ratings']
  ))

insert_listing = """
INSERT INTO listings (
  listing_id, host_id, location_id, property_type, room_type, guest_count,
  bathrooms, beds, price, minimum_nights, maximum_nights, availability_30,
  availability_60, availability_90, availability_365, number_of_reviews,
  number_of_reviews_ltm, number_of_reviews_l30d, first_review, last_review,
  review_scores_rating, review_scores_accuracy, review_scores_cleanliness,
  review_scores_checkin, review_scores_communication, review_scores_location,
  review_scores_value, instant_bookable, reviews_per_month, entire_home_apt,
  rating_category, average_ratings
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (listing_id) DO NOTHING;
"""

execute_batch_query(insert_listing, listing_data)
```

For each table we are looping through the dataframe, using our insert SQL statement to add each item, and passing the values as separate arguments to the `execute_query` function. The reason we are passing the values as separate arguments is to prevent SQL injection attacks. This is a good practice to follow when executing queries with user input, and is common in most database libraries.

---

**_NOTE_** - Be sure to pay attention to what method you are using (execute_query or execute_batch_query) and what arguments you are passing to the function. The `execute_query` function is used for single queries, while the `execute_batch_query` function is used for batch queries. Passing the wrong arguments to the wrong function can cause errors in your code.

**_DEV_NOTE_** - I actually spent a few hours rewriting this part, as I was initially inserting each row individually, which took about 90 minutes to run by doing each transaction individually. By changing the way we are inserting the data, we can insert all the data in one transaction, which is much faster. Using the `execute_batch_query` function, we can insert all the data in one transaction, which is much faster than inserting each row individually. This is a good example of how to optimize your code for performance. It should take you less than a few minutes to seed your database using the above SQL, which is a significant improvement over the initial implementation. Remembering that in a production environment, you may be dealing with millions of rows of data, so optimizing your code is important. Transactions cost time and resources, so the fewer transactions you can make, the better. A small change like this one can literally save a company millions of dollars in server costs over the course of the apps lifetime, so always be thinking about how you can optimize your code.

---

#### 4. Verify Data in TablePlus

To verify that the data has been successfully loaded into the PostgreSQL database, you can use a database management tool like TablePlus. Connect to the database using the credentials from the `.env` file and check the tables to ensure that the data has been inserted correctly.

You can connect using a URI like this:

```ini
postgresql://{your_username}:{your_password}@localhost/airbnb_db?statusColor=686B6F&env=local&name=local_airbnb&tLSMode=0&usePrivateKey=false&safeModeLevel=0&advancedSafeModeLevel=0&driverVersion=0&lazyload=true
```

### Summary

In this step, you have:

- Set up environment variables to manage database credentials securely.
- Written reusable utility functions for database operations.
- Processed and loaded data from CSV and GeoJSON files into PostgreSQL using pandas in a Jupyter notebook.

The loading of data into SQL now allows us to much more efficiently query and analyze the data. The runtime efficiency of SQL databases is much higher than that of CSV files, and the ability to join tables and perform complex queries will be beneficial as we build out our Flask API and Dash dashboard. As you have seen from the seed phase, the data is not always in the format you need, and you may need to clean and normalize the data before loading it into the database. This causes major time delays in interacting with the data, so our efforts are important to ensure that subsequent reads have a high efficency. This is a common practice in data engineering and data science, and is an important step in the data processing pipeline.

This completes the process of loading data into PostgreSQL. In the next step, we will create Flask endpoints to access this data.
