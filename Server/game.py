from flask import Flask, request, jsonify
import psycopg2
app = Flask(__name__)
from wherewolfdao import WherewolfDao 
import datetime 
from collections import defaultdict
import random

dbhour = "08:00:00" 
daybreakhour = datetime.datetime.strptime(dbhour , "%H:%M:%S")
nfhour = "20:00:00"
nightfallhour = datetime.datetime.strptime(nfhour , "%H:%M:%S")
d = WherewolfDao()

def get_time(game_id):
    db_time = d.get_db_time(game_id)
    if db_time == None:
        current_time = datetime.datetime.now()
        return current_time
    else:
        current_time = db_time
        current_time = datetime.datetime.strptime(current_time  , "%H:%M:%S")
        return   current_time

def isNight(game_id):
    current_time = get_time(game_id)
    if current_time >= nightfallhour or current_time < daybreakhour:
        return True

def isDay(game_id):
    current_time = get_time(game_id)
    if current_time >= daybreakhour or current_time < nightfallhour:  
        return  True  

def get_db(databasename='wherewolf', 
        username='postgres',
        password='psql4me'):
    return psycopg2.connect(database= databasename,
             user=username, password=password)
@app.route('/healthcheck')
def health_check():
    return "healthy"
@app.route("/")
def hello():
    return "Hello World!!!"

@app.route('/v1/checkpassword', methods = ["GET"])
def check_password():

    auth = request.authorization
    username = auth.username
    password = auth.password
    check_pw = d.check_password(username, password)
    response = {}
    #response['status'] = 'success'
    if check_pw:
        response['status'] = 'success'
    else:
        response['error'] = "Invalid Username and or Password"

    return jsonify(response)

# DONE
@app.route('/v1/register', methods=["POST"])
def create_user():
    username = request.form['username']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    user = d.get_username(username)
    response = {}
    response["error"]  = ""
    if not user and len(password) >= 5:
        d.create_user(username, password, firstname, lastname)
        print 'created a user called {}'.format(username)
        response["status"] = "success"
    if not user and len(password) < 5:
        response["status"] = "Failure"
        response["error"]  = "Password too short, must be at least 5 charachters."
    if user and len(password) >= 5:
        response["status"] = "Failure"
        response["error"] = "User already exists."
    if user and  len(password) < 5:
        response["status"] = "Failure"
        response["error"]  = "User already exists and password too short, must be at least 5 charachters."
    return jsonify(response)
#DONE
@app.route('/v1/game', methods=["POST"])
def create_game():
    game_name = request.form["game_name"]
    description = request.form['description']
    auth = request.authorization
    username = auth.username
    password = auth.password
    response = {}
    response["results"] = {}
    response["results"]["game_id"] = '' 
    response["error"]  = ""
    admin_id = d.get_admin_id(username)
    if not admin_id and d.check_password(username, password):
        game_id = d.create_game(username, game_name, description)
        d.join_game(username, game_id)
        response["status"] = "success" 
        response["results"]["game_id"] = game_id  
    if not admin_id and not d.check_password(username, password):
        response["status"] = "Failure" 
        response["error"]  = "Bad authentication."  
    if admin_id and d.check_password(username, password):
        response["status"] = "Failure"
        response["error"]  = "Already administrating a game."
    if admin_id and not d.check_password(username, password):
        response["status"] = "Failure" 
        response["error"]  = "Bad authentication and already administrating a game"
    return jsonify(response)
# work on deleting all current player records for other players of game
@app.route('/v1/game/<int:game_id>', methods=["DELETE"])
def leave_game(game_id):
    auth = request.authorization
    username = auth.username
    password = auth.password
    response = {}
    response["error"]  = ""
    admin_id = d.get_admin_game(game_id, username)
    player_id= d.get_player_id_game(username, game_id)

    if admin_id and d.check_password(username, password): # IF ADMIN DELETE whole game 
        d.delete_game_as_admin(game_id, admin_id)
        #d.leave_game(username)
        response["status"] = "Success"
    
    if admin_id and not d.check_password(username, password):
        response["status"] = "Failure"
        response["error"]  = "Bad authentication"
   
    if not admin_id and player_id and d.check_password(username, password): # IF NOT ADMIN DELETE only this player
        d.delete_player(game_id, username)
        d.leave_game(username)
        response["status"] = "Success"
        response["error"]  = "Not an admin, only this player deleted from the game."

    if not admin_id and player_id and not d.check_password(username, password):
        response["status"] = "Failure"
        response["error"]  = "Bad authentication"
    
    if not player_id: 
        response["status"] = "Failure"
        response["error"]  = "Not a player in a game."

    return jsonify( response )
# DONE

@app.route('/v1/games')
def get_games():
    auth = request.authorization
    username = auth.username
    password = auth.password
    response = {} 
    response["results"] = {}
    results = d.get_games()
    response["results"] = results 
    print "test"
    print (response["results"])
    return jsonify(response)

@app.route('/v1/game/<int:game_id>/lobby', methods = ["POST"]) 
def join_game(game_id):
    auth = request.authorization
    username = auth.username
    password = auth.password
    current_player = d.get_current_player(username)
    info = d.game_info(game_id)
    status = info["status"]
    response ={}
    response["error"]=''

    if not current_player and d.check_password(username, password) and status==0:
        d.join_game(username, game_id)
        response["status"] = "success"
    if  current_player:
        response["status"] = "Failure"
        response['error']  = "Already in another game"
    if not current_player and not d.check_password(username, password) and status==0:
        response["status"] = "Failure"
        response['error']  = "Bad authentication"
    if not current_player and  d.check_password(username, password) and status!=0:
        response["status"] = "Failure"
        response['error']  = "Game is not in lobby."
    if not current_player and  not d.check_password(username, password) and status!=0:
        response["status"] = "Failure"
        response['error']  = "Bad authentication and game is not in lobby"

    return jsonify(response)
@app.route('/v1/game/<int:game_id>' , methods = ["PUT"])
def update_game(game_id):
    lat = request.form["lat"]
    lng = request.form['lng']
    auth = request.authorization
    username = auth.username
    password = auth.password
    d.set_location(username, lat, lng)
    nearby = d.get_alive_nearby(username, game_id, 700000)
    response = {}
    # check if ww?
    player_id = d.get_voting_player_id(username, game_id)
    check_werewolf = d.player_type(game_id, player_id)

    if check_werewolf != 0:
        if nearby:
            response['status'] = 'success'
            response['results'] = {}
            response['results']['werewolfscent'] = nearby
        #response['results'] = {} 
        #for row in players_nearby:     
        #for p in nearby:
         #   print "{} is {} meters away".format(p["player_id"],p["distance"])
        #print nearby
    else:
        response['status'] = 'succes (you are not a werewolf)'
    return jsonify(response)
# need to add in time

@app.route('/v1/game/<int:game_id>', methods = ["GET"])
def game_players(game_id):
    auth = request.authorization
    username = auth.username
    password = auth.password 
    players = d.get_playername(game_id)
    response = {}
    response['players']= players
    print response
    return jsonify(response)



@app.route('/v1/game/<int:game_id>', methods = ["GET"])
def game_info(game_id):
    auth = request.authorization
    username = auth.username
    password = auth.password 
    info = d.game_info(game_id)
    response = {}
    response["status"] = info 
    players = d.get_players(game_id)
    response['players']= players
    print response
    return jsonify(response)

@app.route('/v1/game/<int:game_id>/time', methods = ["POST"])
def set_game_time(game_id):
    username = request.form["username"]
    game_time = request.form["game_time"]
    d.set_db_time(game_time, game_id)
    response={}
    response["status"]= "sucess"
    return jsonify(response)

@app.route('/v1/game/<int:game_id>/vote', methods = ["POST"])
def cast_vote(game_id):
    target_id = request.form["target_id"]
    auth = request.authorization
    username = auth.username
    password = auth.password
    current_time = get_time(game_id)
    print isDay(game_id)
    response = {}
    response["error"]  = ""
    player_id = d.get_voting_player_id(username, game_id) 
    if isDay(game_id):
        if player_id and d.check_password(username, password):
            d.vote_new(game_id, player_id, target_id)
            response["status"] = 'success'
        if not player_id and d.check_password(username, password):
            response["status"] = 'Failure'
            response["error"]  = 'Not in the game'
        if player_id  and not d.check_password(username, password):
            response["status"] = 'Failure'
            response["error"]  = 'Bad authentication'
        if not player_id  and not d.check_password(username, password):
            response["status"] = 'Failure'
            response["error"]  = 'Not in the game and bad authentication'
    #if isNight(game_id):
    else:
        response["status"] = 'Failure'
        response["error"]  = 'It is not daytime'
    return jsonify(response)

@app.route('/v1/game/<int:game_id>/ballot', methods = ["GET"])
def get_ballot(game_id):
    auth = request.authorization
    username = auth.username
    password = auth.password
    players = d.get_all_players(game_id)
    tally = []
    for i in players:
        vote = d.get_last_vote(i, game_id)
        tally.append(vote)
    voted_out = max(((item, tally.count(tally)) for item in set(tally)), key=lambda a: a[1])[0]  
    frequency = {i:tally.count(i) for i in set(tally)}
    response ={}
    response["results"] = []
    response["status"] = "success"
    for key in frequency:
        vote ={}
        vote["player_id"] = key
        vote["votes"] = frequency[key]
        response["results"].append(vote)
        response["voted_out"] = voted_out
    return jsonify(response)

@app.route('/v1/game/<int:game_id>/status', methods = ["POST"])
def set_game_status(game_id):
    username = request.form["username"]
    game_status= request.form["game_status"]
    d.set_game_status(username, game_status, game_id)

@app.route('/v1/game/<int:game_id>/werewolf', methods = ["POST"])
def set_werewolf(game_id):
    werewolf_id = request.form["werewolf_id"]
    d.set_werewolf(game_id, werewolf_id)

@app.route('/v1/user', methods = ["GET"])
def get_playerid():
    username = request.form["username"]
    playerid = d.get_current_player(username)
    response = {}
    response['playerid'] = playerid
    return jsonify(response)

@app.route('/v1/game/<int:game_id>/attack',methods=["POST"])
def attack_villager(game_id):
    target_id = request.form['target_id']
    auth = request.authorization
    username = auth.username
    password = auth.password
    response = {}
    response['results'] = {}
    in_game_check = d.in_game_check(username, game_id)
    target_player_type = d.player_type(game_id, target_id)
    w_player_id = d.get_current_player(username)


    if isNight(game_id):
        if in_game_check and target_player_type == 0 and d.check_password(username,password):
            # werewolf stats
            w_hp, w_attack = d.werewolf_stats(game_id, w_player_id)
            # villager stats
            v_hp, v_attack = d.villager_stats(target_id)


            while w_hp >= 0 and v_hp >= 0:
                w_roll = random.randint(0, w_attack)
                v_hp -= w_roll
                v_roll = random.randint(0, v_attack)
                w_hp -= v_roll

                if w_hp <= 0:
                    response['status'] = 'success'
                    response['results']['summary'] = 'death'
                    response['results']['combatant'] = w_player_id
                    #response['summary'] = 'death'
                    #response['combatant'] = w_player_id
                    d.set_dead(username)
                    #w lost
                    
                elif v_hp <= 0:
                    response['status'] = 'success'
                    response['results']['summary'] = 'death'
                    response['results']['combatant'] = target_id
                    #response['summary'] = 'death'
                    #response['combatant'] = target_id
                    v_username = d.get_username1(target_id)
                    d.set_dead(v_username)
                    # v lost
        
        else:
            response['status'] = 'failure'
    else:
        response['status'] = 'failure'

    return jsonify(response)

@app.route('/v1/game/<int:game_id>/vote_death',methods=["POST"])
def set_top_voted_death(game_id):
    player_id = request.form['player_id']
    d.set_dead_pid(player_id)



@app.route('/v1/cleandatabase', methods = ["DELETE"])
def clean_game_data():
    d.clear_tables()
    response= {}
    response["status"] = "success"
    return jsonify(response)


@app.route('/v1/game/<int:game_id>/assign_lupus', methods=["POST"])
def assign_lupus_and_clear_votes_table(game_id):
    death_player_id = request.form["death_player_id"]
    d.clear_vote_table()
    username = d.get_username1(death_player_id)
    d.award_achievement(username, 'It is never Lupus')
        #def award_achievement(self, username, achievementname):

@app.route('/v1/game/<int:game_id>/game_results', methods=["GET"])
def check_game_results(game_id):
    ww_check = d.check_all_ww_dead(game_id)
    v_check = d.check_all_v_dead(game_id)
    response = {}
    if not ww_check:
        # not all ww dead
        response['status'] = 'villagers won'
    if not v_check:
        # not all v dead
        response['status'] = 'werewolves won'

    if ww_check and v_check:
        #neither is dead, continut game
        response['status'] = 'continue'

    return jsonify(response)


# are all ww dead?
##if all ww dead: 'villagers won'
# are all v dead?
##if all v dead: 'werewolves won'
# neither
## continue game


    


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
    






