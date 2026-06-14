from fastapi import FastAPI, WebSocket
import sqlite3
from routers import player,rating
from database import create_database

create_database.create_database()

app = FastAPI()

conn = sqlite3.connect("xo-server/database/database.db")

cursor = conn.cursor()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    conn = sqlite3.connect("xo-server/database/database.db")

    cursor = conn.cursor()

    EVENT_HANDLER = []

    while True:
        data = await websocket.receive_json()
        try:
            if data["event"] in EVENT_HANDLER:
                if data:
                    pass
                else:
                    print("ERROR:400\nInvalid request")
                    await websocket.send_json({"error": "Invalid request", "type": "400"})

            else:
                print("ERROR:404\nEvent not found")
                print(f"Received data: {data}")
                await websocket.send_json({"error": "Event not found", "type": "404"})
        except:
            await websocket.send_json({"error": "INVALID_VALUE", "type": "404"})

        

app.include_router(player.router)
app.include_router(rating.router)

if __name__ == '__main__':
    pass
