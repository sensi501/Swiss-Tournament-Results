-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE players (
	id SERIAL PRIMARY KEY, 
	name TEXT NOT NULL,
	wins INTEGER,
	loses INTEGER,
	matches INTEGER
	);

CREATE TABLE matches (
	player1 INTEGER,
	player2 INTEGER REFERENCES players (id),
	winner INTEGER REFERENCES players (id), 
	loser INTEGER
	);