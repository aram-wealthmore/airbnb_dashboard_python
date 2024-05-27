# Section One: Initial Setup

## Step 2: Create a PostgreSQL Database

In this step, we will set up a PostgreSQL database using Docker. This database will store our AirBnB dataset, which will be accessed and processed by our Flask server and displayed on the Dash frontend.

### Goals

- Set up a PostgreSQL database using Docker.
- Verify that the database is running and accessible.

### Prerequisites

Ensure you have Docker Desktop installed on your machine:

- [Docker Installation](https://docs.docker.com/get-docker/)

### Step-by-Step Instructions

#### 1. Create a Docker Compose File

Create a file named `docker-compose.yml` in your project directory. This file will define the PostgreSQL service and its configuration.

```yml
version: "3.1"

services:
  db:
  image: postgres:latest
  restart: always
  environment:
    POSTGRES_USER: airbnb_user
    POSTGRES_PASSWORD: airbnb_password
    POSTGRES_DB: airbnb_db
  ports:
    - "5432:5432"
  volumes:
    - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

This Docker Compose file sets up a PostgreSQL container with the specified user, password, and database name. It also maps the default PostgreSQL port 5432 to your local machine.

#### 2. Start the PostgreSQL Database

Use Docker Compose to start the PostgreSQL database in your terminal. Since you are already running the Flask server from the previous step, you can open a new terminal window or tab to run the following command:

```bash
# Start the PostgreSQL database
docker-compose up -d
```

---

**_TIP_** - To open a new terminal window or tab in VS Code, press:

```
Ctrl + Shift + `
```

You will now see two terminal windows or tabs open in VS Code. Please reach out if you are having trouble at this step.

---

The `-d` flag runs the containers in the background. You can check the status of the containers using the following command:

```bash
docker-compose ps
```

You should see the PostgreSQL container listed and running.

#### 3. Verify the Database

To verify that the PostgreSQL database is running and accessible, you can use a database management tool like TablePlus, or the command line. Here, we'll use the command line.

First, install the `psql` command line tool if you haven't already:

```bash
# Install the PostgreSQL client
brew install postgresql
```

Confirm the installation by running:

```bash
psql --version
```

Then, connect to the database:

```bash
psql -h localhost -p 5432 -U airbnb_user -d airbnb_db
```

When prompted, enter the password `airbnb_password`. If everything is set up correctly, you should see the PostgreSQL prompt:

```
airbnb_db=>
```

You can now run SQL commands to interact with your database. For right now, you can exit the PostgreSQL prompt by typing:

```sql
\q
```

**_NOTE_** - To stop the PostgreSQL database, you can run the following command:

```bash
# Stop the PostgreSQL database
docker-compose down
```

This will stop and remove the PostgreSQL container.If you downloaded Docker Desktop, you will also be able to see the PostgreSQL container running in the Docker Desktop application, and control it from there.

### Summary

In this step, you have:

- Created a `docker-compose.yml` file to define the PostgreSQL service.
- Started the PostgreSQL database using Docker Compose.
- Verified that the database is running and accessible.

This setup ensures that you have a PostgreSQL database ready to store and manage your AirBnB data. In the next step, we will set up the Dash frontend to start building the user interface for our dashboard.
