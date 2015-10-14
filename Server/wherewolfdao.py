# Wherewolf game DAO
# Abstraction for the SQL database access.

import psycopg2
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

    def __init__(self, dbname='wherewolf', pgusername='wherewolf', pgpasswd='password'):
        self.dbname = dbname
        self.pgusername = pgusername
        self.pgpasswd = pgpasswd
        self.dbhost = 'wherewolf.cpkl5uywse0b.us-west-2.rds.amazonaws.com'
        print ('connection to database {}, user: {}, password: {}'.format(dbname, pgusername, pgpasswd))

    def get_db(self):
        return psycopg2.connect(host=self.dbhost, database=self.dbname,user=self.pgusername,password=self.pgpasswd)

    def create_user(self, username, password, firstname, lastname):
        """ registers a new player in the system """
        conn = self.get_db()
        with conn:
            c = conn.cursor()
            c.execute('SELECT COUNT(*) from gameuser WHERE username=%s',(username,))
            n = int(c.fetchone()[0])
            # print 'num of rfdickersons is ' + str(n)
            if n == 0:
                hashedpass = md5.new(password).hexdigest()
                c.execute('INSERT INTO gameuser (username, password, firstname, lastname) VALUES (%s,%s,%s,%s)', 
                          (username, hashedpass, firstname, lastname))
                conn.commit()
            else:
                raise UserAlreadyExistsException('{} user already exists'.format((username)) )
        
    def check_password(self, username, password):
        """ return true if password checks out """
        conn = self.get_db()
        with conn:
            c = conn.cursor()
            sql = ('select password from gameuser where username=%s')
            c.execute(sql,(username,))
            hashedpass = md5.new(password).hexdigest()
            u = c.fetchone()
            if u == None:
                raise NoUserExistsException(username)
            # print 'database contains {}, entered password was {}'.format(u[0],hashedpass)
            return u[0] == hashedpass
        
    def set_location(self, username, lat, lng):
        conn = self.get_db()
        with conn:
            cur = conn.cursor()
            sql = ('update player set lat=%s, lng=%s '
                   'where player_id=(select current_player from gameuser '
                   'where username=%s)')
            cur.execute(sql, (lat, lng, username))
            conn.commit()


    def get_location(self, username):
        conn = self.get_db()
        result = {}
        with conn:
            c = conn.cursor()
            sql = ('select player_id, lat, lng from player, gameuser '
                   'where player.player_id = gameuser.current_player '
                   'and gameuser.username=%s')
            c.execute(sql, (username,))
            row = c.fetchone()
            result["playerid"] = row[0]
            result["lat"] = row[1]
            result["lng"] = row[2]
        return result

        
    def get_alive_nearby(self, username, game_id, radius): 
        ''' returns all alive players near a player '''
        conn = self.get_db()
        result = []
        with conn:
            c = conn.cursor()
            sql_location = ('select lat, lng from player, gameuser where '
                           'player.player_id = gameuser.current_player '
                           'and gameuser.username=%s')
            c.execute(sql_location, (username,))
            location = c.fetchone()

            if location == None:
                return result

            # using the radius for lookups now
            sql = ('select player_id, '
                   'earth_distance( ll_to_earth(player.lat, player.lng), '
                   'll_to_earth(%s,%s) ) '
                   'from player where '
                   'earth_box(ll_to_earth(%s,%s),%s) '
                   '@> ll_to_earth(player.lat, player.lng) '
                   'and game_id=%s '
                   'and is_werewolf = 0 '
                   'and is_dead = 0')

            # sql = ('select username, player_id, point( '
            #       '(select lng from player, gameuser '
            #       'where player.player_id=gameuser.current_player '
            #       'and gameuser.username=%s), '
            #       '(select lat from player, gameuser '
            #       'where player.player_id=gameuser.current_player '
            #       'and gameuser.username=%s)) '
            #       '<@> point(lng, lat)::point as distance, '
            #       'is_werewolf '
            #       'from player, gameuser where game_id=%s '
            #       'and is_dead=0 '
            #       'and gameuser.current_player=player.player_id '
            #       'order by distance')
            # print sql

            c.execute(sql, (location[0], location[1], 
                            location[0], location[1], 
                            radius, game_id))
            for row in c.fetchall():
                d = {}
                d["player_id"] = row[0]
                d["distance"] = row[1]
                #d["distance"] = row[1]
                #d["is_werewolf"] = row[2]
                result.append(d)
        return result
                   
        
    def add_item(self, username, itemname):
        conn = self.get_db()
        with conn:
            cur=conn.cursor()

            cmdupdate = ('update inventory set quantity=quantity+1'
                         'where itemid=(select itemid from item where name=%s)' 
                         'and playerid='
                         '(select current_player from gameuser where username=%s);')
            cmd = ('insert into inventory (playerid, itemid, quantity)' 
                   'select (select current_player from gameuser where username=%s) as cplayer,'
                   '(select itemid from item where name=%s) as item,' 
                   '1 where not exists' 
                   '(select 1 from inventory where itemid=(select itemid from item where name=%s)' 
                   'and playerid=(select current_player from gameuser where username=%s))')
            cur.execute(cmdupdate + cmd, (itemname, username, username, itemname, itemname, username))

            conn.commit()

 
    def remove_item(self, username, itemname):
        conn = self.get_db()
        with conn:
            cur = conn.cursor()
            cmd = ('update inventory set quantity=quantity-1 where ' 
                   'itemid=(select itemid from item where name=%s) and ' 
                   'playerid=(select current_player from gameuser where username=%s);')
            cmddelete = ('delete from inventory where itemid=(select itemid from item where name=%s)' 
                         'and playerid=(select current_player from gameuser where username=%s) '
                         'and quantity < 1;')
            cur.execute(cmd + cmddelete, (itemname, username, itemname, username))
            conn.commit()


    def get_items(self, username):
        conn = self.get_db()
        items = []
        with conn:
            c = conn.cursor()
            sql = ('select item.name, item.description, quantity '
                   'from item, inventory, gameuser where '
                   'inventory.itemid = item.itemid and '
                   'gameuser.current_player=inventory.playerid and '
                   'gameuser.username=%s')
            c.execute(sql, (username,))
            for item in c.fetchall():
                d = {}
                d["name"] = item[0]
                d["description"] = item[1]
                d["quantity"] = item[2]
                items.append(d)
        return items

        
    def award_achievement(self, username, achievementname):
        conn = self.get_db()
        with conn:
            cur = conn.cursor()
            cmd = ('insert into user_achievement (user_id, achievement_id, created_at) '
                   'values ((select user_id from gameuser where username=%s), '
                   '(select achievement_id from achievement where name=%s), now());')
            cur.execute(cmd, (username, achievementname))
            conn.commit()

        
    def get_achievements(self, username):
        conn = self.get_db()
        with conn:
            cur = conn.cursor()
            cmd = ('select name, description, created_at from achievement, user_achievement '
                   'where achievement.achievement_id = user_achievement.achievement_id '
                   'and user_achievement.user_id = '
                   '(select user_id from gameuser where username=%s);')
            cur.execute(cmd, (username,))
            achievements = []
            for row in cur.fetchall():
                d = {}
                d["name"] = row[0]
                d["description"] = row[1]
                d["created_at"] = row[2]
                achievements.append(d)
        return achievements

    def set_dead(self, username):
        conn = self.get_db()
        with conn:
            cur = conn.cursor()
            cmd = ('update player set is_dead=1 '
                   'where player_id='
                   '(select current_player from gameuser where username=%s);')
            cur.execute(cmd, (username,))
            conn.commit()

    def set_dead_pid(self, player_id):
        conn = self.get_db()
        with conn:
            cur = conn.cursor()
            cmd = ('update player set is_dead=1 '
                   'where player_id= %s;')
            cur.execute(cmd, (player_id,))
            conn.commit()
    def get_playername(self, gameid):
        conn = self.get_db()
        players = []
        with conn:
            cur = conn.cursor()
            cmd = ('select username from gameuser where current_player = any (select player_id from player where game_id = %s);')
            cur.execute(cmd, (gameid,))
            for row in cur.fetchall():
                P = {}
                P["username"] = row[0]
                players.append(P)
            return players

    def get_players(self, gameid):
        conn = self.get_db()
        players = []
        with conn:
            cur = conn.cursor()
            cmd = ('select player_id, is_dead, lat, lng, is_werewolf from player '
                   ' where game_id=%s;')
            cur.execute(cmd, (gameid,))
            for row in cur.fetchall():
                p = {}
                p["playerid"] = row[0]
                p["is_dead"] = row[1]
                p["lat"] = row[2]
                p["lng"] = row[3]
                p["is_werewolf"] = row[4]
                players.append(p)
        return players

    def get_user_stats(self, username):
        pass
        
        
    def get_player_stats(self, username):
        pass

    # game methods    
    def join_game(self, username, gameid):
        conn = self.get_db()
        with conn:
            cur = conn.cursor()
            cmd = ('INSERT INTO player ( is_dead, lat, lng, game_id) '
                   'VALUES ( %s, %s, %s, %s) returning player_id')
            cmd2 = ('update gameuser set current_player=%s where username=%s')
            cur.execute(cmd,( 0, 0, 0, gameid))
            cur.execute(cmd2, (cur.fetchone()[0], username));
            conn.commit()
    
    def leave_game(self, username):
        conn = self.get_db()
        with conn:
            cur = conn.cursor()
            cmd1 = '''UPDATE gameuser set current_player = null where username=%s'''
            cur.execute(cmd1, (username,)) 
            conn.commit()
        
        
    def create_game(self, username, gamename, description):
        ''' returns the game id for that game '''
        conn = self.get_db()
        with conn:
            cur = conn.cursor()
            cmd = ('INSERT INTO game (admin_id, name, description) VALUES ( '
                   '(SELECT user_id FROM gameuser where username=%s), '
                   '%s, %s) returning game_id')
            cur.execute(cmd,(username, gamename, description))
            game_id = cur.fetchone()[0]
            conn.commit()
            return game_id


    def game_info(self, game_id):
        conn = self.get_db()
        with conn:
            cur = conn.cursor()
            cmd = '''SELECT game_id, admin_id, status, name from game where game_id=%s'''
            cur.execute(cmd, (game_id,))
            row = cur.fetchone()
            d = {}
            d["game_id"] = row[0]
            d["admin_id"] = row[1]
            d["status"] = row[2]
            d["name"] = row[3]
            #d["current_time"] = row[4]
            return d

    def get_games(self):
        conn = self.get_db()
        games = []
        with conn:
            cur = conn.cursor()
            cmd = ('SELECT game_id, name, description, status from game')
            cur.execute(cmd)
            for row in cur.fetchall():
                d = {}
                d["game_id"] = row[0]
                d["name"] = row[1]
                d["description"] = row[2]
                d["status"] = row[3]
                games.append(d)
            return games

            
    def set_game_status(self, username, game_status, game_id):
        conn = self.get_db()
        with conn:
            cur = conn.cursor()
            cmd = ('UPDATE game set status = %s where game_id = %s')
            cur.execute(cmd, (game_status, game_id))
            conn.commit()
        
    
    def vote(self, game_id, player_id, target_id):
        conn = self.get_db()
        with conn:
            cur = conn.cursor()
            sql = ('insert into vote '
                   '(game_id, player_id, target_id, cast_date) '
                   'values ( %s,'
                   '(select current_player from gameuser where username=%s), '
                   '(select current_player from gameuser where username=%s), '
                   'now())')
            cur.execute(sql, (game_id, player_id, target_id))
            conn.commit()
    
    def vote_new(self, game_id, player_id, target_id):
        conn = self.get_db()
        with conn:
            cur = conn.cursor()
            sql = ('insert into vote '
                   '(game_id, player_id, target_id, cast_date) '
                   'values ( %s, %s, %s, '
                   'now())')
            cur.execute(sql, (game_id, player_id, target_id))
            conn.commit()
    
    def get_username(self, username):
        conn = self.get_db()
        with conn:
            cur = conn.cursor()
            sql = ('select username from gameuser '
                'where username=%s')
            cur.execute(sql, (username,))
            user = cur.fetchone()
            return user 

   
    def get_admin_id(self, username):
        conn = self.get_db()
        with conn:
            cur = conn.cursor()
            sql = ('select admin_id from game '
                'where admin_id =(select user_id from gameuser where username = %s)')
            cur.execute(sql, (username,))
            admin_id = cur.fetchone()
            return admin_id

    def get_admin_game(self, game_id, username):
        conn = self.get_db()
        cur = conn.cursor()
        sql = ('select admin_id from game '
                'where game_id = %s and admin_id= (select user_id from gameuser where username = %s)')
        cur.execute(sql, (game_id, username))
        admin_id = cur.fetchone()
        return admin_id

    def delete_game_as_admin(self, game_id, admin_id):
        conn = self.get_db()
        with conn:
            cur   = conn.cursor()
            sql   = ('DELETE from inventory where playerid = ANY (select player_id from player where game_id = %s)')
           #sql_1 = ('DELETE from player_stat where player_id = ANY (select player_id from player where game_id = %s)')
            sql_2 = ('DELETE from vote where player_id = ANY (select player_id from player where game_id = %s)')
            sql_3 = ('DELETE from player where player_id = ANY (select player_id from player where game_id = %s)')
            sql_4 = ('DELETE  FROM game WHERE admin_id = %s')
            sql_5 = ('UPDATE gameuser set current_player = null where current_player = ANY ( select player_id from player where game_id = %s)')
            cur.execute(sql, (game_id,))
           # cur.execute(sql_1, (game_id,))
            cur.execute(sql_5, (game_id,))
            cur.execute(sql_2, (game_id,))
            cur.execute(sql_3, (game_id,))
            cur.execute(sql_4, (admin_id,))
            conn.commit()

    def delete_player(self, game_id, username):
        conn = self.get_db()
        cur = conn.cursor()
        sql = ('DELETE FROM player WHERE game_id =%s and player_id = (select current_player from gameuser where username = %s)')
        cur.execute(sql, (game_id, username))
        conn.commit()


    def get_player_id_game(self, username, game_id): 
        conn = self.get_db()
        with conn:
            cur = conn.cursor()
            sql = ('select current_player from gameuser where username = %s')
            cur.execute(sql, (username,))
            player_id = cur.fetchone()
            print player_id
            cur1 = conn.cursor()
            sql_1 = ('select player_id from player where game_id = %s and player_id = %s')
            cur1.execute(sql_1, (game_id, player_id))
            checked_pid = cur1.fetchone()
            print checked_pid
            return checked_pid

    def get_current_player(self, username):
        conn = self.get_db()
        with conn:
            cur = conn.cursor()
            sql = ('select current_player from gameuser where username = %s')
            cur.execute(sql, (username,))
            current_player = cur.fetchone()[0]
            return current_player 

    def get_db_time(self, game_id):
        conn = self.get_db()
        with conn:
            cur = conn.cursor()
            sql = ("select to_char(currenttime, 'HH24:MI:SS') from game where game_id = %s")
            cur.execute(sql, (game_id,))
            db_time = cur.fetchone()[0]       
            return db_time
    def set_db_time(self, game_time, game_id):
        conn = self.get_db()
        with conn:
            cur = conn.cursor()
            sql = ("UPDATE game set currenttime = to_timestamp(%s, 'HH24.MI.SS') where game_id = %s")
            cur.execute(sql, (game_time, game_id))
            conn.commit()
    def get_voting_player_id(self, username, game_id):
        conn = self.get_db()
        with conn:
            cur = conn.cursor()
            sql = ('select player_id from player where player_id = (select current_player from gameuser where username = %s)'
                        ' and game_id = %s')
            cur.execute(sql, (username, game_id))
            voting_id = cur.fetchone()
            return voting_id

    def get_all_players(self, game_id):       
        conn = self.get_db()
        cur = conn.cursor()
        sql = ("select username from gameuser where current_player = ANY "
                    '(select player_id from player where game_id = %s)')
        cur.execute(sql, (game_id,))
        players = []
        for i in cur.fetchall():
                players.append(i[0])
        return players
    def get_last_vote(self, username, game_id):
        conn = self.get_db()
        with conn:
            cur = conn.cursor()
            max_vote_id = ('select max(vote_id) from vote where game_id=%s and player_id = (select current_player from gameuser where username = %s)')
            cur.execute(max_vote_id, (game_id, username))
            last_vote_id = cur.fetchone()[0]
            last_vote_sql = ('select target_id from vote where vote_id = %s')
            cur.execute(last_vote_sql, (last_vote_id,))                
            last_vote = cur.fetchone()
            return last_vote

    def set_werewolf(self, game_id, werewolf_id):
        conn = self.get_db()
        with conn:
            cur = conn.cursor()
            sql = ("UPDATE player set is_werewolf = 1 where game_id = %s and player_id = %s")
            cur.execute(sql, (game_id, werewolf_id))
            conn.commit()               

    def in_game_check(self, username, game_id):
        conn = self.get_db()
        with conn:
            c = conn.cursor()
            sql = ('select player_id from player where player_id = (select current_player from gameuser where \
                        username=%s) and game_id=%s')
            c.execute(sql, (username, game_id))
            in_game_check = c.fetchone()
            return in_game_check

    def player_type(self, game_id, target_id):
        conn = self.get_db()
        with conn:
            cur = conn.cursor()
            cmd = ('select is_werewolf from player where game_id = %s and player_id = %s')
            cur.execute(cmd, (game_id, target_id))
            player_type = cur.fetchone()[0]
            return player_type
            
    def villager_stats(self, target_id):
        hp = 10
        attack = 1
        conn = self.get_db()
        with conn:
            cur = conn.cursor()
            cmd = ('select itemid, quantity from inventory where playerid = %s')
            cur.execute(cmd, (target_id,))
            villager_stats = cur.fetchall()
            for i in villager_stats:
                item = i[0]
                quantity = i[1]
                if item == 0:
                    hp += (0*quantity)
                if item == 1:
                    hp += (1*quantity)
                if item == 2:
                    hp += (2*quantity)
                if item == 3:
                    hp += (3*quantity)
                if item == 4:
                    attack += (0*quantity)
                if item == 5:
                    attack += (3*quantity)
                if item == 6:
                    attack += (6*quantity)
                if item == 7:
                    attack += (10*quantity)
            return hp, attack

    def werewolf_stats(self,game_id, username):
        werewolf_stats = self.player_type(game_id, username)
        hp = 0
        attack = 0
        if werewolf_stats == 1:
            hp = 10
            attack = 3
        if werewolf_stats == 2:
            hp = 15
            attack = 5
        if werewolf_stats == 3:
            hp = 20
            attack = 8
        return hp, attack

    def get_username1(self, player_id):
        conn = self.get_db()
        with conn:
            cur = conn.cursor()
            sql = ('select username from gameuser '
                'where current_player=%s')
            cur.execute(sql, (player_id,))
            user = cur.fetchone()
            return user

    def clear_tables(self):
        conn = self.get_db()
        with conn:
            c = conn.cursor()
            c.execute('truncate gameuser cascade')
            c.execute('truncate player cascade')
            c.execute('truncate user_achievement cascade')
            conn.commit()
            
    def clear_vote_table(self):
        conn = self.get_db()
        with conn:
            c = conn.cursor()
            c.execute('truncate vote')
            conn.commit()

    def check_all_ww_dead(self, game_id):
        conn = self.get_db()
        with conn:
            cur = conn.cursor()
            sql = ('select player_id from player where game_id=%s and is_werewolf<>0 and is_dead=0')
            cur.execute(sql, (game_id,))
            alive_ww = cur.fetchall()
            return alive_ww
            
    def check_all_v_dead(self, game_id):
        conn = self.get_db()
        with conn:
            cur = conn.cursor()
            sql = ('select player_id from player where game_id=%s and is_werewolf=0 and is_dead=0')
            cur.execute(sql, (game_id,))
            alive_v = cur.fetchall()
            return alive_v

    
if __name__ == "__main__":
    #dao = WherewolfDao('wherewolf','postgres','psql4me')
    dao = WherewolfDao()
    
    dao.clear_tables()
    
    try:
        dao.create_user('rfdickerson', 'awesome', 'Robert', 'Dickerson')
        dao.create_user('oliver','furry','Oliver','Cat')
        dao.create_user('vanhelsing', 'van', 'Van', 'Helsing')
        print 'Created a new player!'
    except UserAlreadyExistsException as e:
        print e
    except Exception:
        print 'General error happened'
        
    username = 'rfdickerson'
    correct_pass = 'awesome'
    incorrect_pass = 'scaley'
    print 'Logging in {} with {}'.format(username, correct_pass)
    print 'Result: {} '.format( dao.check_password(username, correct_pass ))
    
    print 'Logging in {} with {}'.format(username, incorrect_pass)
    print 'Result: {} '.format( dao.check_password(username, incorrect_pass ))

    game_id = dao.create_game('rfdickerson', 'TheGame', 'Test')
    # dao.create_game('oliver', 'AnotherGame')
    
    dao.join_game('oliver', game_id)
    dao.join_game('rfdickerson', game_id)
    dao.join_game('vanhelsing', game_id)

    print "Adding some items..."
    dao.add_item('rfdickerson', 'Silver Knife')
    dao.add_item('rfdickerson', 'Blunderbuss')
    dao.add_item('rfdickerson', 'Blunderbuss')
    dao.add_item('rfdickerson', 'Blunderbuss')
    dao.add_item('oliver', 'Blunderbuss')
    dao.remove_item('rfdickerson', 'Blunderbuss')

    print
    print 'rfdickerson items'
    print '--------------------------------'
    items = dao.get_items("rfdickerson")
    for item in items:
        print item["name"] + "\t" + str(item["quantity"])
    print

    # location stuff
    dao.set_location('rfdickerson', 30.202, 97.702)
    dao.set_location('oliver', 30.201, 97.701)
    dao.set_location('vanhelsing', 30.2, 97.7) 
    loc = dao.get_location('rfdickerson')
    loc2 = dao.get_location('oliver')
    print "rfdickerson at {}, {}".format(loc["lat"], loc["lng"]) 
    print "oliver at {}, {}".format(loc2["lat"], loc2["lng"]) 

    dao.award_achievement('rfdickerson', 'Children of the moon')
    dao.award_achievement('rfdickerson', 'A hairy situation')
    achievements = dao.get_achievements("rfdickerson")

    print
    print 'rfdickerson\'s achievements'
    print '--------------------------------'
    for a in achievements:
        print "{} ({}) - {}".format(a["name"],a["description"],a["created_at"].strftime('%a, %H:%M'))
    print
    
    nearby = dao.get_alive_nearby('rfdickerson', game_id, 700000)
    print ('Nearby players: ')
    print nearby
    for p in nearby:
        print "{} is {} meters away".format(p["player_id"],p["distance"])

    
    dao.vote(game_id, 'rfdickerson', 'oliver')
    dao.vote(game_id, 'oliver', 'vanhelsing')
    dao.vote(game_id, 'vanhelsing', 'oliver')
    # print 'Players in game 1 are'
    # print dao.get_players(1)
    
    dao.set_dead('rfdickerson')
    