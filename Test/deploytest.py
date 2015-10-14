import requests
import json
import random
import math

#hostname = "http://localhost:5000"
#hostname = 'http://wherewolf-1231767711.us-west-2.elb.amazonaws.com'
hostname = 'http://wherewolflb-1561986807.us-west-2.elb.amazonaws.com'

rest_prefix = "/v1"

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
    return response 

def cast_vote(username, password, game_id, target_id):
    payload = {'username': username, 'password': password, 'game_id': game_id, 'target_id': target_id}    
    r = requests.post(hostname + rest_prefix + "/game/" + str(game_id) + "/vote",auth=(username, password), data=payload)
    response = r.json()

    print response 

## MAKE THIS WORK
def get_ballot(username, password, game_id): 
    payload = {'game_id': game_id}
    url = "{}{}{}{}{}".format(hostname, rest_prefix, "/game/", str(game_id), "/ballot")
    r = requests.get(url, auth=(username, password), data=payload)
    #r = requests.get(hostname + rest_prefix + "/game/" + str(game_id) + "/ballot", auth=(username, password), data=payload)
    response = r.json()
    #print response["status"]
    #print response["results"]
    #return response["voted_out"]
    return response

def set_game_status(username, game_id, game_status):
    payload = {'username': username, 'game_id': game_id, 'game_status': game_status}
    requests.post(hostname + rest_prefix + "/game/" + str(game_id) +"/status", data=payload)
    return

def get_playerid(username):
    payload = {'username': username}
    r = requests.get(hostname + rest_prefix + "/user", data=payload)
    response = r.json()
    return response['playerid']

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
    create_user('michael', 'paper01', 'Michael', 'Scott')
    create_user('dwight', 'paper02', 'Dwight', 'Schrute')
    create_user('jim', 'paper03', 'Jim', 'Halpert')
    create_user('pam', 'paper04', 'Pam', 'Beesly')
    create_user('ryan', 'paper05', 'Ryan', 'Howard')
    create_user('andy', 'paper06', 'Andy', 'Bernard')
    create_user('angela', 'paper07', 'Angela', 'Martin')
    create_user('toby', 'paper08', 'Toby', 'Flenderson')

def all_join_game(game_id):
    join_game('dwight', 'paper02', game_id)
    join_game('jim', 'paper03', game_id)
    join_game('pam', 'paper04', game_id)
    join_game('ryan', 'paper05', game_id)
    join_game('andy', 'paper06', game_id)
    join_game('angela', 'paper07', game_id)
    join_game('toby', 'paper08', game_id)

def set_werewolf(game_id, werewolf_id):
    payload = {'werewolf_id': werewolf_id, 'game_id': game_id}
    requests.post(hostname + rest_prefix + "/game/" + str(game_id) +"/werewolf", data=payload )
    return

def attack_villager(username, password, game_id, target_id):
    payload = {'username': username, 'password': password, 'game_id': game_id, 'target_id': target_id}
    r = requests.post(hostname + rest_prefix + "/game/" + str(game_id) + "/attack",auth=(username, password), data=payload)
    response = r.json()
    print response

def assign_lupus_and_clear_votes_table(game_id, death_player_id):
    payload = {'game_id': game_id, 'death_player_id': death_player_id}
    requests.post(hostname + rest_prefix + "/game/" + str(game_id) +"/assign_lupus", data=payload )
    return

def clean_game_data():
    r = requests.delete(hostname + rest_prefix +"/cleandatabase" )
    response = r.json()
    print response

def set_top_voted_death(game_id, player_id):
    payload = {'game_id': game_id, 'player_id': player_id}
    requests.post(hostname + rest_prefix + "/game/" + str(game_id) +"/vote_death", data=payload )
    return

def check_game_results(game_id):
    payload = {'game_id': game_id}
    r = requests.get(hostname + rest_prefix + "/game/" + str(game_id) +"/game_results", data=payload )
    response = r.json()
    return response

def update_locations(game_id):
    #positioned in a rectangular region (9.9, 9.9),(10.1, 10.1). Max possible Distance: 31210m
    minValue = 9.9
    maxValue = 10.1
    update_game('michael', 'paper01', game_id, random.uniform(minValue, maxValue), random.uniform(minValue, maxValue))
    update_game('dwight', 'paper02', game_id, random.uniform(minValue, maxValue), random.uniform(minValue, maxValue))
    update_game('jim', 'paper03', game_id, random.uniform(minValue, maxValue), random.uniform(minValue, maxValue))
    update_game('pam', 'paper04', game_id, random.uniform(minValue, maxValue), random.uniform(minValue, maxValue))
    update_game('ryan', 'paper05', game_id, random.uniform(minValue, maxValue), random.uniform(minValue, maxValue))
    update_game('andy', 'paper06', game_id, random.uniform(minValue, maxValue), random.uniform(minValue, maxValue))
    update_game('angela', 'paper07', game_id, random.uniform(minValue, maxValue), random.uniform(minValue, maxValue))
    update_game('toby', 'paper08', game_id, random.uniform(minValue, maxValue), random.uniform(minValue, maxValue))


if __name__ == "__main__":
    
    print "--------------------Preparing the game---------------------"
    clean_game_data()

    game_day = 0
    #------------------Game Simulation---------------------------------
    # The client script will register 8 new users
    print "-----------creating users---------------------------------"
    create_users()

    
    # A new game called NightHunt will be created by michael, as the admin michael will automatically be
    # added to the game. All the other users will join that game with new players being created for 
    # each of the users. 
    print "------------------------------creating a game-------------------------------------"
    admin_username = 'michael'
    admin_password = 'paper01'
    game_id = create_game(admin_username, admin_password, "NightHunt", "SAMPLE GAME")
    print '-----------------Rest of Users join the game----------------------'
    all_join_game(game_id)
    
    #---------------GET this list ready for voting--------------#
    list_players = ['michael', 'dwight', 'jim', 'pam', 'ryan', 'andy', 'angela', 'toby']
    list_password = ['paper01', 'paper02', 'paper03', 'paper04', 'paper05', 'paper06', 'paper07', 'paper08']
    username_password_playerid_list = []
    for i in range(len(list_players)): 
        player = {}
        player['username'] = list_players[i]
        player['password'] = list_password[i]
        player['playerid'] = get_playerid(player['username'])
        username_password_playerid_list.append(player)
    
    
    # Admin will set the game to active, and the first day round begins.
      # michael will set the game to active, and the first day round begins.
    print '-----------------start the game----------------------'
    set_game_status(admin_username, game_id, 1)
    set_game_time(admin_username, game_id, '22:00:00')

    # 30% of the players rounding up will be set to be werewolves (3 werewolves in our case) 
    print '-----------------current game info----------------------'
    c_game_info = game_info(admin_username, admin_password, game_id)
    random_playerid_list =[ entry['playerid'] for entry in c_game_info['players'] ]
    random.shuffle(random_playerid_list)
    num_werewolf = int(math.ceil(len(random_playerid_list)*0.3))
    for i in xrange(num_werewolf):
        set_werewolf(game_id,random_playerid_list[i])
    
    # Daytime:  Voting starts on day 2. All Players will be randomly positioned in a rectangular region.
    # The admin sets the round to night.
    # One werewolf will move to a location of one random villager. The werewolf will make an attack. The villager may or may not survive this encounter
    # The admin sets the round to day.
    # pprint (current_game_info)  # print game_info before it starts.
    
    
    
    while(c_game_info['status']['status'] == 1):  # as long as game not end yet, continue play
        print "------------set to day time------------------"
        set_game_time(admin_username, game_id, '10:00:00')
        game_day += 1

        print "%%%%%%-----------------------Game in daytime-------------------------%%%%%%%%%%%"
        print "%%%%%%----------------------------round {}---------------------------%%%%%%%%%%%".format(game_day)
        if game_day <= 1:      #There is no vote in first day round
            print "------------------------set all random landmark in random place in day 1------------------"
            #numLandmark = set_random_landmark(current_game_id)   # set random land marks on the game in day 1
            #print "------------------------attach treasure to each landmark if it is not a save zone------------------"
            #set_treasure_to_landmark(current_game_id,numLandmark)         # link treasure to landmark
            update_locations(game_id)
        else:
            # print "------------------------ reset set all random landmark in random place after day 1------------------"
            # clean_landmark_treasure()
            #numLandmark = set_random_landmark(current_game_id)   # set random land marks on the game in day 1
            #print "------------------------attach treasure to each landmark if it is not a save zone------------------"
            #set_treasure_to_landmark(current_game_id,numLandmark)         # link treasure to landmark
    
            #-------get all alive playerid:----------------
    
        
            alive_playerid_list = []
            for player in c_game_info['players']:
                if player['is_dead'] == 0:
                    alive_playerid_list.append(int(player['playerid']))
             # -------------every one votes------------------
            print "-----------Voting begins---------------"
            for player in c_game_info['players']:
                if int(player['is_dead']) == 0:
                    # get the user_info
                    for i in xrange(len(username_password_playerid_list)):
                        if username_password_playerid_list[i]['playerid'] == player['playerid']:
                            userInfo = username_password_playerid_list[i]
                            break
                            
                    # get target id, target id can not be voter's player id
                    target_id = alive_playerid_list[random.randint(0,len(alive_playerid_list)-1)]
                    while(target_id == player['playerid']):
                        target_id = alive_playerid_list[random.randint(0,len(alive_playerid_list)-1)]

                    # call vote function
                    cast_vote(userInfo['username'], userInfo['password'], game_id, target_id)

            
            print '-------showing vote results and checking if game is end, clear all vote info after pull over vote results'
            vote_results = get_ballot(admin_username, admin_password, game_id)
            print vote_results
            vote_results_sorted = sorted(vote_results['results'], key = lambda k: k['votes'], reverse=True )   

            print "-----------------voting results for round {}----------------------------".format(game_day)
            print (vote_results_sorted)
        #### works above
                     
            print '#---------------set top voted player to death------------------'
            if len(vote_results_sorted) > 0:
                dead_playerid = vote_results_sorted[0]['player_id']
                set_top_voted_death(game_id,dead_playerid)
                for player in c_game_info['players']:
                    if dead_playerid == player['playerid']:
                        werewolf_checker = player['is_werewolf']

                        print '#-----------if the dead is not a werewolf----assign lupus---------------------#'
                        print 'ww_c', werewolf_checker
                        if werewolf_checker == 0:   # then assign lupus to each player's stats
                            assign_lupus_and_clear_votes_table(game_id, dead_playerid)
                        break

                    
                #werewolf_checker = c_game_info['players']['is_werewolf'] # check if the dead is werewolf 
               # print '#-----------if the dead is not a werewolf----assign lupus---------------------#'
               # print 'ww_c', werewolf_checker
                #if werewolf_checker == 0:   # then assign lupus to each player's stats
                #    assign_lupus_and_clear_votes_table(game_id, dead_playerid)
        #### works above
            
            
            print '#---------------is game ended?? who won??------------------'
            
            game_results = check_game_results(game_id)
            print game_results
            if game_results['status'] == 'villagers won' or game_results['status'] == 'werewolves won':
                set_game_status(admin_username, game_id, 2)
                break  # game ended
            else:
                update_locations(game_id)
        ### works above
            
        print "#-----------update current_game_info before night comes---------------------------"
        c_game_info = game_info(admin_username, admin_password, game_id)
        #game_info = game_info(admin_username, admin_password, game_id)

        
        ########################THE NIGHT IS COMING###################################################
        print "set to a night time"
        set_game_time(admin_username, game_id, '20:00:00')
        print "%%%%%%-----------------------Game in night time-------------------------%%%%%%%%%%%"
        print "%%%%%%----------------------------round {}---------------------------%%%%%%%%%%%".format(game_day)

        alive_werewolf_list = []
        alive_village_list = []
        for player in c_game_info['players']:
            if player['is_dead'] == 0 and player['is_werewolf'] == 0:
                alive_village_list.append(int(player['playerid']))
            elif player['is_dead'] == 0 and player['is_werewolf'] != 0:
                alive_werewolf_list.append(int(player['playerid']))
        # -------------every one votes--------------------
    ### works above
        
        print "----------------Attacking Begins-----------------------"

        attacker_id = alive_werewolf_list[random.randint(0,len(alive_werewolf_list)-1)]
        target_id = alive_village_list[random.randint(0,len(alive_village_list)-1)]

        for i in xrange(len(username_password_playerid_list)):
            if username_password_playerid_list[i]['playerid'] == attacker_id:
                attackerInfo = username_password_playerid_list[i]

        # call attack function
        attack_villager(attackerInfo['username'], attackerInfo['password'], game_id, target_id)

        print '#---------------is game ended?? werewolves won???------------------'
        game_results = check_game_results(game_id)
        print game_results
        if game_results['status'] == 'werewolves won':
            set_game_status(admin_username, game_id, 2)
            break  # game ended
        else:
            update_locations(game_id)

        # update current game info before going next loop.
        c_game_info = game_info(admin_username, admin_password, game_id)


### check this later
    ########################THE GAME HAS ENDED#########################################
    c_game_info = game_info(admin_username, admin_password, game_id)
    print "Game status: {}".format(c_game_info['status'])
    print "------------------game ended--------------------"
    #Set all the game's users' current player field to NULL
    print "------------------everyone left the game-----------------------"
    leave_game(admin_username, admin_password, game_id)
    #print "------------------Assigning Achievements----------------------"
   # assign_achievement()
    #print "----------------Show all achievement made in last game--------------------------"
    #all_achievement = get_all_achievement()
    #print(all_achievement)
    
