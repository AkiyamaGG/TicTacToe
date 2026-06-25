from fastapi import WebSocket, APIRouter, WebSocketDisconnect
import datetime
import sqlite3,random
from pathlib import Path
from sys import argv

router = APIRouter(prefix="/match", tags=["API"])

MATCHES = []                # список словарей матчей
ACTIVE_CONNECTIONS = {}     # uid → WebSocket
QUEUE = []                 # uid ожидающих игроков
ROOMS = {}                  # match_id → set(WebSocket)

EVENT_HANDLER = ['start', 'cancel', 'move', 'close_match']

@router.get("/info/{m_id}")
async def get_match_info(m_id: str):
    script_dir = Path(argv[0]).parent.resolve()  # путь к каталогу скрипта
    db_path = script_dir / 'database' / 'database.db'
    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM match WHERE mid = ?''', (m_id,))
    r = cursor.fetchone()
    conn.close()
    return {"mid": r[0], "player_1": r[1],
            "player_2": r[2], "winner": r[3], "elo_1": r[4],
            "elo_2": r[5], "start_datetime": r[6], "finish_datetime": r[7]}
#TODO надо бы мделать автолуз
@router.websocket("/ws/{uid}")
async def websocket_endpoint(websocket: WebSocket, uid:str):
    await websocket.accept()
    ACTIVE_CONNECTIONS[uid] = websocket

    script_dir = Path(argv[0]).parent.resolve()  # путь к каталогу скрипта
    db_path = script_dir / 'database' / 'database.db'
    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    try:
        while True:
            data = await websocket.receive_json()
            event = data.get("event")

            if event not in EVENT_HANDLER:
                await websocket.send_json({"error": "Event not found", "type": "404"})
                continue

            # === СТАРТ ПОИСКА ===
            if event == "start":
                # Добавляем игрока в очередь
                global QUEUE
                QUEUE.append(uid)
                QUEUE = list(set(QUEUE))
                await websocket.send_json({"event": "Add in queue"})

                # Проверяем, можно ли создать матч
                if len(QUEUE) >= 2:
                    global player_1
                    global player_2
                    player_1 = QUEUE.pop(0)
                    player_2 = QUEUE.pop(0)
                    global s_datetime
                    s_datetime = datetime.datetime.now()

                    # Генерация ID матча (без словарей в строке)
                    mid = f"{round(int(s_datetime.timestamp())+0.0000001)}-{player_1}-{player_2}-{random.randint(100000,1000000)}"

                    board = [0] * 9
                    current_mark = player_1
                    moves = 0

                    MATCHES.append({
                        'mid': mid,
                        'player_1': player_1,
                        'player_2': player_2,
                        'board': board,
                        'current_mark': current_mark,
                        'moves': moves,
                        's_datetime': s_datetime
                    })

                    # === СОЗДАНИЕ КОМНАТЫ ===
                    ws1 = ACTIVE_CONNECTIONS.get(player_1)
                    ws2 = ACTIVE_CONNECTIONS.get(player_2)
                    room = set()
                    if ws1: room.add(ws1)
                    if ws2: room.add(ws2)
                    ROOMS[mid] = room

                    # Оповещаем обоих
                    msg = {
                        "event": "matches_found",
                        "mid": mid,
                        "board": board,
                        "current_mark": current_mark,
                        "player_1":player_1,
                        "player_2":player_2
                    }
                    for ws in room:
                        try:
                            await ws.send_json(msg)
                        except:
                            pass

            # === ОТМЕНА ПОИСКА ===
            elif event == "cancel":
                if uid in QUEUE:
                    QUEUE.remove(uid)
                    await websocket.send_json({"event": "search_cancelled"})
            
            # === ХОД В ИГРЕ ===
            elif event == "move":
                match_id = data.get("match_id")
                position = data.get("position")  # 0-8
                if match_id not in ROOMS:
                    await websocket.send_json({"error": "Match not found"})
                    continue

                # Ищем матч в MATCHES
                match = None
                for m in MATCHES:
                    if m["mid"] == match_id:
                        match = m
                        break
                if not match:
                    await websocket.send_json({"error": "Match data missing"})
                    continue

                # Проверка, чей ход
                if (match["current_mark"] == player_1 and uid != match["player_1"]) or (match["current_mark"] == player_2 and uid != match["player_2"]):
                    await websocket.send_json({"error": "Not your turn","position":position})
                    continue

                # Проверка, что клетка свободна
                if match["board"][position] != 0:
                    await websocket.send_json({"error": "Cell occupied","position":position})
                    continue

                # Делаем ход
                mark = 1 if match["current_mark"] == player_1 else 2
                match["board"][position] = int(mark)
                match["moves"] += 1

                # Проверка победы
                if check_win(match["board"], int(mark)):
                    # Победа!
                    winner = uid

                    f_datetime = datetime.datetime.now()

                    R1 = cursor.execute('''SELECT elo FROM player WHERE uid = ?''', (player_1,)).fetchone()[0]
                    R2 = cursor.execute('''SELECT elo FROM player WHERE uid = ?''', (player_2,)).fetchone()[0]

                    elo_1 = (20 if R1 < 2400 else 10) * ((1 if player_1 == winner else 0) - (1 / (1 + 10 * ((R2 - R1) / 400))))
                    elo_2 = (20 if R1 < 2400 else 10) * ((1 if player_2 == winner else 0) - (1 / (1 + 10 * ((R1 - R2) / 400))))

                    cursor.execute('''INSERT INTO match (mid,player_1,player_2,winner,elo_1,elo_2,start_datetime,finish_datetime) VALUES (?,?,?,?,?,?,?,?)''', (match_id,player_1,player_2,winner,elo_1,elo_2,s_datetime,f_datetime,))
                    cursor.execute('''UPDATE player SET elo = ? WHERE uid = ?''', (R1+elo_1, player_1,))
                    cursor.execute('''UPDATE player SET elo = ? WHERE uid = ?''', (R2+elo_2, player_2,))
                    cursor.execute('''UPDATE player SET matches = matches + 1 WHERE uid = ?''', (player_1,))
                    cursor.execute('''UPDATE player SET matches = matches + 1 WHERE uid = ?''', (player_2,))

                    if winner == player_1:
                        cursor.execute('''UPDATE player SET wins = wins + 1 WHERE uid = ?''', (player_1,))
                        cursor.execute('''UPDATE player SET loses = loses + 1 WHERE uid = ?''', (player_2,))
                    else:
                        cursor.execute('''UPDATE player SET wins = wins + 1 WHERE uid = ?''', (player_2,))
                        cursor.execute('''UPDATE player SET loses = loses + 1 WHERE uid = ?''', (player_1,))
                    conn.commit()

                    # Рассылаем результат
                    update_msg = {
                        "event": "game_over",
                        "winner": winner,
                        "board": match["board"]
                    }
                    # Удаляем комнату после игры
                    room = ROOMS.pop(match_id, set())
                    for ws in room:
                        try:
                            await ws.send_json(update_msg)
                        except:
                            pass
                    # Можно удалить матч из MATCHES или пометить завершённым
                    continue

                # Проверка ничьей
                if match["moves"] >= 9:

                    winner = ""

                    f_datetime = datetime.datetime.now()

                    R1 = cursor.execute('''SELECT elo FROM player WHERE uid = ?''', (player_1,)).fetchone()[0]
                    R2 = cursor.execute('''SELECT elo FROM player WHERE uid = ?''', (player_2,)).fetchone()[0]

                    elo_1 = (20 if R1 < 2400 else 10) * (0.5  - (1 / (1 + 10 * ((R2 - R1) / 400))))
                    elo_2 = (20 if R1 < 2400 else 10) * (0.5 - (1 / (1 + 10 * ((R1 - R2) / 400))))

                    cursor.execute('''INSERT INTO match (mid,player_1,player_2,winner,elo_1,elo_2,start_datetime,finish_datetime) VALUES (?,?,?,?,?,?,?,?)''', (match_id,player_1,player_2,winner,elo_1,elo_2,s_datetime,f_datetime,))
                    cursor.execute('''UPDATE player SET elo = ? WHERE uid = ?''', (R1+elo_1, player_1,))
                    cursor.execute('''UPDATE player SET elo = ? WHERE uid = ?''', (R2+elo_2, player_2,))
                    cursor.execute('''UPDATE player SET matches = matches + 1 WHERE uid = ?''', (player_1,))
                    cursor.execute('''UPDATE player SET matches = matches + 1 WHERE uid = ?''', (player_2,))

                    conn.commit()

                    update_msg = {
                        "event": "game_over",
                        "winner": None,  # ничья
                        "board": match["board"]
                    }
                    room = ROOMS.pop(mid, set())
                    for ws in room:
                        try:
                            await ws.send_json(update_msg)
                        except:
                            pass
                    continue

                # Переход хода
                match["current_mark"] = player_1 if mark == 2 else player_2

                # Рассылка обновлённого состояния комнате
                update_msg = {
                    "event": "board_update",
                    "board": match["board"],
                    "current_mark": match["current_mark"]
                }
                room = ROOMS.get(match_id, set())
                dead = []
                for ws in room:
                    try:
                        await ws.send_json(update_msg)
                    except:
                        dead.append(ws)
                for ws in dead:
                    room.discard(ws)
                if not room:
                    ROOMS.pop(match_id, None)

            # === ЗАКРЫТИЕ МАТЧА (добровольное) ===
            elif event == "close_match":
                match_id = data.get("match_id")
                if match_id in ROOMS:
                    room = ROOMS.pop(match_id)
                    for ws in room:
                        try:
                            await ws.send_json({"event": "match_closed"})
                        except:
                            pass
                    # Удаляем матч из MATCHES
                    for m in MATCHES:
                        if m["mid"] == match_id:
                            MATCHES.remove(m)
                            break

    except WebSocketDisconnect:
        # Игрок отключился
        if uid in QUEUE:
            QUEUE.remove(uid)
            print(QUEUE)
        # elif uid in MATCHES:
        else:
            try:
                room = ROOMS.pop(match_id)
            except Exception:
                print("Match not found for delete room")
            for ws in room:
                try:
                    await ws.send_json({"event": "match_closed"})
                except:
                    pass
            # Удаляем матч из MATCHES
            for m in MATCHES:
                if m["mid"] == match_id:
                    MATCHES.remove(m)
                    break
    finally:
        # Очистка
        # Удаляем из ACTIVE_CONNECTIONS
        for key, ws in list(ACTIVE_CONNECTIONS.items()):
            if ws == websocket:
                del ACTIVE_CONNECTIONS[key]
                break
        # Удаляем из QUEUE
        if uid in QUEUE:
            QUEUE.remove(uid)
        # Удаляем из всех комнат
        for mid, room in list(ROOMS.items()):
            if websocket in room:
                room.discard(websocket)
                if not room:
                    del ROOMS[mid]
                    # Оповестить оставшегося игрока, что соперник вышел (опционально)
                    # Здесь можно отправить сообщение другому игроку

        # Закрываем соединение с БД
        conn.close()

def check_win(b, mark):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for condition in win_conditions:
        if b[condition[0]] == b[condition[1]] == b[condition[2]] == mark:
            return True
    return False