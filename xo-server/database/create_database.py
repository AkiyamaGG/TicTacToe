import sqlite3

def create_database():
	conn = sqlite3.connect("xo-server/database/database.db")

	cursor = conn.cursor()

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS player (
		uid	TEXT NOT NULL,
		nickname	TEXT NOT NULL UNIQUE,
		elo	INTEGER DEFAULT 0,
		wins	INTEGER DEFAULT 0,
		loses	INTEGER DEFAULT 0,
		matches	INTEGER DEFAULT 0,
		datetime	TEXT NOT NULL,
		status	TEXT DEFAULT "offline",
		PRIMARY KEY(uid));
		''')
	cursor.execute('''
		CREATE TABLE IF NOT EXISTS match (
		mid	TEXT NOT NULL,
		player_1	TEXT NOT NULL,
		player_2	TEXT NOT NULL,
		winner	TEXT DEFAULT "",
		elo_1	INTEGER NOT NULL,
		elo_2	INTEGER NOT NULL,
		start_datetime	TEXT NOT NULL,
		finish_datetime	TEXT NOT NULL,
		PRIMARY KEY(mid),
		FOREIGN KEY(player_1) REFERENCES player(uid),
		FOREIGN KEY(player_2) REFERENCES player(uid),
		FOREIGN KEY(winner) REFERENCES player(uid));
		''')

	conn.commit()
	conn.close()
