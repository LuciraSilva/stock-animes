from app.services.db_services import connect_to_db, disconnect_from_db
from .db_configs import configs
import psycopg2

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

    conn, cur = connect_to_db()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS animes (
            id BIGSERIAL PRIMARY KEY,
            anime VARCHAR(100) NOT NULL UNIQUE,
            released_date DATE NOT NULL,
            seasons INTEGER NOT NULL
        );
    """)

    conn.commit()
    
    disconnect_from_db(conn, cur)



