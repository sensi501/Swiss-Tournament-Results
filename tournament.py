#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    # The statement below returns the database connection.
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    # The statments below sets one variable to store the database connection and the second variable to store the database cursor.
    conn = connect()
    dbcursor = conn.cursor()
    
    # The query below deletes all rows from the matches table, commits the changes then closes the connection.
    dbcursor.execute("DELETE FROM matches;")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    # The statments below sets one variable to store the database connection and the second variable to store the database cursor.
    conn = connect()
    dbcursor = conn.cursor()
    
    # The query below deletes all rows from players table, commits the changes then closes the connection.
    dbcursor.execute("DELETE FROM players;")
    conn.commit()
    conn.close()
    
def countPlayers():
    """Returns the number of players currently registered."""
    # The statments below sets one variable to store the database connection and the second variable to store the database cursor.
    conn = connect()
    dbcursor = conn.cursor()
    
    # The query below counts all rows in the players table then stores the results in playercount, 
    # commits the changes, closes the connection then returns the playercount.
    dbcursor.execute("SELECT COUNT (players.id) as num FROM players;")
    playercount = dbcursor.fetchone()
    conn.close()
    return(playercount[0])
    
def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    # The statments below sets one variable to store the database connection and the second variable to store the database cursor.
    conn = connect()
    dbcursor = conn.cursor()
    
    # The query below inserts a new player name in to the players table and sets wins, loses and matches to 0,
    # commits the changes, closes the connection.
    dbcursor.execute("INSERT INTO players (name, wins, loses, matches) VALUES ((%s), 0, 0, 0);", (name,))
    conn.commit()
    conn.close()
    
def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    # The statments below sets one variable to store the database connection and the second variable to store the database cursor.
    conn = connect()
    dbcursor = conn.cursor()
    
    # The query below selects the players id, name, wins, loses, then adds the wins and loses to calculate the match count, all from the players table,
    # stores the results into standings,
    # commits the changes, closes the connection then returns standings.
    dbcursor.execute("SELECT players.id AS id, players.name AS name, players.wins AS wins, players.wins + players.loses AS matches FROM players ORDER BY players.wins DESC;")
    standings = dbcursor.fetchall()
    conn.close()
    return(standings)

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # The statments below sets one variable to store the database connection and the second variable to store the database cursor.
    conn = connect()
    dbcursor = conn.cursor()
    
    # The queries below update the players wins, loses and matches for two player ids specified as arguments in the reportMatch() function.
    dbcursor.execute("UPDATE players SET wins = wins + 1, matches = matches + 1 WHERE id = (%s);", (winner,))
    dbcursor.execute("UPDATE players SET loses = loses + 1, matches = matches + 1 WHERE id = (%s);", (loser,))
    conn.commit()
    
    # The query below selects all rows from the matches table where the specified reportMatch() arguments are listed in columns player1 and player2,
    # the matchcount variable stores the length of the resultant list.
    dbcursor.execute("SELECT * FROM matches WHERE player1 IN (%(w)s, %(l)s) AND player2 IN (%(w)s, %(l)s);", {'w' : (winner,), 'l' : (loser,)})
    matchfound = len(dbcursor.fetchall())
    
    # The statements below executes if matchcount is greater than zero,
    # then updates the matches table values winner and loser columns where both reportMatch() function arguments are present.
    if (matchfound > 0):
        dbcursor.execute("UPDATE matches SET winner = (%(w)s), loser = (%(l)s) WHERE player1 IN ((%(w)s), (%(l)s)) AND player2 IN (%(w)s, %(l)s);", {'w' : (winner,), 'l' : (loser,)})
    
    # The statement below executes if matchcount is not greater than one,
    # then inserts into the match table the winner as player1, loser as player2, winner in to the winner column, and the loser in to the loser column.
    else:
        dbcursor.execute("INSERT INTO matches (player1, player2, winner, loser) VALUES ((%(w)s), (%(l)s), (%(w)s), (%(l)s));", {'w' : (winner,), 'l' : (loser,)})
    
    # The statements below commits the changes then closes the connection.
    conn.commit()
    conn.close()
    
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # The statments below sets one variable to store the database connection and the second variable to store the database cursor.
    conn = connect()
    dbcursor = conn.cursor()
    
    # The query below selects all rows from the matches table,
    # stores the length of the results in the matchcount variable,
    # and sets playercount equal to 0.
    dbcursor.execute("SELECT * FROM matches;")
    matchcount = len(dbcursor.fetchall())
    playercount = 0
    
    # The if statement below checks if matchcount is equal to zero,
    # then uses a query to select all player ids from players, 
    # stores the results in playerlist,
    # and stores the length of playerlist in playercount. 
    if (matchcount == 0):
        dbcursor.execute("SELECT players.id FROM players;")
        playerlist = dbcursor.fetchall()
        playercount = len(playerlist)
        
        # The for statement below starts at 0, stops at the playercount value and steps 2 for each loop iteration,
        # the query below inserts into the matches table the player1 and player 2 values from the playerlist,
        # then commits all changes.
        for x in range(0, playercount, 2):
            dbcursor.execute("INSERT INTO matches (player1, player2) VALUES (%(p1)s, %(p2)s);", {'p1' : playerlist[x], 'p2' : playerlist[x + 1]})
            conn.commit()
        
        # The statements below select all rows from the matches table,
        # stores the length of the results to mactchcount, 
        # and sets player offset equal to 0.
        dbcursor.execute("SELECT * FROM matches;")
        matchcount = len(dbcursor.fetchall())
        playeroffset = 0
    
    # The elif statement below checks if matchcount is greater than zero,
    # uses a query to select all player ids from players, stores the results in playerlist in order of the highest wins 
    # and stores the length of playerlist in playercount. 
    elif (matchcount > 0):        
        dbcursor.execute("SELECT players.id FROM players ORDER BY players.wins DESC;")
        playerlist = dbcursor.fetchall()
        playercount = len(playerlist)
        
        # The for statement below starts at 0, stops at the playercount value and steps 2 for each loop iteration,
        # the query below inserts into the matches table the player1 and player 2 values from the playerlist,
        # then commits all changes.
        for x in range(0, playercount, 2):
            dbcursor.execute("INSERT INTO matches (player1, player2) VALUES (%(p1)s, %(p2)s);", {'p1' : playerlist[x], 'p2' : playerlist[x + 1]})
            conn.commit()
        
        # The statements below select all rows from the matches table, 
        # stores the length of the results to mactchcount, 
        # and sets playeroffset equal to matchcount minus half of player count.
        dbcursor.execute("SELECT * FROM matches;")
        matchcount = len(dbcursor.fetchall())
        playeroffset = matchcount - (playercount / 2)

    # The statements below select the players ids and names from the players table based on the matches table row pairings,
    # and stores the values in player1id, player1name, player2id, and player2name.
    dbcursor.execute("SELECT matches.player1 FROM matches, players WHERE matches.player1 = players.id;")
    player1id = dbcursor.fetchall()
    
    dbcursor.execute("SELECT players.name FROM players, matches WHERE players.id = matches.player1;")
    player1name = dbcursor.fetchall()
    
    dbcursor.execute("SELECT matches.player2 FROM matches, players WHERE matches.player2 = players.id;")
    player2id = dbcursor.fetchall()
    
    dbcursor.execute("SELECT players.name FROM players, matches WHERE players.id = matches.player2;")
    player2name = dbcursor.fetchall()
    
    # The statement below creates a list to store the player and name pairs to play each other in the matches table.        
    swisspairs = []

    # The statements below use a for loop to start at the playeroffset, stop at mactchcount, and step by 1,
    # the following statement adds a new tuple to swisspairs containing the values player1id, player1name, player2id, player2name 
    # using the for loop index x and 0 to return the raw value with out the tuple formatting.
    for x in range(playeroffset, matchcount, 1):
        swisspairs.append((player1id[x][0], player1name[x][0], player2id[x][0], player2name[x][0],))
    
    # The statements below commits the changes, closes the connection then returns the swisspairs.
    conn.commit()
    conn.close()
    return(swisspairs)