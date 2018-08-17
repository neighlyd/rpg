class EndGame(Exception):
    pass


class EndGameDied(EndGame):

    def __init__(self, message="You Died."):
        self.message = message


class NotEnoughRoomsInZone(EndGame):
    pass


class ZoneAlreadyExists(EndGame):
    pass


class ZoneCreationError(EndGame):
    pass


class RoomDoesNotExist(EndGame):
    pass


class ItemNotInDictionary(EndGame):
    def __init__(self, message="That item is not in the item dictionary."):
        self.message = message
