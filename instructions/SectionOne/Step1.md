# Section One: Initial Setup

## Table of Contents

## Table of Contents

- [Section One: Initial Setup](#section-one-initial-setup)
- [Goals](#goals)
- [Prerequisites](#prerequisites)
- [Step-by-Step Instructions](#step-by-step-instructions)
    - [1. Create the Project Directory](#1-create-the-project-directory)
    - [2. Set Up a Virtual Environment using VS Code](#2-set-up-a-virtual-environment-using-vs-code)
    - [3. (Optional) Install Required Packages](#3-optional-install-required-packages)
    - [4. Create the Flask Application](#4-create-the-flask-application)
    - [5. Run the Flask Server](#5-run-the-flask-server)
    - [6. Verify the Server](#6-verify-the-server)
- [Summary](#summary)

## Step 1: Hello World - Server Bootstrap

In this step, we will set up a basic Flask server to ensure everything is working correctly before we dive deeper into the project. This initial setup will lay the foundation for our AirBnB Dashboard by establishing a server that will later interact with our PostgreSQL database and Dash frontend.

### Goals

- Create a basic Flask server.
- Verify that the server runs correctly and can be accessed via a web browser.

### Prerequisites

Ensure you have the following installed and set up on your machine:

- Python 3.7 or higher
- Pip
- VS Code (or your preferred IDE)

### Step-by-Step Instructions

#### 1. Create the Project Directory

First, let's create a directory for our project if you haven't already done so.

    ```bash
    # Create the project directory
    mkdir airbnb_dashboard
    cd airbnb_dashboard
    ```

#### 2. Set Up a Virtual Environment using VS Code

Next, set up a virtual environment for your project. This will isolate your project's dependencies from other Python projects on your machine.

- Open the command palette in VS Code (Ctrl + Shift + P).
- Type `Python: Select Interpreter`.
- Select `Create New Virtual Environment`.
- Choose a location for the virtual environment (e.g., `.venv`).
- Select the Python version (3.7 or higher).
- (Optional) Select the `requirements` file to install the required packages.
  - This will only appear if you have added the `requirements.txt` file in your project directory, and prevents you from having to install the packages manually
- Select the virtual environment as the interpreter.

#### 3. (Optional) Install Required Packages

If you did not get the option to select the requirements file during the virtual environment setup, you can install the required packages manually by running the following command in the terminal:

```bash
touch requirements.txt
```

Copy and paste the packages from the README.md file into the `requirements.txt` that was created in the root of your project directory.

---

**_TIP_** - Once you have VS Code open, you can open a terminal that starts in the project directory by pressing:

```
Ctrl + `
```

---

Once the terminal is open, run the following command to install required packages:

```bash
pip install -r requirements.txt
```

#### 4. Create the Flask Application

Create a new file named `server.py` in your project directory. This file will contain the code for our Flask server.

```python
# server.py

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
```

This code sets up a basic Flask server that returns "Hello, World!" when you visit the root URL (`/`).

#### 5. Run the Flask Server

Run the Flask server to ensure everything is working correctly.

```bash
python server.py
```

If everything is set up correctly, you should see output indicating that the server is running:

```
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

#### 6. Verify the Server

Open your web browser and navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/). You should see the message "Hello, World!" displayed in your browser.

Congratulations! You have successfully set up a basic Flask server. You can close the server by pressing `Ctrl + C` in the terminal.

**_TIP_**: Unlike Jupyter notebooks, you now have a persistent server running in the background. If you make changes to your code, you will need to restart the server to see the changes reflected in your browser.

### Summary

In this step, you have:

- Created a project directory and set up a virtual environment.
- Installed Flask and created a basic Flask application.
- Run the Flask server and verified that it works correctly.

This basic setup confirms that your environment is correctly configured and that you can proceed to more advanced steps, such as setting up the PostgreSQL database and integrating the Dash frontend. If you encounter any issues, ensure that you have followed each step correctly and refer to the Flask documentation for additional troubleshooting.

In the next step, we will create a PostgreSQL database using Docker.
