# Section One: Initial Setup

## Table of Contents

- [Goals](#goals)
- [Educational Objectives](#educational-objectives)
- [What is a Server, and Why Are We Building It?](#what-is-a-server-and-why-are-we-building-it)
  - [The Basics](#the-basics)
  - [Front End vs Back End](#front-end-vs-back-end)
- [Why Aren't We Just Using CSV Files, and Why Do We Need a Database?](#why-arent-we-just-using-csv-files-and-why-do-we-need-a-database)
  - [CSV vs SQL](#csv-vs-sql)
  - [Is This Necessary?](#is-this-necessary)
- [Setting Up Your Environment](#setting-up-your-environment)
  - [Notebooks vs Scripts](#notebooks-vs-scripts)
  - [Anaconda vs Venv / Pip / Python](#anaconda-vs-venv--pip--python)
- [Why Docker?](#why-docker)
- [Dash and Plotly](#dash-and-plotly)

## Goals

This section aims to set up the infrastructure by establishing a database, dashboard, and server, ensuring they communicate effectively. We are not populating the database with data or creating visualizations yet. Use this time to get familiar with the project structure and the tools we are using, and make sure everything is working. Once you build it once, you can build it again, setting yourself up for success during the bootstrap phase rather than fixing issues later on.

## Educational Objectives

By the end of this section, you should be able to:

- Understand how to create a Flask server.
- Understand how to create a PostgreSQL database using Docker.
- Understand the basic structure of a Dash app.

Let's start by exploring some foundational concepts.

## What is a Server, and Why Are We Building It?

### The Basics

Data exploration and analysis typically occur within your computer using tools like Jupyter notebooks. However, to share your work with others, you need a server that can host your work and allow others to interact with it. We see client-server interactions in the real world all the time—from websites to mobile apps to video games.

We want to separate the data processing from the data visualization. This allows us to scale each part of the application independently, improve security, speed up the application, and make it easier to maintain and update.

### Front End vs Back End

This practice is often referred to as "front end" and "back end" programming. Familiarize yourself with these terms, as they will be used throughout the project.

For example, Facebook separates its various features (e.g., messaging, payments, marketplace) into different parts. When you use the Messenger app, the front end interacts with a back end server that stores all the messages. This separation allows for efficient management and scaling of each feature independently.

The takeaway here is that for our project, we want our dashboard to take dynamic variables, so that if data on the server changes, the dashboard will update automatically. This is the power of a client-server relationship.

## Why Aren't We Just Using CSV Files, and Why Do We Need a Database?

### CSV vs SQL

CSV files are great for small datasets but become harder to manage as data grows. Databases are designed to handle large amounts of data, optimized for quick reading and writing, and come with built-in security features.

We will use a PostgreSQL database for this project. PostgreSQL is a powerful, open-source database widely used in the industry. It is easy to set up, use, and offers numerous features that make it a good choice for this project.

### Is This Necessary?

For our small dataset, a CSV file would suffice. However, scaling to larger datasets and adding features like search would be difficult and slow with a CSV file. Databases facilitate better data management, version control, and scalability.

Early exposure to database concepts will make you a better programmer. While much of the setup work is typically handled by software or data engineers, understanding these concepts improves team communication and project understanding.

## Setting Up Your Environment

### Notebooks vs Scripts

Notebooks are ideal for exploratory analysis and sharing work with others due to their linear workflow. Scripts, on the other hand, are more flexible, easier to debug and test, and better suited for building dynamic applications. In VS Code, a script file would be `file.py`, while a notebook would be `file.ipynb`.

### Anaconda vs Venv / Pip / Python

Anaconda is popular in the data science community for managing Python environments, coming with many pre-installed packages. However, it can be slow and challenging to manage multiple environments.

Venv / Pip / Python is the standard way to manage Python environments in software development. It's fast, easy to manage, and recommended for this project. However, you can use Anaconda if you prefer. The code will run the same, but the way you manage packages and run the code will differ.

## Why Docker?

Docker allows you to run a container that operates the same way on any machine, regardless of the operating system or hardware. For this section, we will use Docker to start a PostgreSQL database. Think of Docker as a way to programmatically start a database without installing it directly on your machine.

We will use TablePlus to view and edit the database like a spreadsheet and use Python to interact with the database and run queries with the `psycopg2` package.

## Dash and Plotly

Our front end will use Plotly and Dash. Plotly is a powerful graphing library for creating a variety of charts, while Dash is a web application framework that enables interactive web applications with Python. Together, they allow us to create a dynamic dashboard that updates in real time as data changes, handling the complex parts of the client-server relationship.

Plotly can be used in Jupyter Notebooks, but Dash requires a server to run, which is why we need to create a Flask server to host the Dash app.

## Summary

In this section, we are laying the groundwork for our project by setting up the necessary infrastructure. Here’s what we’re doing in simple terms:

1. **Building a Server**: We need a server to host our work so others can interact with it. This involves creating a Flask server.
2. **Setting Up a Database**: Instead of using simple CSV files, we’re using a PostgreSQL database to handle larger datasets more efficiently and securely. We'll use Docker to easily manage this database.
3. **Creating a Dashboard**: We’ll set up the basic structure of a dashboard using Dash and Plotly, which will allow us to create interactive visualizations.

### What to Expect

- **Step-by-Step Guidance**: Each step will be clearly explained with examples and instructions. Don’t worry if you’re not familiar with these concepts yet; we’ll walk you through everything.
- **Learning the Basics**: By the end of this section, you’ll understand the basics of servers, databases, and dashboards. This foundational knowledge will be crucial as we build more features.
- **Practical Experience**: You’ll get hands-on experience with tools and technologies that are widely used in the industry, making you a more versatile and skilled professional.

### Reassurance

Remember, this is just the initial setup. We are not expecting you to master everything at once. Take your time to get comfortable with each step. There will be plenty of opportunities to practice and reinforce what you’ve learned as we progress through the project.

Feel free to revisit any section as needed, and don’t hesitate to ask questions or seek help if something is unclear. This is a learning journey, and every step you take brings you closer to becoming proficient in these essential skills.
