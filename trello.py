import requests
key = "key"
token = "token"

# Create board
url = "https://api.trello.com/1/boards/"
querystring = {"name": "Holidays_Test", "idBoard": "holidays", "key": key, "token": token}
response = requests.request("POST", url, params=querystring)

# Create list
url = "https://api.trello.com/1/boards/{boardId}/lists"
querystring = {"name": "test12", "pos": "top", "key": key, "token": token}
response = requests.request("POST", url, params=querystring)
print(response.text)

# Create card
url = "https://api.trello.com/1/cards"
querystring = {"name": "sample", "idList": "listId", "keepFromSource": "all","key": key, "token": token}
response = requests.request("POST", url, params=querystring)
print(response.text)
