import pandas as pd
import psycopg2
from flask import Flask, request
import os
import configparser
import requests
import json

app = Flask(__name__)

config = configparser.ConfigParser()

config.read('.env')

# .env files names should not be in '' and no , after each name

DB_HOST = config['CONNECTION']['host']
DB_PASSWORD = config['CONNECTION']['password']
DB_PORT = config['CONNECTION']['port']
DB_USERNAME = config['CONNECTION']['user']
DB_DATABASE = config['CONNECTION']['database']


def database_connector():
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USERNAME, password=DB_PASSWORD, database=DB_DATABASE)
    print('Connected to postgress DB')
    return conn


@app.route('/fetchAllArtists', methods=['GET'])
def allArtists():
    conn = database_connector()
    cursor = conn.cursor()
    select_query = """select * from celebrity"""
    celeb_df = pd.read_sql(select_query, con=conn)
    celeb_df.to_csv('celeb.csv')
    celeb_json = celeb_df.to_json(orient='records')
    celeb_df.to_json('test.json')
    conn.commit()
    cursor.close()
    conn.close()
    return celeb_json


@app.route('/fetchHome', methods=['GET'])
def read_artists():
    connection = database_connector()
    cursor = connection.cursor()
    select = """select celebrity_name, genre from celebrity"""
    celeb_df = pd.read_sql(select, con=connection)
    # celeb_df.to_json(
    #     '/Users/adeleke/Documents/simple_api_postgress/celeb.json') --to json file
    celeb_json = celeb_df.to_json(orient="index")
    connection.commit()
    cursor.close()
    connection.close()

    return celeb_json


@app.route('/fetchHome/select', methods=['GET'])
def fetchSelect():
    conn = database_connector()
    cursor = conn.cursor()
    query = """select music_id, music_name from music"""
    query_df = pd.read_sql(query, con=conn)
    query_json = query_df.to_json(orient="index")
    conn.commit()
    cursor.close()
    conn.close()
    return query_json


@app.route('/fetchHome/<int:item_d>', methods=['GET'])
def fetchRows(item_d):
    connection = database_connector()
    cursor = connection.cursor()
    select_sql = """select * from celebrity
    where id = {}
    """
    row_df = pd.read_sql(select_sql.format(item_d), con=connection)
    # if you are not using api, you can simply just pass this to file as above
    row_json = row_df.to_json(orient="index")

    # row_json = row_df.to_json(orient='records')
    connection.commit()
    cursor.close()
    connection.close()
    print('row data returned by id')
    return row_json
    # return row_json


@app.route('/postCelebrity', methods=['POST'])
def insertCelebrity():
    connection = database_connector()
    cursor = connection.cursor()
    insert_sql = """
    insert into celebrity(celebrity_name, genre, num_albums, id )
    values (%s, %s, %s, %s)
    """
    cursor.execute(insert_sql, ('Chioma', 'oyes_music', 10, 15))
    connection.commit()
    cursor.close()
    connection.close()
    return 'Celebrity information posted'


# json load - takes a json file and load as json obj


@app.route('/loadJsonFile', methods=['GET'])
def loadJsonFile():
    f = open('celeb.json', )
    celebrity_data = json.load(f)
    f.close()
    return celebrity_data

# first you open the file, load it and then close the file

# json dump into a file

# we returned a celeb_json as our api response and we dump the json as a file in myfile.json


@app.route('/fetchHomeDump', methods=['GET'])
def read_artistsDump():
    connection = database_connector()
    cursor = connection.cursor()
    select = """select celebrity_name, genre from celebrity"""
    celeb_df = pd.read_sql(select, con=connection)
    # Just trying out if we are not converting to df and then we want to dump to json file
    # Celeb_df.to_json(and passing the file path in quote) will give us the json file here
    celeb_json = celeb_df.to_json(orient="index")
    out_file = open("myfile.json", "w")  # w = write to file
    # or with open("myfile.json", "w") as outfile
    json.dump(celeb_json, out_file)
    out_file.close()
    connection.commit()
    cursor.close()
    connection.close()

    return celeb_json


@app.route('/updateCelebrity/<int:item_id>/<int:age>', methods=['PUT'])
def updateCelebrityId(item_id, age):
    connection = database_connector()
    print('Connected to DB')
    cursor = connection.cursor()
    update_sql = """update celebrity
    set age = {}
    where id = {}
    """
    cursor.execute(update_sql.format(item_id, age))
    connection.commit()
    cursor.close()
    connection.close()
    return "Celebrity information updated"


app.run(host='localhost', port=5000, debug=True)
