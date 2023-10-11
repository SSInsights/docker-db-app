import json
from flask import Flask,request
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

app = Flask(__name__)
password = os.environ['POSTGRES_PASSWORD']

@app.route('/')
def hello_world():
    return 'Hello, Docker!'

# @app.route('/widgets')
# def get_widgets():
#     conn = psycopg2.connect(
#         host="db",
#         user="postgres",
#         password=password,
#         database="example"
#     )
#     cursor = conn.cursor()

#     cursor.execute("SELECT * FROM widgets")

#     row_headers=[x[0] for x in cursor.description]

#     results = cursor.fetchall()
#     json_data=[]
#     for result in results:
#         json_data.append(dict(zip(row_headers,result)))

#     cursor.close()
#     conn.close()

#     return json.dumps(json_data)

@app.route('/initdb')
def db_init():
    conn = psycopg2.connect(
        host="docker-db-app-db-1", 
        user="postgres",
        password=password,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = conn.cursor()

    cursor.execute("DROP DATABASE IF EXISTS example")
    cursor.execute("CREATE DATABASE example")

    cursor.close()
    conn.commit()
    conn.close()

    conn = psycopg2.connect(
    host="docker-db-app-db-1",
    user="postgres", 
    password=password,
    database="example"
    )
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS widgets")
    cursor.execute("CREATE TABLE example (name VARCHAR(255), description VARCHAR(255))")

    cursor.close()
    conn.commit()
    conn.close()

    return 'init database'



# New route to insert a single record into the "example" table
@app.route('/add_record', methods=['POST'])
def add_record():
    data = request.get_json()
    if 'name' not in data or 'description' not in data:
        return 'Invalid data format', 400

    conn = psycopg2.connect(
        host="db",
        user="postgres",
        password=password,
        database="example"
    )
    cursor = conn.cursor()

    insert_query = "INSERT INTO example (name, description) VALUES (%s, %s)"
    cursor.execute(insert_query, (data['name'], data['description']))

    conn.commit()
    cursor.close()
    conn.close()

    return 'Record added to the "example" table successfully', 201



# # Modify the existing route to insert a single record into the "example" table
# @app.route('/widgets', methods=['POST'])
# def add_widget():
#     data = request.get_json()
#     if 'name' not in data or 'description' not in data:
#         return 'Invalid data format', 400

#     conn = psycopg2.connect(
#         host="docker-db-app-db-1",
#         user="postgres",
#         password=password,
#         database="example"
#     )
#     cursor = conn.cursor()

#     insert_query = "INSERT INTO example (name, description) VALUES (%s, %s)"
#     cursor.execute(insert_query, (data['name'], data['description']))

#     conn.commit()
#     cursor.close()
#     conn.close()

#     return 'Record added to the "example" table successfully', 201


# CREATE ONE ENDPOINT to insert one record in table 

if __name__ == "__main__":
    app.run(host ='0.0.0.0')
