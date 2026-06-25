import logging
import threading
import os
import signal
import sqlite3
from fastapi import FastAPI
from routers import player, rating, match
from database import create_database
from contextlib import asynccontextmanager
from pathlib import Path
from sys import argv


# --- 1. НАСТРОЙКА ЛОГИРОВАНИЯ ---
# Базовый конфиг: выводим время, уровень и сообщение
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Отключаем спам от uvicorn (оставляем только WARNING и ERROR)
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

create_database.create_database()

app = FastAPI()

@app.get("/")
async def check_server_status():
    return None

app.include_router(match.router)
app.include_router(player.router)
app.include_router(rating.router)

# --- 2. ГРАЦИОЗНАЯ ОСТАНОВКА (Срабатывает при /stop) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Сервер останавливается. Завершение матчей и очистка очереди...")

    try:
        script_dir = Path(argv[0]).parent.resolve()
        db_path = script_dir / 'database' / 'database.db'
        
        # Подключаемся, меняем статус на offline, сохраняем и закрываем
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE player SET status = ?;", ('offline',))
        conn.commit()
        conn.close()
        logger.info("Статус всех игроков успешно изменен на 'offline'.")
    except Exception as e:
        logger.error(f"Ошибка при обновлении статусов в БД: {e}")
    
    # Опустошаем очередь
    match.QUEUE.clear()
    
    # Оповещаем и отключаем всех игроков в активных соединениях
    for uid, ws in list(match.ACTIVE_CONNECTIONS.items()):
        try:
            await ws.send_json({"event": "server_shutdown", "message": "Сервер был остановлен администратором."})
            await ws.close()
        except Exception:
            pass
            
    match.ACTIVE_CONNECTIONS.clear()
    match.ROOMS.clear()
    match.MATCHES.clear()
    logger.info("Очереди и матчи успешно очищены. Сервер выключен.")

# --- 3. ОБРАБОТЧИК КОМАНДЫ РЕЙТИНГА ---
def handle_rating_cmd(cmd: str):
    parts = cmd.split()
    
    # Дефолтные значения
    category = "elo"
    limit = 100
    player_uid = None
    
    cat_map = {"-e": "elo", "-w": "wins", "-l": "loses", "-g": "matches"}
    
    # Парсим аргументы
    i = 1
    while i < len(parts):
        p = parts[i]
        if p in cat_map:
            category = cat_map[p]
        elif p == "-lim" and i + 1 < len(parts):
            try:
                limit = int(parts[i+1])
            except ValueError:
                pass
            i += 1
        else:
            player_uid = p  # Если не флаг, значит это идентификатор игрока
        i += 1

    # Запрос в БД
    try:
        script_dir = Path(argv[0]).parent.resolve()  # путь к каталогу скрипта
        db_path = script_dir / 'database' / 'database.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        if player_uid:
            # Ищем конкретного игрока
            cursor.execute(f"SELECT nickname, {category} FROM player WHERE uid = ?", (player_uid,))
            user = cursor.fetchone()
            if user:
                name, val = user
                # Вычисляем его место в топе (считаем, сколько людей имеют показатель выше)
                cursor.execute(f"SELECT COUNT(*) FROM player WHERE {category} > ?", (val,))
                rank = cursor.fetchone()[0] + 1
                print(f"\n[РЕЙТИНГ] Игрок {name} ({player_uid}) занимает {rank} место в категории '{category}' со счетом {round(val)}.\n")
            else:
                print(f"\n[ОШИБКА] Игрок с идентификатором {player_uid} не найден.\n")
        else:
            # Выдаем топ игроков
            cursor.execute(f"SELECT nickname, {category} FROM player ORDER BY {category} DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            print(f"\n--- ТОП {limit} ({category.upper()}) ---")
            for idx, row in enumerate(rows, 1):
                print(f"{idx}. {row[0]} - {round(row[1])}")
            print("-----------------------\n")
        conn.close()
    except Exception as e:
        logger.error(f"Ошибка при запросе рейтинга из БД: {e}")

# --- 4. ФОНОВЫЙ ПОТОК ДЛЯ ЧТЕНИЯ КОНСОЛИ ---
def console_listener():
    while True:
        try:
            cmd = input().strip()
            if not cmd:
                continue
            
            if cmd == "/stop":
                logger.info("Получена команда /stop. Инициализация остановки...")
                script_dir = Path(argv[0]).parent.resolve()  # путь к каталогу скрипта
                db_path = script_dir / 'database' / 'database.db'
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                cursor.execute('''UPDATE player SET status = 'offline' ''')
                conn.commit()
                conn.close()
                # Посылаем процессу сигнал прерывания (Ctrl+C), чтобы FastAPI корректно завершил работу
                os.kill(os.getpid(), signal.SIGINT)
                break
            elif cmd.startswith("/rating"):
                handle_rating_cmd(cmd)
            else:
                print("Неизвестная команда. Доступные:\n /stop\n /rating [-e|-w|-l|-g] [-lim X] [uid]")
        except EOFError:
            break
        except Exception as e:
            logger.error(f"Ошибка в консоли: {e}")

if __name__ == '__main__':
    import uvicorn
    
    # Запускаем слушатель консоли в отдельном daemon-потоке
    # (daemon=True означает, что поток умрет вместе с основным процессом)
    threading.Thread(target=console_listener, daemon=True).start()
    
    logger.info("Сервер запускается. Введите команды в консоль.")
    
    # Запуск сервера. Обратите внимание, что мы убрали reload=True, 
    # так как он конфликтует с консольным вводом (input)
    uvicorn.run("main:app", host="0.0.0.0", port=8000)