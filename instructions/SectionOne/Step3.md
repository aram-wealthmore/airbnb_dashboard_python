# Section One: Initial Setup

## Table of Contents

- [Step 3: Hello World - Dash / Plotly Dashboard Bootstrap](#step-3-hello-world---dash--plotly-dashboard-bootstrap)
- [Goals](#goals)
- [Prerequisites](#prerequisites)
- [Step-by-Step Instructions](#step-by-step-instructions)
  - [1. Create the Dash Application](#1-create-the-dash-application)
  - [2. Add a Dummy Plotly Graph](#2-add-a-dummy-plotly-graph)
  - [3. Run the Dash Application](#3-run-the-dash-application)
  - [4. Verify the Dash Application](#4-verify-the-dash-application)
- [Summary](#summary)

## Step 3: Hello World - Dash / Plotly Dashboard Bootstrap

In this step, we will set up a basic Dash application to ensure that our front end is working correctly. This initial setup will help us verify that our environment is ready for building the interactive dashboard.

### Goals

- Create a basic Dash application.
- Verify that the Dash app runs correctly and can be accessed via a web browser.

### Prerequisites

Ensure you have the virtual environment activated. If not, select it in VS Code by:

1. Opening the command palette (Ctrl + Shift + P).
2. Typing `Python: Select Interpreter`.
3. Selecting the virtual environment you created.
   - If you don't see the virtual environment, create one by following the instructions in Step 1.

### Step-by-Step Instructions

#### 1. Create the Dash Application

Create a new file named `dashboard.py` in your project directory. This file will contain the code for our Dash application.

```python
# dashboard.py

from dash import Dash, html

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children='''
        Dash: A web application framework for Python.
    ''')
])

if __name__ == '__main__':
    app.run_server(debug=True)
```

This code sets up a basic Dash application that displays a simple "Hello Dash" message.

#### 2. Add a Dummy Plotly Graph

To make our Dash application more interesting, let's add a dummy Plotly graph.

First, import the necessary libraries:

```python
# dashboard.py

from dash import Dash, html, dcc #  NEW - Import dcc from dash
# NEW - Import Plotly Express and Pandas
import plotly.express as px
import pandas as pd
# END NEW
```

Next, create a simple DataFrame and a bar chart:

```python
# Create a simple DataFrame
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Grapes"],
    "Amount": [4, 1, 2, 5]
})

# Create a bar chart
fig = px.bar(df, x="Fruit", y="Amount", title="Dummy Fruit Data")
```

Finally, update the app layout to include the graph:

```python
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])
```

The updated `dashboard.py` should look like this:

```python
# dashboard.py

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# Create a simple DataFrame
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Grapes"],
    "Amount": [4, 1, 2, 5]
})

# Create a bar chart
fig = px.bar(df, x="Fruit", y="Amount", title="Dummy Fruit Data")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
```

This code adds a simple bar chart to the Dash application using Plotly.

#### 3. Run the Dash Application

Run the Dash application to ensure everything is working correctly.

```bash
python dashboard.py
```

If everything is set up correctly, you should see output indicating that the server is running:

```
    * Running on http://127.0.0.1:8050/ (Press CTRL+C to quit)
```

#### 4. Verify the Dash Application

Open your web browser and navigate to [`http://127.0.0.1:8050/`](http://127.0.0.1:8050/). You should see a web page with the message "Hello Dash" and a brief description underneath, along with the dummy bar chart.

### Summary

In this step, you have:

- Created a basic Dash application.
- Added a dummy Plotly graph to the application.
- Run the Dash application and verified that it works correctly.

This basic setup confirms that your environment is correctly configured and that you can proceed to more advanced steps, such as integrating the PostgreSQL database and creating more complex visualizations. If you encounter any issues, ensure that you have followed each step correctly and refer to the Dash documentation for additional troubleshooting.

In the next step, we will load data into the PostgreSQL database and start working on the backend to fetch and serve data to the Dash frontend.
