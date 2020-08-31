import requests
key = "your_key"
token = "your_token"


def create_board(board_name):
    """
    Creates a board based on the given board name.

    :param board_name:
    :returns: board_id
    """

    url = "https://api.trello.com/1/boards/"
    querystring = {"name": board_name, "prefs_background": "sky", "key": key, "token": token}
    response = requests.request("POST", url, params=querystring)
    board_id = response.json()["shortUrl"].split("/")[-1].strip()
    return board_id


def create_list(board_id, list_name, position):
    """
    Creates a list based on the given list name.

    :param board_id:
    :param list_name:
    :param position: the position of the list, '1' being the first in the order
    :returns: list_id
    """

    url = f"https://api.trello.com/1/boards/{board_id}/lists"
    querystring = {"name": list_name, "pos": position, "key": key, "token": token}
    response = requests.request("POST", url, params=querystring)
    list_id = response.json()["id"]
    return list_id


def create_card(list_id, card_name):
    """
    Creates a card based on the given card name.

    :param list_id:
    :param card_name:
    :returns: card_id
    """

    url = "https://api.trello.com/1/cards"
    querystring = {"name": card_name, "idList": list_id, "key": key, "token": token}
    response = requests.request("POST", url, params=querystring)
    card_id = response.json()["id"]
    return card_id
