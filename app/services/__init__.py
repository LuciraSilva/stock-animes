from app.exceptions.anime_error import AttributeIsMissing, InvalidKey
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

configs = {
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD'),
    'host': os.getenv('HOST'),
    'database': os.getenv('DB_NAME')
}

def create_db():
    try:
        conn = psycopg2.connect(**configs)

        conn.close()

    except psycopg2.OperationalError:
        conn = psycopg2.connect(user=configs['user'], password=configs['password'])

        conn.autocommit = True

        cur = conn.cursor()

        cur.execute("""
            CREATE DATABASE %s;
        """ % configs['database'])


        cur.close()
        conn.close()
        

def create_animes_table():

    conn = psycopg2.connect(**configs)

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS animes (
            id BIGSERIAL PRIMARY KEY,
            anime VARCHAR(100) NOT NULL UNIQUE,
            released_date DATE NOT NULL,
            seasons INTEGER NOT NULL
        );
    """)

    conn.commit()

    cur.close()
    conn.close()


def checking_keys(data: dict):
    valid_keys = ['name', 'seasons', 'released_date']
    invalid_keys = []

    if len([k for k in data.keys()]) < len(valid_keys):

        raise AttributeIsMissing("You need to send: 'name', 'released_date' and 'seasons' ")

    for k in data.keys():
        if k not in valid_keys:
            invalid_keys.append(k)

    if len(invalid_keys) > 0:
        raise InvalidKey(valid_keys, invalid_keys)

        
def convert_dict_to_tuple(data: dict):
    return tuple([v for v in data.values()])


