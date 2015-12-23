Swiss Tournament Application
by: Jamal Pilgrim

Readme
    To successfully run this application you will need to: 
        
    Installation
    
    -   Install Python 2.7.10 or later from the python website below
		https://www.python.org/downloads/release/python-2710/ 
		also select the version that matches your operating system
		
    -   Install Vagrant virtual machine from http://vagrantup.com/
        
    -   Install Virtual Box from https://www.virtualbox.org/
		
    -   For instructions on installing git go to http://www.git-scm.com/book/en/v2/Getting-Started-Installing-Git
        
    -   Sign up to or login to github.com then, fork the repository from http://github.com/udacity/fullstack-nanodegree-vm
        
    -   Clone your forked repository from github.com to your local machine using git bash or terminal or command line
        
    -   Navigate to /vagrant/tournament within the locally cloned repository
    
    -   Copy the files of this projects folder to /vagrant/tournament
    
    
    Virtual Machine startup
    
    -   Navigate to /vagrant and input: 'vagrant up' then 'vagrant ssh'
    
    -   Navigate to /vagrant/tournament 
    
    Tournament Database Setup
    
    -   Input: 'psql' to start postgresql, '\i tournament.sql' to set database schema then '\q' to exit postgresql
    
    Application Startup
    
    -   Input: 'python tournament_test.py' to run test cases
    OR
    -   Input: 'python' then 'from tournament import *' to use tournament.py script functions
    OR
    -   Add the tournament.py file to a project and add the lines: 'import tournament' or 'from tournament import *' to a python file to be executed
    
    Tournament.py Functions
    
        -   Their are several functions to use: 
            -   connect() to connect to the tournament database
            -   deleteMatches() to delete all rows from the matches table
            -   deletePlayers() to delete all rows from the players table
            -   countPlayers() to count all players in the players table
            -   registerPlayer(name) to add a new player taking an argument for the name to players table and set wins, loses, and matches to 0
            -   playerStandings() to list the players ids, names, wins, loses and matches from the players table
            -   reportMatch(winner, loser) updates the matches and players statistics in the players and matches table based on the winner id and loser id arguments
            -   swissPairings() generates new player match pairs based on player wins and loses
    
Contact
		email address:	sensi501@gmail.com