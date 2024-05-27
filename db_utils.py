# db_utils.py

import os
import psycopg2
from psycopg2.extras import RealDictCursor, execute_batch
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
