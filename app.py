import requests, json
import configparser

config = configparser.ConfigParser()
config.read('tokens.cfg')

API_BASE_URL = "https://api.trello.com/1"
API_MEMBERS_ME = API_BASE_URL + "/members/me/"
API_MEMBERS_ME_BOARDS = API_BASE_URL + "/members/me/boards"
API_BOARDS_CARD = API_BASE_URL + "/boards/{id}/cards"
API_KEY = config['TRELLO']['API_KEY']
API_TOKEN = config['TRELLO']['API_TOKEN']

def getUser():
    r = requests.get(API_MEMBERS_ME, params={'key': API_KEY, 'token': API_TOKEN})
    user = json.loads(r.text)
    return user

def getUserBoards():
    data = []
    r = requests.get(API_MEMBERS_ME_BOARDS, params={'key': API_KEY, 'token': API_TOKEN})
    boards = json.loads(r.text)
    for board in boards:
        data.append({'name': board['name'], 'id': board['id']})
    return data

def getCardsOfUserWithBoardID(userid, boardid):
    cardsOfUser = []
    r = requests.get(API_BOARDS_CARD.format(id=boardid), params={'key': API_KEY, 'token': API_TOKEN})
    cards = json.loads(r.text)
    for card in cards:
        if userid in card['idMembers']:
            cardsOfUser.append(card)
    return cardsOfUser

def main():
    cardOfUserCount = 0
    user = getUser()
    userid = user['id']
    boards = getUserBoards()
    for board in boards:
        count = len(getCardsOfUserWithBoardID(userid, board['id']))
        cardOfUserCount += count
        print("{board}: {count}".format(board=board['name'], count=count))
    print("Total of {username}: {count}".format(username=user['initials'], count=cardOfUserCount))

if __name__ == '__main__':
    main()
