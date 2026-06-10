import sqlite3
from sqlite3 import *

conn = sqlite3.connect("database.db")

conn.execute('''
    CREATE TABLE "player" (
	"uid"	TEXT NOT NULL,
	"nickname"	TEXT NOT NULL,
	"elo"	INTEGER DEFAULT 0,
	"wins"	INTEGER DEFAULT 0,
	"loses"	INTEGER DEFAULT 0,
	"matches"	INTEGER DEFAULT 0,
	PRIMARY KEY("uid"));
	''')
conn.execute('''
    CREATE TABLE "match" (
	"mid"	TEXT NOT NULL,
	"player_1"	TEXT NOT NULL,
	"player_2"	TEXT NOT NULL,
	"winner"	TEXT NOT NULL,
	"c_elo"	INTEGER NOT NULL,
	"datetime"	TEXT NOT NULL,
	PRIMARY KEY("mid"),
	FOREIGN KEY("player_1") REFERENCES "player"("uid"),
	FOREIGN KEY("player_2") REFERENCES "player"("uid"),
	FOREIGN KEY("winner") REFERENCES "player"("uid"));
	''')
conn.execute('''
    CREATE TABLE "queue" (
	"uid"	TEXT,
	"elo"	INTEGER NOT NULL,
	FOREIGN KEY("elo") REFERENCES "player"("elo"),
	FOREIGN KEY("uid") REFERENCES "player"("uid"));
	''')

conn.commit()
conn.close()
