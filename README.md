# AirBnB Dashboard

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Repo Setup / Package Installation](#repo-setup--package-installation)
- [Steps](#steps)
  - [Section One: Initial Setup](#section-one-initial-setup)
  - [Section Two: Data Processing](#section-two-data-processing)
  - [Section Three: Additional Features](#section-three-additional-features)
- [Running this Project](#running-this-project)
- [Conclusion](#conclusion)
- [Additional Resources](#additional-resources)

## Introduction

In this project, we are building a dashboard from an already processed AirBnB dataset located in the folder `seed/initial_data_airbnb.csv`, and using map data from `seed/denver_neighborhoods.geojson`. The dataset contains information about the listings on the AirBnB platform. The dashboard will be built using the `dash` library in Python. This project will include the following features:

- Creating a PostgreSQL database to store the data instead of a CSV file
  - This database will be started and accessed using Docker
- Backend server using Flask to access the database programmatically
  - The server will be started using the command line
  - The server will be able to access the database and return the data in JSON format
- Frontend using Dash and Plotly to display the data in a dashboard
  - The frontend will be started using the command line and will be able to access the backend server
  - A map of Denver with the neighborhoods colored by the average review will be the primary feature.
  - TBD: Other features to be added

## Prerequisites

- Python 3.7 or higher
  - [Python Installation](https://www.python.org/downloads/)
- Pip
  - [Pip Installation](https://pip.pypa.io/en/stable/installation/)
- Docker Desktop
  - [Docker Installation](https://docs.docker.com/get-docker/)
- Docker Compose
  - [Docker Compose Installation](https://docs.docker.com/compose/install/)
- VS Code
  - [VS Code Installation](https://code.visualstudio.com/download)
- TablePlus
  - [TablePlus Installation](https://tableplus.com/)

## Repo Setup / Package Installation

For this project, each branch will provide an example of the code at a specific step in the tutorial. However, you will be building the project from scratch and will only be downloading the folder `/seed` to get the initial data.

1. Create a new repository on GitHub and clone it to your local machine.
   - Create a new repository on GitHub.
   - Clone the repository to your local machine:
     ```bash
     # Clone the repository
     git clone `github-repo-url`
     ```
   - Change the directory to the repository:
     ```bash
     # Change the directory
     cd `repository-name`
     ```
2. Download the `/seed` folder from the GitHub repository and place it in the root of your project.
   - Seed URL: [AirBnB Dashboard Seed](https://example.com) // TODO: Update with the correct link.
3. Create a virtual environment for the project.
   - Creating a virtual environment in VS Code:
     - Open the command palette (Ctrl + Shift + P).
     - Type `Python: Select Interpreter`.
     - Select `Create New Virtual Environment`.
     - Choose a location for the virtual environment.
     - Select the Python version (3.7 or higher).
     - Select the virtual environment as the interpreter.
4. Create a `requirements.txt` file in the root of the project.
   - Run the following command in the terminal:
     ```bash
     # Create a requirements.txt file
     pip freeze > requirements.txt
     ```
   - Add the following packages to the `requirements.txt` file:
     ```txt
     dash
     flask
     psycopg2
     pandas
     geopandas
     geojson
     ```
5. Install the required packages from the `requirements.txt` file.
   - Run the following command in the terminal:
     ```bash
     # Install from requirements.txt
     pip install -r requirements.txt
     ```
   - By saving all of your package requirements in a `requirements.txt` file, you can easily install all of the packages in a new environment by running the command above, and allow others to install the same packages in their environment. This will ensure that everyone is using the same versions of the packages and that the project will run correctly.

## Steps

Follow the steps in the `instructions` folder in order to build the project from scratch. Each step will build on the previous step and will provide a new feature or functionality to the project. If you get stuck, you can refer to the branches in the repository to see the code at each step.

### Section One: Initial Setup

1. Step 1: Hello World - Server Bootstrap.
   - Branch: `step_1_hello_world_bootstrap`
2. Step 2: Create a PostgreSQL database.
   - Branch: `step_2_create_postgres_database`
3. Step 3: Hello World - Dash / Plotly Dashboard Bootstrap.
   - Branch: `step_3_hello_world_dash_plotly_dashboard_bootstrap`

### Section Two: Data Processing

4. Step 4: Load Data into PostgreSQL.
   - Branch: `step_4_load_data_into_postgres`
5. Step 5: Create Flask Endpoints to Access Data.
   - Branch: `step_5_create_flask_endpoints`
6. Step 6: Create Average Review Map in Dash.
   - Branch: `step_6_create_average_review_map`

### Section Three: Additional Features

7. Step 7: TBD.
   - Branch: `step_7_tbd`

## Running this Project

To test the project, you will need to run the following commands in the terminal:

```bash
# Start the PostgreSQL database
docker-compose up -d

# Start the Flask server
python server.py

# Start the Dash app
python app.py
```

Once the commands have been run, you can access the dashboard by going to `http://localhost:8050/` in your web browser. If you see the dashboard, then the project is working correctly and you have the proper prerequisites installed to build this on your own. If you are having trouble, please refer to the branches in the repository to see the code at each step.

## Conclusion

In this project, you will have learned how to build a front end, back end, and how to host and manage a PostgreSQL database using Docker. You will have built a dashboard that allows the end user to interact with the data and visualize it in a meaningful way rather than relying on an analyst to provide the information. This project will provide you with the skills to build a full-stack application using Python and Docker, and have abstracted the data processing and visualization to a point where you can easily add new features and data sources, and deploy each part of the application to a cloud service independently, allowing them to scale as needed based on the demand.

## Additional Resources

- [Dash Documentation](https://dash.plotly.com/)
- [Plotly Documentation](https://plotly.com/python/)
- [Flask Documentation](https://flask.palletsprojects.com/en/2.0.x/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [VS Code Documentation](https://code.visualstudio.com/docs)
