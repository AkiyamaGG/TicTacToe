from fastapi import FastAPI
from routers import player,rating,match
from database import create_database

create_database.create_database()

app = FastAPI()

app.include_router(match.router)
app.include_router(player.router)
app.include_router(rating.router)

if __name__ == '__main__':
    pass
