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
    resp = json.loads(r.text)
    return resp

def getUserBoards():
    data = []
    r = requests.get(API_MEMBERS_ME_BOARDS, params={'key': API_KEY, 'token': API_TOKEN})
    resp = json.loads(r.text)
    for i in resp:
        data.append({'name': i['name'], 'id': i['id']})
    return data

def getCardsOfUserWithBoardID(userid, boardid):
    data = []
    r = requests.get(API_BOARDS_CARD.format(id=boardid), params={'key': API_KEY, 'token': API_TOKEN})
    resp = json.loads(r.text)
    for i in resp:
        if userid in i['idMembers']:
            data.append(i)
    return data

def main():
    card_count = 0
    user = getUser()
    userid = user['id']
    boards = getUserBoards()
    for board in boards:
        count = len(getCardsOfUserWithBoardID(userid, board['id']))
        card_count += count
        print("{board}: {count}".format(board=board['name'], count=count))
    print("Total Cards of {username}: {count}".format(username=user['initials'], count=card_count))

if __name__ == '__main__':
    main()
