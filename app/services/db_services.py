import psycopg2
from .db_configs import configs

def connect_to_db():

    conn = psycopg2.connect(**configs)

    cur = conn.cursor()

    return (conn, cur)

def disconnect_from_db(conn, cur):

    cur.close()

    conn.close()


def execute_cmd(cmd: str, chosen_fetch=None):

    conn, cur = connect_to_db()

    command, chosen_fetch = cmd, chosen_fetch

    cur.execute(command)

    fetch_data = None

    if chosen_fetch == 'one':

        fetch_data = cur.fetchone()

    elif chosen_fetch == 'all':
        
        fetch_data = cur.fetchall()

    conn.commit()

    disconnect_from_db(conn, cur)

    return fetch_data




