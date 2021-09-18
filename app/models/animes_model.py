
from app.exceptions.animes_exceptions import AnimeNotFoundError, InvalidKeyError, AttributeIsMissingError
from app.services.db_services import execute_cmd
from typing import Tuple, Union
from datetime import date

from psycopg2 import sql



AVALIABLE_KEYS = ['anime', 'seasons', 'released_date']

class Anime: 
    def __init__(self, fields: Union[ Tuple[int, str, date, int], dict[str, date, int] ]) -> None:

        if type(fields) is tuple:

            self.id, self.anime, self.released_date, self.seasons = fields

            self.released_date = self.released_date.strftime('%d/%m/%Y')

        elif type(fields) is dict:
            for k, v in fields.items():

                if k == 'anime':
                    v = v.title()
                setattr(self, k, v)

    @staticmethod
    def checking_keys(data: dict):

        not_avaliable = []

        for k in data.keys():
            if k not in AVALIABLE_KEYS:
                not_avaliable.append(k)

        if len(not_avaliable) > 0:
            raise InvalidKeyError(AVALIABLE_KEYS, not_avaliable)

    @staticmethod
    def get_data() -> list:

        query = """
            SELECT 
                * 
            FROM 
                animes;
        """

        fetch_data = execute_cmd(query, 'all')

        serialized_data = [Anime(anime_data).__dict__ for anime_data in fetch_data]

        return serialized_data

    def create(self) -> dict:

        Anime.checking_keys(self.__dict__)

        request_keys_len = len([k for k in self.__dict__.keys()])

        if request_keys_len < len(AVALIABLE_KEYS):
            
            raise AttributeIsMissingError

        converted_data = tuple([v for v in self.__dict__.values()])

        query = """
            INSERT INTO animes
                (anime, released_date, seasons)
            VALUES
                {}
            RETURNING *;
        """.format(converted_data)

        fetch_data = execute_cmd(query, 'one')

        serialized_data = Anime(fetch_data).__dict__ 

        return serialized_data

      
    @staticmethod
    def get_data_by_id(id: int) -> dict:

        query = """
            SELECT
                *
            FROM 
                animes
            WHERE id = %s;
        """ % (id)

        fetch_data = execute_cmd(query, 'one')
        
        if not fetch_data:
            raise AnimeNotFoundError

        serialized_data = Anime(fetch_data).__dict__ 

        return serialized_data

    @staticmethod
    def delete(id: int) -> None:
        
        if not Anime.get_data_by_id(id):
            raise AnimeNotFoundError

        query = """
            DELETE
            FROM 
                animes
            WHERE id = %s;
        """ % (id)

        execute_cmd(query)

    @staticmethod
    def update(id: int, data: dict) -> None:

        Anime.checking_keys(data)        

        if data['anime']:
            data['anime'] = data['anime'].title()
        
        columns = [sql.Identifier(k) for k in data.keys()]

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
                
        fetch_data = execute_cmd(query, 'one')

        if not fetch_data:
            raise AnimeNotFoundError

        serialized_data = Anime(fetch_data).__dict__ 

        return serialized_data
