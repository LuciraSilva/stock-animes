class AttributeIsMissingError(Exception):

    def __init__(self) -> None:

        message = "Make sure you send: 'anime', 'released_date' and 'seasons'"

        super().__init__(message)
    

class AnimeNotFoundError(Exception):

    def __init__(self) -> None:

        message = 'Anime not found'

        super().__init__(message)


class InvalidKeyError(Exception):     

    def __init__(self, valid_keys: list, invalid_keys: list) -> None:

        self.message = {'valid_keys': valid_keys, 'invalid_keys': invalid_keys}

        super().__init__(self.message)