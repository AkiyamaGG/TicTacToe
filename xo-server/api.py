import sqlite3
from sqlite3 import *
from fastapi import *
from pydantic import BaseModel
import uuid

app = FastAPI()

class UserCreate(BaseModel):
    nickname: str

class UserStatus(BaseModel):
    status: str


@app.get("/player/info/uid/{user_id}")
async def get_player_id(user_id: str):
    conn = sqlite3.connect("xo-server/database.db")

    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM player WHERE uid = ?''', (user_id,))
    r = cursor.fetchone()
    conn.close()
    return {"uid": r[0], "nickname": r[1],
            "elo": r[2], "wins": r[3], "loses": r[4],
            "matches": r[5]}


@app.get("/player/info/nickname/{username}")
async def get_player_username(username: str):
    conn = sqlite3.connect("xo-server/database.db")

    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM player WHERE nickname = ?''', (username,))
    r = cursor.fetchone()
    conn.close()
    return {"uid": r[0], "nickname": r[1],
            "elo": r[2], "wins": r[3], "loses": r[4],
            "matches": r[5]}

@app.get("/player/status/uid/{user_id}")
async def get_player_status(user_id: str):
    conn = sqlite3.connect("xo-server/database.db")

    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM player WHERE user_id = ?''', (user_id,))
    r = cursor.fetchone()
    conn.close()
    return {"uid": user_id, "status": r[6]}

@app.put("/player/status/uid/{user_id}")
async def put_player_status(user_id: str, userstatus: UserStatus):
    conn = sqlite3.connect("xo-server/database.db")

    cursor = conn.cursor()

    cursor.execute('''UPDATE player SET status = ? WHERE user_id = ?''', (userstatus, user_id,))
    conn.close()
    return {"uid": user_id, "status": userstatus.status}

@app.get("/player/online")
async def get_player_online():
    conn = sqlite3.connect("xo-server/database.db")

    cursor = conn.cursor()

    cursor.execute('''SELECT COUNT(*) FROM player WHERE status = "online"''')
    conn.close()

@app.get("/rating/elo")
async def get_rating_elo():
    conn = sqlite3.connect("xo-server/database.db")

    cursor = conn.cursor()

    cursor.execute('''SELECT nickname, elo FROM player ORDER BY elo DESC LIMIT 100''')
    columns = [col[0]for col in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return results

@app.get("/rating/wins")
async def get_rating_wins():
    conn = sqlite3.connect("xo-server/database.db")

    cursor = conn.cursor()

    cursor.execute('''SELECT nickname, wins FROM player ORDER BY wins DESC LIMIT 100''')
    columns = [col[0]for col in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return results

@app.get("/rating/loses")
async def get_rating_loses():
    conn = sqlite3.connect("xo-server/database.db")

    cursor = conn.cursor()

    cursor.execute('''SELECT nickname, loses FROM player ORDER BY loses DESC LIMIT 100''')
    columns = [col[0]for col in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return results

@app.get("/rating/matches")
async def get_rating_matches():
    conn = sqlite3.connect("xo-server/database.db")

    cursor = conn.cursor()

    cursor.execute('''SELECT nickname, matches FROM player ORDER BY matches DESC LIMIT 100''')
    columns = [col[0]for col in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return results

@app.post("/player/create/")
async def create_player(username: UserCreate):
    conn = sqlite3.connect("xo-server/database.db")

    cursor = conn.cursor()

    generated_id = str(uuid.uuid4())
    cursor.execute('''INSERT OR IGNORE INTO player (uid,nickname) VALUES (?,?)''', (generated_id, username.nickname,))
    conn.commit()
    conn.close()
    return {"uid": generated_id, "nickname": username.nickname}
