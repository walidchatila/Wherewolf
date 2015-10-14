import requests
import json

hostname = "http://localhost:5000"
# user = 'rfdickerson'
# password = 'awesome'
game_id = 0

rest_prefix = "/v1"

''' Important functions
create a game
leave a game
update game state with location
cast a vote
'''

def create_user(username, password, firstname, lastname):
    payload = {'username': username, 'password': password, 'firstname': firstname, 'lastname': lastname}
    url = "{}{}{}".format(hostname, rest_prefix, "/register")
    r = requests.post(url, data=payload)
    response = r.json()
    print response["status"]
    print response["error"]

def create_game(username, password, game_name, description):
    payload = {'game_name': game_name, 'description': description}
    url = "{}{}{}".format(hostname, rest_prefix, "/game")
    print 'sending {} to {}'.format(payload, url)
    r = requests.post(url, auth=(username, password), data=payload)
    response = r.json()
    print response["status"]
    return response["results"]["game_id"]


def leave_game(username, password, game_id):
    r = requests.delete(hostname + rest_prefix + "/game/" + str(game_id), 
                        auth=(username, password))
    
    response = r.json()

    print response["status"]
    print response["error"]

def update_game(username, password, game_id, lat, lng):
    """ reports to the game your current location, and the game 
    returns to you a list of players nearby """

    payload = {'lat': lat, 'lng': lng}
    url = "{}{}/game/{}".format(hostname, rest_prefix, game_id)
    r = requests.put(url, auth=(username, password), data=payload)
    response = r.json()
    print response


def game_info(username, password, game_id):
    ''' returns all the players, the time of day, and other options for the game '''
    r = requests.get(hostname + rest_prefix + "/game/" + str(game_id), auth=(username, password))
    response = r.json()
    print response['info']

def cast_vote(username, password, game_id, target_id):
    payload = {'username': username, 'password': password, 'game_id': game_id, 'target_id': target_id}    
    r = requests.post(hostname + rest_prefix + "/game/" + str(game_id) + "/vote",auth=(username, password), data=payload)
    response = r.json()

    print response 

def get_ballot(username, password, game_id): 
    payload = {'username': username, 'password': password, 'game_id': game_id}
    r = requests.get(hostname + rest_prefix + "/game/" + str(game_id) + "/ballot",auth=(username, password), data=payload)
    response = r.json()
    print response
    return response

def set_game_time(username, game_id, game_time):
    ''' allows you to override the current time to a user specified one'''
    payload = {'username': username, 'game_id': game_id, 'game_time': game_time}
    r = requests.post(hostname + rest_prefix + "/game/" + str(game_id) +"/time", data=payload)
    response = r.json()
    print response

def join_game(username, password, game_id):
    print 'Joining game id {}'.format(game_id)
    payload = {'game_id': game_id}
    url = "{}{}/game/{}/lobby".format(hostname, rest_prefix, game_id)
    r = requests.post(url, auth=(username, password))
    response = r.json()
    print response["status"]
    print response["error"]

def get_games(username, password):
    r = requests.get(hostname + rest_prefix + "/game")
    r = r.json()
    return r["results"]


def create_users():
    create_user('michael', 'paper', 'Michael', 'Scott')
    create_user('dwight', 'paper', 'Dwight', 'Schrute')
    create_user('jim', 'paper', 'Jim', 'Halpert')
    create_user('pam', 'paper', 'Pam', 'Beesly')
    create_user('ryan', 'paper', 'Ryan', 'Howard')
    create_user('andy', 'paper', 'Andy', 'Bernard')
    create_user('angela', 'paper', 'Angela', 'Martin')
    create_user('toby', 'paper', 'Toby', 'Flenderson')

def werewolf_winning_game():
    game_id = create_game('michael', 'paper', 'NightHunt', 'A test for werewolf winning')
    games = get_games('michael', 'paper')
    for game in games:
        print "Id: {},\tName: {}".format(game["game_id"], game["name"])
    
    join_game('dwight', 'paper', game_id)
    join_game('jim', 'paper', game_id)
    join_game('pam', 'paper', game_id)
    join_game('ryan', 'paper', game_id)
    join_game('andy', 'paper', game_id)
    join_game('angela', 'paper', game_id)
    join_game('toby', 'paper', game_id)
    start_game('michael', 'paper', game_id)
    
    leave_game('micheal', 'paper', game_id)
    

if __name__ == "__main__":

    #create_users()
    #werewolf_winning_game()
    #create_user('dima', 'password', 'dima', 'chatila')
    #create_game('walid', 'password', 'NightHunt', 'A game in Austin')
    #update_game('rfdickerson', 'awesome', 3, 80, 20)
    #game_info('rfdickerson', 'awesome', 22)
    #leave_game('rfdickerson', 'awesome', 1)
    #create_user('kevin', 'password', 'walid', 'chatila')
    #join_game('dala', 'password', 6)
    #game_info('rfdickerson', 'awesome', 3)
    #cast_vote('rfdickerson', 'awesome', 1, 'oliver') 
    #set_game_time('rfdickerson', 1, '08:00:00')
    get_ballot('rfdickerson', 'awesome', 1)

        