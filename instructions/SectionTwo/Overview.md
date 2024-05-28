# Section Two: Data Processing

## Table of Contents

- [Goals](#goals)
- [Educational Objectives](#educational-objectives)
- [Why PostgreSQL?](#why-postgresql)
  - [Relational Database Architecture](#relational-database-architecture)
  - [Foreign Keys and Scalability](#foreign-keys-and-scalability)
- [Loading Data into PostgreSQL](#loading-data-into-postgresql)
  - [GeoJSON and CSV Files](#geojson-and-csv-files)
  - [Breaking Down the Data](#breaking-down-the-data)
- [Reusable Database Functions](#reusable-database-functions)
  - [Database Connections in Python](#database-connections-in-python)
  - [Creating and Querying the Database](#creating-and-querying-the-database)
  - [Environment Variables and .env File](#environment-variables-and-env-file)
  - [Gitignore Practices for .env File](#gitignore-practices-for-env-file)
- [Using Jupyter Notebooks for Database Tasks](#using-jupyter-notebooks-for-database-tasks)
  - [Seeding the Database](#seeding-the-database)
  - [Handling Migrations](#handling-migrations)
- [Creating Flask Endpoints](#creating-flask-endpoints)
  - [What are endpoints, and how does a server work?](#what-are-endpoints-and-how-does-a-server-work)
  - [Accessing Data](#accessing-data)
  - [Returning JSON Responses](#returning-json-responses)
- [Creating the Average Review Map](#creating-the-average-review-map)
  - [Integrating Dash with Flask](#integrating-dash-with-flask)
  - [Visualizing Data](#visualizing-data)

## Goals

This section aims to build upon the initial setup by loading data into a PostgreSQL database, creating endpoints to access this data, and visualizing it using Dash. By the end of this section, you will have a functional backend that can serve data to the frontend for dynamic visualization.

### Step-by-Step Goals:

1. **Load Data into PostgreSQL**:
   - Convert and load data from `seed/initial_data_airbnb.csv` and `seed/denver_neighborhoods.geojson` into a PostgreSQL database.
   - Create a relational database schema that is both expandable and scalable.
2. **Create Flask Endpoints to Access Data**:

   - Set up Flask routes that query the PostgreSQL database.
   - Return the queried data in JSON format.

3. **Create Average Review Map in Dash**:
   - Connect our Front End to our Back End.
   - Visualize the average review scores on a map of Denver neighborhoods.

## Educational Objectives

By the end of this section, you should be able to:

- Understand the principles of relational database architecture.
- Load and query data in a PostgreSQL database.
- Create Flask endpoints to serve data.
- Integrate Dash with Flask for dynamic data visualization.

## Why PostgreSQL?

### Relational Database Architecture

PostgreSQL is a powerful, open-source relational database system that uses SQL (Structured Query Language) to manage data. Unlike flat-file databases like CSV, relational databases allow us to structure data into tables that can be linked using relationships. This approach offers several advantages:

- **Data Integrity**: Enforces data consistency through constraints and relationships.
- **Scalability**: Handles larger datasets more efficiently.
- **Complex Queries**: Supports advanced querying capabilities for more complex data retrieval.

### Foreign Keys and Scalability

Using foreign keys, we can link tables together, creating relationships between different datasets. This is crucial for scalability because it allows us to:

- **Normalize Data**: Reduce redundancy by storing related data in separate tables.
- **Expandability**: Easily add new data and relationships without restructuring the entire database.

For instance, in our AirBnB dataset, we will break down the data into three main tables: `locations`, `hosts`, and `listings`.

### Breaking Down the Data

#### 1. Locations Table

The `locations` table will store geographical data, helping us normalize location information and allowing for more efficient queries and data management.

- **Columns**:
  - `location_id` (primary key, integer)
  - `neighborhood_name` (text)
  - `latitude` (float)
  - `longitude` (float)

#### 2. Hosts Table

The `hosts` table will contain information about the hosts, separating host-specific data from the listings, which will help reduce redundancy.

- **Columns**:
  - `host_id` (primary key, integer)
  - `host_since` (date)
  - `host_is_superhost` (boolean)

#### 3. Listings Table

The `listings` table will contain the main data related to the properties, including review data, property details, and foreign keys linking to the `locations` and `hosts` tables.

- **Columns**:
  - `listing_id` (primary key, integer)
  - `host_id` (foreign key, integer)
  - `location_id` (foreign key, integer)
  - `property_type` (text)
  - `room_type` (text)
  - `guest_count` (integer)
  - `bathrooms` (float)
  - `beds` (float)
  - `price` (float)
  - `minimum_nights` (integer)
  - `maximum_nights` (integer)
  - `availability_30` (integer)
  - `availability_60` (integer)
  - `availability_90` (integer)
  - `availability_365` (integer)
  - `number_of_reviews` (integer)
  - `number_of_reviews_ltm` (integer)
  - `number_of_reviews_l30d` (integer)
  - `first_review` (date)
  - `last_review` (date)
  - `review_scores_rating` (float)
  - `review_scores_accuracy` (float)
  - `review_scores_cleanliness` (float)
  - `review_scores_checkin` (float)
  - `review_scores_communication` (float)
  - `review_scores_location` (float)
  - `review_scores_value` (float)
  - `instant_bookable` (boolean)
  - `reviews_per_month` (float)
  - `entire_home_apt` (boolean)
  - `rating_category` (text)
  - `average_ratings` (float)

## Reusable Database Functions

### Database Connections in Python

To manage our database connections efficiently, we will create utility functions in a Python script. These functions will handle connecting to the PostgreSQL database and executing queries. Our high level goal is to reduce the amount of repeated code and make our application more maintainable, and our low level goal is to create functions that ensure that each time we interact with the database, we do it the same way. This will help us avoid errors and make our code more readable, as well as centralize all security concerns in one place.

### Creating and Querying the Database

We will create Python functions for:

- **Connecting to the Database**: Establish a connection to the PostgreSQL server using connection parameters.
- **Executing Queries**: Execute SQL queries to create tables, insert data, and fetch results.

### Environment Variables and .env File

To keep our database credentials secure, we will store them in an `.env` file. This file will contain sensitive information like database name, user, password, and host. We will use the `python-dotenv` package to load these environment variables in our scripts.

### Gitignore Practices for .env File

To ensure that our `.env` file is not tracked by version control, we will add it to our `.gitignore` file. This prevents sensitive information from being exposed in the repository.

Add the following line to your `.gitignore` file:

    ```
    # Ignore environment variables file
    .env
    ```

## Using Jupyter Notebooks for Database Tasks

### Seeding the Database

We will use Jupyter notebooks to run one-off scripts for seeding the database. The notebooks will use the utility functions created earlier to load data from the CSV and GeoJSON files into the PostgreSQL database.

### Handling Migrations

In the future, we may need to make schema changes. Jupyter notebooks will also be used to handle database migrations, allowing us to update the schema and migrate data as needed.

---

**_NOTE_** - It is a wise practice to use some sort of migration tool to track any schema changes programatically. We will explore this in future sections, as we have established our three main tables and relationships above, and will not be making any schema changes in this section.

---

## Creating Flask Endpoints

### What are endpoints, and how does a server work?

An endpoint is a URL pattern that the server uses to route requests to the appropriate handler. When a client makes a request to the server, the server matches the URL pattern to the corresponding endpoint and executes the associated code.

Example: The endpoint `/locations?neighborhood=Capitol Hill` might return all listings in the Capitol Hill neighborhood. When a client talks to a server, this `address` tells the server what code to run, and what to respond with.

### Accessing Data

We will create Flask routes to access the data stored in PostgreSQL. These routes will perform SQL queries to retrieve data based on various parameters.

### Returning JSON Responses

Flask routes will return data in JSON format, making it easy for the frontend (Dash) to consume and display the data.

## Creating the Average Review Map

### Integrating Dash with Flask

We will integrate Dash with Flask to create a seamless flow of data from the database to the frontend. Dash will use the endpoints created in Flask to fetch data dynamically.

### Visualizing Data

Using Dash and Plotly, we will create a map that visualizes the average review scores of AirBnB listings across different neighborhoods in Denver. This will involve:

1. **Fetching Data**: Querying the PostgreSQL database via Flask endpoints.
2. **Processing Data**: Aggregating review scores by neighborhood.
3. **Displaying Data**: Plotting the data on an interactive map using Plotly.

### Reusable Graph Components

We will create reusable components for the map visualization, allowing us to update the data dynamically without rewriting the entire codebase. This modular approach will make our code more maintainable and scalable, and seperate the concerns of data processing and visualization.

## Summary

In this section, you will:

- Learn the importance of relational databases and how to structure them.
- Load and manage data in PostgreSQL.
- Create reusable database connection and query functions.
- Use environment variables to manage sensitive information.
- Utilize Jupyter notebooks for seeding and migrating the database.
- Create endpoints to serve data using Flask.
- Visualize data dynamically with Dash.
- Integrate Dash with Flask to create a functional backend and frontend.

These steps will significantly enhance your understanding of backend and frontend integration, setting the stage for more advanced features and data processing in subsequent sections. Stay focused on understanding each component's role and how they interact to form a cohesive and scalable application.
