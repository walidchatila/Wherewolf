# Wherewolf game DAO
# Abstraction for the SQL database access.

import sqlite3
import md5


class UserAlreadyExistsException(Exception):
    def __init__(self, err):
        self.err = err
    def __str__(self):
        return 'Exception: ' + self.err
        
class NoUserExistsException(Exception):
    def __init__(self, err):
        self.err = err
    def __str__(self):
        return 'Exception: ' + self.err
        
class BadArgumentsException(Exception):
    """Exception for entering bad arguments"""
    def __init__(self, err):
        self.err = err
    def __str__(self):
        return 'Exception: ' + self.err
 
class WherewolfDao:

    def __init__(self, dbname):
        print 'Created the DAO'
        self.dbname = dbname
        self.conn = sqlite3.connect('C:\Users\User\Documents\WhereWolf\Server\Wherewolf.db')

    def create_player(self, username, password, firstname, lastname):
        """ registers a new player in the system """
        conn = sqlite3.connect(self.dbname)
        with conn:
            c = self.conn.cursor()
            c.execute('SELECT COUNT(*) from user WHERE username=?',(username,))
            n = int(c.fetchone()[0])
            print 'num of rfdickersons is ' + str(n)
            if n == 0:
                hashedpass = md5.new(password).hexdigest()
                c.execute('INSERT INTO user (username, password, firstname, lastname) VALUES (?,?,?,?)', (username, hashedpass, firstname, lastname))
                self.conn.commit()
            else:
                raise UserAlreadyExistsException('{} user already exists'.format((username)) )
        
    def checkpassword(self, username, password):
        """ return true if password checks out """
        conn = sqlite3.connect(self.dbname)
        with conn:
            c = self.conn.cursor()
            results = c.execute('SELECT password FROM user WHERE username=?',(username,))
            hashedpass = md5.new(password).hexdigest()
            return results.fetchone()[0] == hashedpass
            
        
    def set_location(self, username, lat, lng):
        conn = sqlite3.connect(self.dbname)
        with conn:
            c = self.conn.cursor()
            c.execute('UPDATE player SET lat = ?, lng = ? WHERE playerid in (SELECT playerid FROM player join user WHERE player.userid = user.userid and user.username = ?)', (lat, lng, username))
            self.conn.commit()
   
    def get_location(self, username):
        conn = sqlite3.connect(self.dbname)
        with conn:
            c = self.conn.cursor()
            c.execute('SELECT lat, lng from player join user where user.userid = player.userid and user.username = ?', (username,))
            n = c.fetchall()
        location = []
        for row in n:
            lat = row[0]
            lng = row[1]
            d = {}
            d['lat']=lat
            d['lng']=lng
            location.append(d)
        return location
        
    def get_alive_nearby(self, username, gameid):
        """ returns a list of players nearby """
        conn = sqlite3.connect(self.dbname)
        with conn:
            c = self.conn.cursor()
            c.execute('SELECT lat FROM player JOIN user ON (user.userid=player.userid and username=?)',(username,))
            lat = c.fetchone()[0]
            c.execute('SELECT lng FROM player JOIN user ON (user.userid=player.userid and username=?)',(username,))
            lng = c.fetchone()[0]
            c.execute('SELECT (lat-?)*(lat-?)+(lng-?)*(lng-?) as distance, playerid, lat, lng FROM player JOIN user ON (user.userid=player.userid) WHERE player.is_dead=0 and player.game_id=? ORDER BY distance',(lat,lat,lng,lng, gameid))
            loc = c.fetchall()      
        nearby = []
        for row in loc:
            d = {}
            d['playerid']=row[1]
            d['lat']=row[2]
            d['lng']=row[3]
            nearby.append(d)
        return nearby
                
    def add_item(self, username, itemname):
        """ adds a relationship to inventory and or increments quantity by 1"""
        conn = sqlite3.connect(self.dbname)
        with conn:
            c = self.conn.cursor()
            c.execute('SELECT playerid FROM player join user where player.userid = user.userid and user.username = ?', (username,))
            temp_uid = c.fetchone()[0]
            c.execute('SELECT itemid FROM item where name = ?', (itemname,))
            temp_iid = c.fetchone()[0]
            c.execute('INSERT OR IGNORE INTO  inventory (playerid, itemid, quantity) VALUES(?, ? , 0)', (temp_uid, temp_iid))
            self.conn.commit()
            c.execute('UPDATE inventory set quantity = quantity + 1 where itemid = ? and playerid = ?', (temp_iid, temp_uid))
            self.conn.commit()

        
    def get_items(self, username):
        """ get a list of items the user has"""
        conn = sqlite3.connect(self.dbname)
        with conn:
            c = self.conn.cursor()
            c.execute( 'select name,description,inventory.quantity from item join user,player,inventory where user.userid=player.userid and player.playerid=inventory.playerid and inventory.itemid= item.itemid and username=?',(username,)) 
            n= c.fetchall()
        items = []
        for row in n:
            d = {}
            d['name']=row[0]
            d['description']=row[1]
            d['quantity']=row[2]
            items.append(d)
        return items
        
    def award_achievement(self, username, achievementname):
        """ award an achievement to the user """
        conn = sqlite3.connect(self.dbname)
        with conn:
            c = self.conn.cursor()
            c.execute('SELECT userid FROM user where username = ?', (username,))
            temp_uid = c.fetchone()[0]
            c.execute('SELECT achievementid FROM achievement where name = ?', (achievementname,))
            temp_aid = c.fetchone()[0]
            c.execute('INSERT OR IGNORE INTO  user_achievement (userid, achievementid) VALUES(?, ? )', (temp_uid, temp_aid))
            self.conn.commit()
        
    def get_achievements(self, username):
        """ return a list of achievements for the user """
        conn = sqlite3.connect(self.dbname)
        with conn:
            c = self.conn.cursor()
            c.execute('SELECT name, description FROM achievement join user_achievement, user where user.userid = user_achievement.userid and achievement.achievementid = user_achievement.achievementid and  user.username = ? ORDER BY user_achievement.created_at DESC LIMIT 10' ,(username,))
            n = (c.fetchall()) 
        achievements = []
        for row in n:
            d = {}
            d['name']=row[0]
            d['description']=row[1]
            achievements.append(d)
        return achievements
              
        
        
    def set_dead(self, username):
         """ set a player as dead """
         conn = sqlite3.connect(self.dbname)
         with conn:
            c = self.conn.cursor()
            c.execute('UPDATE player set is_dead = 1 where playerid in (select playerid from player join user where user.userid = player.userid and user.username = ?)' ,(username,))
            self.conn.commit()


    def get_players(self, gamename):
        """ get information about all the players currently in the game """
        conn = sqlite3.connect(self.dbname)
        with conn:
            c = self.conn.cursor()
            c.execute('Select * from player join game WHERE player.game_id = game.gameid and name = ?', (gamename,))
            n = (c.fetchall())
        players = []
        for i in n:
            players.append(list(i))
        return players
        
        
    def get_user_stats(self, username):
        """ return a list of all stats for the user """
        conn = sqlite3.connect(self.dbname)
        with conn:
            c = self.conn.cursor()
            c.execute('SELECT statName from user_stat join user where user_stat.userid = user.userid and user.username = ?',(username,))
            n = (c.fetchone())
            stat = n[0]
        return stat

        
    def get_player_stats(self, username):
        """ return a list of all stats for the player """
        conn = sqlite3.connect(self.dbname)
        with conn:
            c = self.conn.cursor()
            c.execute('SELECT numKills from player_stat join user, player WHERE player_stat.playerid = player.playerid and player.userid = user.userid and user.username = ?',(username,)) 
        n = c.fetchone()
        kills = int(n[0])
        return kills
        
    # game methods    
    def join_game(self, username, gameid):
        """ makes a player for a user. adds player to a game """
        conn = sqlite3.connect(self.dbname)
        with conn:
            c = self.conn.cursor()
            c.execute('SELECT userid from user where username = ?', (username,))
            temp_uid = c.fetchone()[0]
            c.execute('INSERT INTO player(userid, is_dead, lat, lng, game_id) VALUES(?, 1, 0, 0, ?)', (temp_uid, gameid))
            self.conn.commit()
        
    
    def leave_game(self, username):
        """ deletes player for user. removes player from game"""
        conn = sqlite3.connect(self.dbname)
        with conn:
            c = self.conn.cursor()
            c.execute('SELECT playerid from player join user where player.userid = user.userid and username = ?', (username,))
            temp_pid = c.fetchone()[0]
            c.execute('DELETE FROM player where playerid = ?', (temp_pid,)) 
            self.conn.commit()
        
    def create_game(self, username,gamename):
        """ creates a new game """
        conn = sqlite3.connect(self.dbname)
        with conn:
            c = self.conn.cursor()
            c.execute('SELECT userid from user where username = ?', (username,))
            temp_uid = c.fetchone()[0] 
            c.execute('INSERT INTO game (adminid, name) VALUES(?, ?)', (temp_uid, gamename))
            self.conn.commit()
            
            
    def start_game(self, gameid):
        """ set the game as started """
        conn = sqlite3.connect(self.dbname)
        with conn:
            c = self.conn.cursor()
            c.execute('UPDATE game set status = 1 where gameid = ?', (gameid,))
            self.conn.commit()

        
    def end_game(self, gameid):
        """ delete all players in the game, set game as completed (complete is 1)"""
        conn = sqlite3.connect(self.dbname)
        with conn:
            c = self.conn.cursor()
            c.execute('UPDATE game set status = 2 where gameid = ?', (gameid,))
            self.conn.commit()
            c.execute('DELETE FROM player where game_id = ?', (gameid,))
            self.conn.commit()
    
       
if __name__ == "__main__":
    dao = WherewolfDao('Wherewolf.db')
    try:
        dao.create_player('rfdickerson', 'furry', 'Robert', 'Dickerson')
        print 'Created a new player!'
    except UserAlreadyExistsException as e:
        print e
    except Exception:
        print 'General error happened'
        
    username = 'rfdickerson'
    correct_pass = 'furry'
    incorrect_pass = 'scaley'
    print 'Logging in {} with {}'.format(username, correct_pass)
    print 'Result: {} '.format( dao.checkpassword(username, correct_pass ))
    
    print 'Logging in {} with {}'.format(username, incorrect_pass)
    print 'Result: {} '.format( dao.checkpassword(username, incorrect_pass ))
    
   
    
    