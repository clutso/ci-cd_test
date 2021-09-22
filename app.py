import mysql.connector
from flask import Flask
import os 
import json
from dotenv import load_dotenv

try:
    load_dotenv()
except: 
    pass

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Docker!'

@app.route('/widgets')
def get_widgets():
    mydb= mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )
    cursor= mydb.cursor()

    cursor.execute("SELECT * FROM widgets")
    #extract row headers
    row_headers=[x[0] for x in cursor.description]
    results = cursor.fetchall()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))

    cursor.close()
    return json.dumps(json_data)

@app.route('/initdb')
def db_init():
    mydb= mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )
    cursor= mydb.cursor()
    cursor.execute("DROP DATABASE IF EXISTS inventory")
    cursor.execute("CREATE DATABASE inventory")
    cursor.close()
    mydb= mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )
    cursor= mydb.cursor()
    cursor.execute("DROP TABLE IF EXISTS widgets")
    cursor.execute("CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255))")
    cursor.close()

    return 'DB ready'

if __name__=="__main__":
    app.run(host='0.0.0.0')    
