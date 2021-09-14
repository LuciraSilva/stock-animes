
from app.services import convert_dict_to_tuple
from app.exceptions.anime_error import AnimeNotFound, InvalidKey
from typing import Tuple, Union

from datetime import date

import os

import psycopg2
from psycopg2 import sql


configs = {
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD'),
    'host': os.getenv('HOST'),
    'database': os.getenv('DB_NAME')
}

class Anime: 
    def __init__(self, fields: Union[ Tuple[int, str, date, int], dict[str, date, int] ]) -> None:

        if type(fields) is tuple:
            self.id, self.name, self.released_date, self.seasons = fields

            self.released_date = self.released_date.strftime('%d/%m/%Y')

        elif type(fields) is dict:
            for k, v in fields.items():
                if k == 'name':
                    v = v.title()
                setattr(self, k, v)

    @staticmethod
    def get_data() -> list:
        conn = psycopg2.connect(**configs)

        cur = conn.cursor()

        cur.execute("""
            SELECT
                *
            FROM 
                animes;
        """)

        getting_data = cur.fetchall()

        conn.commit()

        cur.close()
        conn.close()

        serialized_data = [Anime(anime_data).__dict__ for anime_data in getting_data]

        return serialized_data

    def save(self) -> dict:
        conn = psycopg2.connect(**configs)

        cur = conn.cursor()

        converted_data = convert_dict_to_tuple(self.__dict__)
        print(converted_data)
        cur.execute("""
            INSERT INTO animes
                (anime, released_date, seasons)
            VALUES
                {}
            RETURNING *;
        """.format(converted_data))

        added_anime = cur.fetchone()

        conn.commit()

        cur.close()
        conn.close()

        serialized_data = Anime(added_anime).__dict__ 

        return serialized_data

      
    @staticmethod
    def get_data_by_id(id: int) -> dict:

        conn = psycopg2.connect(**configs)

        cur = conn.cursor()

        cur.execute("""
            SELECT
                *
            FROM 
                animes
            WHERE id = %s;
        """ % id)

        getting_data = cur.fetchone()
        
        if not getting_data:
            raise AnimeNotFound('anime not found')

        conn.commit()

        cur.close()
        conn.close()

        serialized_data = Anime(getting_data).__dict__ 

        return serialized_data

    @staticmethod
    def delete(id: int) -> None:
        
        if not Anime.get_data_by_id(id):
            raise AnimeNotFound('anime not found')

        conn = psycopg2.connect(**configs)

        cur = conn.cursor()

        cur.execute("""
            DELETE
            FROM 
                animes
            WHERE id = %s;
        """ % (id))

        conn.commit()

        cur.close()
        conn.close()

    @staticmethod
    def update(id: int, data: dict) -> None:

        valid_keys = ['name', 'released_date', 'seasons']
        invalid_keys = []

        for k in data.keys():
            if k not in valid_keys:
                invalid_keys.append(k)

        if len(invalid_keys) > 0:
            raise InvalidKey(valid_keys, invalid_keys)        
        
        conn = psycopg2.connect(**configs)

        cur = conn.cursor()

        if 'name' in data.keys():
            data['name'] = data['name'].title()

        columns = [sql.Identifier('anime') if  k == 'name' else sql.Identifier(k) for k in data.keys()]
        values = [sql.Literal(v) for v in data.values()]

        query = sql.SQL(
            """
                UPDATE
                    animes
                SET
                    ({columns}) = row({values})
                WHERE
                    id={id}
                RETURNING *
            """).format(id=sql.Literal(str(id)),
                        columns=sql.SQL(',').join(columns),
                        values=sql.SQL(',').join(values))
                
        cur.execute(query)


        fetch_result = cur.fetchone()

        if not fetch_result:
            raise AnimeNotFound('anime not found')


        conn.commit()

        cur.close()
        conn.close()

        serialized_data = Anime(fetch_result).__dict__ 

        return serialized_data
