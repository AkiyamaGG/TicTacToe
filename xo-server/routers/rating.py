import sqlite3
from sqlite3 import *
from fastapi import APIRouter
from pathlib import Path
from sys import argv

router = APIRouter(prefix="/rating", tags=["API"])

@router.get("/{type}/")
async def get_rating(type: str, limit: int = 100):
    script_dir = Path(argv[0]).parent.resolve()  # путь к каталогу скрипта
    db_path = script_dir / 'database' / 'database.db'
    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    cursor.execute(f'''SELECT nickname, {type}  FROM player ORDER BY ? DESC LIMIT ?''', (type, limit,))
    columns = [col[0] for col in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    if type == "elo":
        for x in range(len(results)):
            results[x]["elo"] = round(results[x]["elo"]+0.0000001)
    conn.close()
    return results