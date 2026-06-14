import sqlite3
from sqlite3 import *
from fastapi import *

router = APIRouter(prefix="/rating", tags=["API"])

@router.get("/{type}/")
async def get_rating(type: str, limit: int = 100):
    conn = sqlite3.connect("xo-server/database/database.db")

    cursor = conn.cursor()

    cursor.execute(f'''SELECT nickname, {type}  FROM player ORDER BY ? DESC LIMIT ?''', (type, limit,))
    columns = [col[0] for col in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return results