import datetime, uuid
import sqlite3
from fastapi import APIRouter
from pydantic import BaseModel
from pathlib import Path
from sys import argv

router = APIRouter(prefix="/player", tags=["API"])


class UserCreate(BaseModel):
    nickname: str


class UserStatus(BaseModel):
    status: str

@router.post("/create/")
async def create_player(username: UserCreate):
    script_dir = Path(argv[0]).parent.resolve()  # путь к каталогу скрипта
    db_path = script_dir / 'database' / 'database.db'
    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    dt = str(datetime.datetime.now())
    generated_id = str(uuid.uuid4())
    cursor.execute('''INSERT OR IGNORE INTO player (uid,nickname,datetime) VALUES (?,?,?)''',
                   (generated_id, username.nickname, dt,))
    conn.commit()
    conn.close()
    return {"uid": generated_id, "nickname": username.nickname, "datetime": dt}


@router.get("/info/uid/{user_id}")
async def get_player_info_for_id(user_id: str):
    script_dir = Path(argv[0]).parent.resolve()  # путь к каталогу скрипта
    db_path = script_dir / 'database' / 'database.db'
    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM player WHERE uid = ?''', (user_id,))
    r = cursor.fetchone()
    conn.close()
    return {"uid": r[0], "nickname": r[1],
            "elo": round(r[2]+0.0000001), "wins": r[3], "loses": r[4],
            "matches": r[5], "datetime": r[6], "status": r[7]}


@router.get("/info/nickname/{username}")
async def get_player_info_for_username(username: str):
    script_dir = Path(argv[0]).parent.resolve()  # путь к каталогу скрипта
    db_path = script_dir / 'database' / 'database.db'
    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM player WHERE nickname = ?''', (username,))
    r = cursor.fetchone()
    conn.close()
    return {"uid": r[0], "nickname": r[1],
            "elo": round(r[2]+0.0000001), "wins": r[3], "loses": r[4],
            "matches": r[5], "datetime": r[6], "status": r[7]}


@router.get("/status/uid/{user_id}")
async def get_player_status(user_id: str):
    script_dir = Path(argv[0]).parent.resolve()  # путь к каталогу скрипта
    db_path = script_dir / 'database' / 'database.db'
    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    cursor.execute('''SELECT status FROM player WHERE uid = ?''', (user_id,))
    r = cursor.fetchone()
    conn.close()
    return {"uid": user_id, "status": r[0]}


@router.post("/status/uid/update/{user_id}")
async def update_player_status(user_id: str, user_status: UserStatus):
    script_dir = Path(argv[0]).parent.resolve()  # путь к каталогу скрипта
    db_path = script_dir / 'database' / 'database.db'
    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    cursor.execute('''UPDATE player SET status = ? WHERE uid = ?''', (user_status.status, user_id,))
    conn.commit()
    conn.close()
    return {"uid": user_id, "status": user_status.status}