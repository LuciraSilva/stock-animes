class AttributeIsMissing(Exception):
    ...


class DatabaseNotFound(Exception):
    ...

class AnimeNotFound(Exception):
    ...

class InvalidKey(Exception):     

    def __init__(self, valid_keys: list, invalid_keys: list) -> None:

        self.message = {'valid_keys': valid_keys, 'invalid_keys': invalid_keys}

        super().__init__(self.message)