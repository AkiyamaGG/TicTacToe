# -*- coding: utf-8 -*-
################################################################################
## Form generated from reading UI file 'xo.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
from PySide6 import QtCore, QtGui
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, Signal, QTimer, QThread)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform, QStandardItemModel)
from PySide6.QtWidgets import (QApplication, QFrame, QHeaderView, QLabel,
                               QMainWindow, QPushButton, QSizePolicy, QStatusBar,
                               QTabWidget, QTableView, QWidget, QVBoxLayout, QMessageBox)
import sys, socket, requests, websocket, json, queue, threading, time

HOST_URL = "127.0.0.1:8000"

nickname = socket.gethostname()

class Player:
    def create_player(nickname):
        requests.post(f'http://{HOST_URL}/player/create',json={'nickname':nickname})
        
    def get_player_info_for_nickname(self, nickname):
        try:
            player = requests.get(f'http://{HOST_URL}/player/info/nickname/{nickname}')
            uid = player.json()["uid"]
            elo = player.json()["elo"]
            wins = player.json()["wins"]
            loses = player.json()["loses"]
            matches = player.json()["matches"]
            p_status = player.json()["status"]
            status = "Нажмите старт"
            return uid,elo,wins,loses,matches,p_status,status
        except requests.exceptions.JSONDecodeError:
            self.create_player(nickname)
            player = requests.get(f'http://{HOST_URL}/player/info/nickname/{nickname}')
            uid = player.json()["uid"]
            elo = player.json()["elo"]
            wins = player.json()["wins"]
            loses = player.json()["loses"]
            matches = player.json()["matches"]
            p_status = player.json()["status"]
            status = "Нажмите старт"
            return uid,elo,wins,loses,matches,p_status,status
        except requests.exceptions.ConnectionError:
            uid = ''
            elo = 0
            wins = 0
            loses = 0
            matches = 0
            p_status = 'offline'
            status = "Сервер недоступен😭"
            return uid,elo,wins,loses,matches,p_status,status
        
    def get_player_info_for_uid(uid):
        try:
            player = requests.get(f'http://{HOST_URL}/player/info/uid/{uid}')
            elo = player.json()["elo"]
            wins = player.json()["wins"]
            loses = player.json()["loses"]
            matches = player.json()["matches"]
            p_status = player.json()["status"]
            status = "Нажмите старт"
            return elo,wins,loses,matches,p_status,status
        except requests.exceptions.ConnectionError:
            elo = 0
            wins = 0
            loses = 0
            matches = 0
            p_status = 'offline'
            status = "Сервер недоступен😭"
            return elo,wins,loses,matches,p_status,status
    
    def update_player_status(uid,p_status):
        try:
            requests.post(f"http://{HOST_URL}/player/status/uid/update/{uid}",json={"uid":uid,"status":p_status})
        except requests.exceptions.ConnectionError:
            status = "Сервер недоступен😭"
            return status

class Opponent:
    def get_opponent_info(uid):
        opponent = requests.get(f'http://{HOST_URL}/player/info/uid/{uid}').json()
        nickname = opponent["nickname"]
        elo = opponent["elo"]
        return nickname,elo
        

player = Player

global uid,elo,wins,loses,matches,p_status,status
uid,elo,wins,loses,matches,p_status,status = player.get_player_info_for_nickname(player, nickname)

mid = ""
o_nickname, o_elo = '',0
y_mark, o_mark = "",""
button_text = "Start"


if p_status == "online":
   sys.exit()
else:
    player.update_player_status(uid, "online")


class Rating:
    def __init__(self):
        self.type = None
        self.limit = 100
    def get_rating(type, limit=100):
        try:
            table = requests.get(f"http://{HOST_URL}/rating/{type}/?limit={limit}").json()
            keys = ["nickname",type]
            return table, keys
        except requests.exceptions.JSONDecodeError:
            table = [{"nickname":"",type:""}]
            keys = ["nickname",type]
            return table, keys
        except requests.exceptions.ConnectionError:
            table = [{"nickname":"",type:""}]
            keys = ["nickname",type]
            return table, keys


class Ui_TicTacToe(object):
    def setupUi(self, TicTacToe):
        if not TicTacToe.objectName():
            TicTacToe.setObjectName(u"TicTacToe")
        TicTacToe.resize(430, 250)
        TicTacToe.setStyleSheet(u"")
        self.centralwidget = QWidget(TicTacToe)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 430, 250))
        self.tabWidget.setStyleSheet(u"")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.line_4 = QFrame(self.tab)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setGeometry(QRect(10, 130, 190, 20))
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)
        self.pushButton_7 = QPushButton(self.tab)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setGeometry(QRect(150, 10, 50, 50))
        self.pushButton_8 = QPushButton(self.tab)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setGeometry(QRect(80, 10, 50, 50))
        self.pushButton_2 = QPushButton(self.tab)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(80, 150, 50, 50))
        self.pushButton_9 = QPushButton(self.tab)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setGeometry(QRect(10, 10, 50, 50))
        self.pushButton_3 = QPushButton(self.tab)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(150, 150, 50, 50))
        self.pushButton_4 = QPushButton(self.tab)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(10, 80, 50, 50))
        self.line = QFrame(self.tab)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(130, 10, 20, 191))
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.pushButton_5 = QPushButton(self.tab)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(80, 80, 50, 50))
        self.pushButton_6 = QPushButton(self.tab)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setGeometry(QRect(150, 80, 50, 50))
        self.line_2 = QFrame(self.tab)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(60, 10, 20, 190))
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.pushButton = QPushButton(self.tab)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(10, 150, 50, 50))
        self.line_3 = QFrame(self.tab)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setGeometry(QRect(10, 60, 191, 20))
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)
        self.label_3 = QLabel(self.tab)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(210, 40, 100, 20))
        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(210, 20, 100, 20))
        self.label_2 = QLabel(self.tab)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(320, 40, 90, 20))
        self.pushButton_10 = QPushButton(self.tab)
        self.pushButton_10.setObjectName(u"pushButton_10")
        self.pushButton_10.setGeometry(QRect(340, 170, 75, 25))
        self.label_4 = QLabel(self.tab)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(320, 20, 90, 20))
        self.label_5 = QLabel(self.tab)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(210, 60, 100, 20))
        self.label_6 = QLabel(self.tab)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(210, 0, 21, 20))
        self.label_6.setMaximumSize(QSize(16777215, 16777213))
        self.label_7 = QLabel(self.tab)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(210, 90, 100, 20))
        self.label_8 = QLabel(self.tab)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(210, 110, 100, 20))
        self.label_9 = QLabel(self.tab)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(210, 130, 90, 20))
        self.label_10 = QLabel(self.tab)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(210, 170, 120, 20))
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget_2 = QTabWidget(self.tab_2)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tabWidget_2.setGeometry(QRect(0, 0, 430, 210))
        self.tabWidget_2.setStyleSheet(u"")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.tableView = QTableView(self.tab_6)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setEnabled(True)
        self.tableView.setGeometry(QRect(0, 0, 420, 180))

        rating = Rating

        elo_table, keys = rating.get_rating("elo")

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['№'] + keys)

        for i, row_dict in enumerate(elo_table):
            # Элемент для колонки Нумерации
            num_item = QtGui.QStandardItem(str(i + 1))
            num_item.setTextAlignment(QtCore.Qt.AlignCenter)  # Выравнивание

            row_items = [num_item]

            # Элементы для значений из словаря
            for key in keys:
                val = str(row_dict.get(key, ''))  # Безопасное получение значения
                row_items.append(QtGui.QStandardItem(val))

            self.model.appendRow(row_items)

        self.tableView.setModel(self.model)
        self.tabWidget_2.addTab(self.tab_6, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.tableView_2 = QTableView(self.tab_3)
        self.tableView_2.setObjectName(u"tableView_2")
        self.tableView_2.setEnabled(True)
        self.tableView_2.setGeometry(QRect(0, 0, 420, 180))

        wins_table, keys = rating.get_rating("wins")

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['№'] + keys)

        for i, row_dict in enumerate(wins_table):
            # Элемент для колонки Нумерации
            num_item = QtGui.QStandardItem(str(i + 1))
            num_item.setTextAlignment(QtCore.Qt.AlignCenter)  # Выравнивание

            row_items = [num_item]

            # Элементы для значений из словаря
            for key in keys:
                val = str(row_dict.get(key, ''))  # Безопасное получение значения
                row_items.append(QtGui.QStandardItem(val))

            self.model.appendRow(row_items)

        self.tableView_2.setModel(self.model)
        self.tabWidget_2.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.tableView_3 = QTableView(self.tab_4)
        self.tableView_3.setObjectName(u"tableView_3")
        self.tableView_3.setEnabled(True)
        self.tableView_3.setGeometry(QRect(0, 0, 420, 180))

        
        loses_table, keys = rating.get_rating("loses")

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['№'] + keys)

        for i, row_dict in enumerate(loses_table):
            # Элемент для колонки Нумерации
            num_item = QtGui.QStandardItem(str(i + 1))
            num_item.setTextAlignment(QtCore.Qt.AlignCenter)  # Выравнивание

            row_items = [num_item]

            # Элементы для значений из словаря
            for key in keys:
                val = str(row_dict.get(key, ''))  # Безопасное получение значения
                row_items.append(QtGui.QStandardItem(val))

            self.model.appendRow(row_items)

        self.tableView_3.setModel(self.model)
        self.tabWidget_2.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.tableView_4 = QTableView(self.tab_5)
        self.tableView_4.setObjectName(u"tableView_4")
        self.tableView_4.setEnabled(True)
        self.tableView_4.setGeometry(QRect(0, 0, 420, 180))

        matches_table, keys = rating.get_rating("matches")

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['№'] + keys)

        for i, row_dict in enumerate(matches_table):
            # Элемент для колонки Нумерации
            num_item = QtGui.QStandardItem(str(i + 1))
            num_item.setTextAlignment(QtCore.Qt.AlignCenter)  # Выравнивание

            row_items = [num_item]

            # Элементы для значений из словаря
            for key in keys:
                val = str(row_dict.get(key, ''))  # Безопасное получение значения
                row_items.append(QtGui.QStandardItem(val))

            self.model.appendRow(row_items)

        self.tableView_4.setModel(self.model)
        self.tabWidget_2.addTab(self.tab_5, "")
        self.tabWidget.addTab(self.tab_2, "")
        TicTacToe.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(TicTacToe)
        self.statusbar.setObjectName(u"statusbar")
        TicTacToe.setStatusBar(self.statusbar)

        self.retranslateUi(TicTacToe)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)




        QMetaObject.connectSlotsByName(TicTacToe)
    # setupUi

    def retranslateUi(self, TicTacToe):
        TicTacToe.setWindowTitle(QCoreApplication.translate("TicTacToe", u"TicTacToe", None))
        self.pushButton_7.setText("")
        self.pushButton_8.setText("")
        self.pushButton_2.setText("")
        self.pushButton_9.setText("")
        self.pushButton_3.setText("")
        self.pushButton_4.setText("")
        self.pushButton_5.setText("")
        self.pushButton_6.setText("")
        self.pushButton.setText("")
        self.label_3.setText(QCoreApplication.translate("TicTacToe", f"Loses: {loses}", None))
        self.label.setText(QCoreApplication.translate("TicTacToe", f"Wins: {wins}", None))
        self.label_2.setText(QCoreApplication.translate("TicTacToe", f"ELO: {elo}", None))
        self.pushButton_10.setText(QCoreApplication.translate("TicTacToe", f"{button_text}", None))
        self.label_4.setText(QCoreApplication.translate("TicTacToe", f"{nickname}", None))
        self.label_5.setText(QCoreApplication.translate("TicTacToe", f"W/L: {round(wins/loses + 0.000000001,2) if loses != 0 else wins}", None))
        self.label_6.setText(QCoreApplication.translate("TicTacToe", f"You: {y_mark}", None))
        self.label_7.setText(QCoreApplication.translate("TicTacToe", f"Opponent: {o_mark}", None))
        self.label_8.setText(QCoreApplication.translate("TicTacToe", f"{o_nickname}", None))
        self.label_9.setText(QCoreApplication.translate("TicTacToe", f"ELO: {o_elo}", None))
        self.label_10.setText(status)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("TicTacToe", u"Game", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_6), QCoreApplication.translate("TicTacToe", u"ELO", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), QCoreApplication.translate("TicTacToe", u"N of Wins", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), QCoreApplication.translate("TicTacToe", u"N of Loses", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_5), QCoreApplication.translate("TicTacToe", u"N of Matches", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("TicTacToe", u"Rating", None))
    # retranslateUi

class WebSocketWorker(QObject):
    message_received = Signal(dict)
    connection_error = Signal(str)
    connection_closed = Signal()

    def __init__(self, uid):
        super().__init__()
        self.uid = uid
        self.ws = None
        self.running = False
        self.send_queue = queue.Queue()
        self._stop_event = threading.Event()

    def run(self):
        self.running = True
        try:
            self.ws = websocket.create_connection(f"ws://{HOST_URL}/match/ws/{self.uid}")
            self.ws.settimeout(0.1)
            while self.running:
                # Отправка сообщений из очереди
                try:
                    while True:
                        msg = self.send_queue.get_nowait()
                        self.ws.send(json.dumps(msg))
                except queue.Empty:
                    pass
                # Чтение входящих сообщений
                try:
                    data = self.ws.recv()
                    if data:
                        msg = json.loads(data)
                        self.message_received.emit(msg)
                except websocket.WebSocketTimeoutException:
                    pass
                except websocket.WebSocketConnectionClosedException:
                    self.running = False
                except Exception as e:
                    self.connection_error.emit(str(e))
                    self.running = False
        except Exception as e:
            self.connection_error.emit(str(e))
        finally:
            self.running = False
            if self.ws:
                self.ws.close()
            self.connection_closed.emit()

    def send(self, message):
        self.send_queue.put(message)

    def stop(self):
        self.running = False

class MainWindow(QMainWindow):
    # Состояния игры
    IDLE = 0
    SEARCHING = 1
    IN_GAME = 2

    def __init__(self):
        super().__init__()
        self.ui = Ui_TicTacToe()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('icon.ico'))
        self.setFixedSize(430, 250)

        self.game_state = MainWindow.IDLE
        self.match_id = None
        self.board = [0] * 9
        self.current_turn_uid = None
        self.is_my_turn = False
        self.my_mark = 0
        self.opponent_uid = None
        self.opponent_nickname = ""
        self.opponent_elo = 0

        # Список кнопок поля (индексы 0-8)
        self.board_buttons = [
            self.ui.pushButton_9,  # 0: левая верхняя
            self.ui.pushButton_8,  # 1: центральная верхняя
            self.ui.pushButton_7,  # 2: правая верхняя
            self.ui.pushButton_4,  # 3: левая средняя
            self.ui.pushButton_5,  # 4: центральная средняя
            self.ui.pushButton_6,  # 5: правая средняя
            self.ui.pushButton,    # 6: левая нижняя
            self.ui.pushButton_2,  # 7: центральная нижняя
            self.ui.pushButton_3   # 8: правая нижняя
        ]

        # Подключаем кнопки поля
        for idx, btn in enumerate(self.board_buttons):
            btn.clicked.connect(lambda checked, idx=idx: self.on_board_button_clicked(idx))

        # Кнопка "Start" / "Cancel" / "Forfeit"
        self.ui.pushButton_10.clicked.connect(self.on_action_button_clicked)

        # Настройка потока WebSocket
        self.worker = WebSocketWorker(uid)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.message_received.connect(self.handle_ws_message)
        self.worker.connection_error.connect(self.handle_ws_error)
        self.worker.connection_closed.connect(self.handle_ws_closed)
        self.thread.start()

        # Таймер для сброса цвета кнопки после ошибки
        self.error_flash_timer = QTimer(self)
        self.error_flash_timer.setSingleShot(True)
        self.error_flash_timer.timeout.connect(self.reset_error_button_style)

        self.error_button = None

        self.update_ui()
        self.update_rating_tables()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Выход', 'Вы действительно хотите выйти?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # Сообщаем серверу о выходе из матча или отмене поиска
                if self.game_state == MainWindow.IN_GAME and self.match_id:
                    self.worker.send({"event": "close_match", "match_id": self.match_id})
                elif self.game_state == MainWindow.SEARCHING:
                    self.worker.send({"event": "cancel"})
                
                # Даем потоку WebSocket крошечное время (100 мс) на отправку пакета
                time.sleep(0.1) 
                
                Player.update_player_status(uid, "offline")
            except Exception as e:
                print(f"Ошибка при выходе: {e}")
                
            self.worker.stop()
            self.thread.quit()
            self.thread.wait()
            event.accept()
        else:
            event.ignore()

    # === Обработчики кнопок ===
    def on_action_button_clicked(self):
        if self.game_state == MainWindow.IDLE:
            # Начать поиск
            self.game_state = MainWindow.SEARCHING
            self.worker.send({"event": "start"})
            self.ui.pushButton_10.setText("Cancel")
            self.ui.label_10.setText("Поиск соперника...")
            self.clear_board()
        elif self.game_state == MainWindow.SEARCHING:
            # Отменить поиск
            self.worker.send({"event": "cancel"})
            self.game_state = MainWindow.IDLE
            self.ui.pushButton_10.setText("Start")
            self.ui.label_10.setText("Поиск отменён")
        elif self.game_state == MainWindow.IN_GAME:
            # Форфейт / закрыть матч
            if self.match_id:
                self.worker.send({"event": "close_match", "match_id": self.match_id})
            self.reset_game_state()

    def on_board_button_clicked(self, idx):
        if self.game_state != MainWindow.IN_GAME or not self.is_my_turn:
            return
        if self.board[idx] != 0:
            # Клетка занята – имитация ошибки
            self.flash_error_on_button(idx)
            return
        # Отправляем ход
        self.worker.send({"event": "move", "match_id": self.match_id, "position": idx})

    def flash_error_on_button(self, idx):
        btn = self.board_buttons[idx]
        btn.setStyleSheet("background-color: red;")
        self.error_button = btn
        self.error_flash_timer.start(300)

    def reset_error_button_style(self):
        if self.error_button:
            self.error_button.setStyleSheet("")
            self.error_button = None

    # === Обработчики сообщений WebSocket ===
    def handle_ws_message(self, msg):
        event = msg.get("event")
        if event == "Add in queue":
            pass  # уже в поиске
        elif event == "matches_found":
            self.match_id = msg["mid"]
            self.board = msg["board"]
            self.current_turn_uid = msg["current_mark"]
            self.player_1 = msg["player_1"]
            self.player_2 = msg["player_2"]
            # Определяем, кто мы в этом матче
            # Отправим запрос на получение информации о матче
            try:
                if uid == self.player_1:
                    self.my_mark = 1
                    self.opponent_uid = self.player_2
                else:
                    self.my_mark = 2
                    self.opponent_uid = self.player_1
                # Получаем данные соперника
                opp_nick, opp_elo = Opponent.get_opponent_info(self.opponent_uid)
                self.opponent_nickname = opp_nick
                self.opponent_elo = opp_elo
                # Обновляем метки
                self.ui.label_6.setText(f"You: {'X' if self.my_mark == 1 else 'O'}")
                self.ui.label_7.setText(f"Opponent: {'X' if self.my_mark == 2 else 'O'}")
                self.ui.label_8.setText(self.opponent_nickname)
                self.ui.label_9.setText(f"ELO: {self.opponent_elo}")
            except Exception as e:
                print("Ошибка получения данных матча:", e)
                self.ui.label_10.setText("Ошибка данных матча")
                self.reset_game_state()
                return

            self.game_state = MainWindow.IN_GAME
            self.ui.pushButton_10.setText("Exit")
            self.ui.label_10.setText("Игра началась")
            self.update_board_ui()

        elif event == "board_update":
            self.board = msg["board"]
            self.current_turn_uid = msg["current_mark"]
            self.update_board_ui()

        elif event == "game_over":
            winner = msg.get("winner")
            self.board = msg["board"]
            self.update_board_ui()
            
            if winner == uid:
                self.ui.label_10.setText("Вы победили!")
            elif winner is None:
                self.ui.label_10.setText("Ничья!")
            else:
                self.ui.label_10.setText("Вы проиграли!")
                
            # Обновляем личную статистику
            self.update_player_stats()
            
            # --- НОВАЯ СТРОКА: Обновляем таблицы рейтинга ---
            self.update_rating_tables()
            
            # Сбрасываем состояние через 2 секунды
            QTimer.singleShot(2000, self.reset_game_state)

        elif event == "match_closed":
            self.ui.label_10.setText("Матч закрыт")
            self.reset_game_state()

        elif event == "error":
            error_text = msg.get("error", "")
            position = msg.get("position")
            if "not your turn" in error_text:
                self.ui.label_10.setText("Не ваш ход")
                if position is not None:
                    self.flash_error_on_button(position)
            elif "cell occupied" in error_text:
                self.ui.label_10.setText("Клетка занята")
                if position is not None:
                    self.flash_error_on_button(position)
            else:
                self.ui.label_10.setText(f"Ошибка: {error_text}")

    def handle_ws_error(self, error_msg):
        self.ui.label_10.setText(f"WebSocket error: {error_msg}")
        self.reset_game_state()

    def handle_ws_closed(self):
        if self.game_state != MainWindow.IDLE:
            self.ui.label_10.setText("Соединение закрыто")
            self.reset_game_state()

    def update_board_ui(self):
        self.is_my_turn = (self.current_turn_uid == uid)
        if self.is_my_turn:
            self.ui.label_10.setText("Ваш ход")
        else:
            self.ui.label_10.setText("Ход соперника")

        for idx, btn in enumerate(self.board_buttons):
            val = self.board[idx]
            if val == 0:
                btn.setText("")
                btn.setEnabled(True)
            elif val == 1:
                btn.setText("X")
                btn.setEnabled(False)
            elif val == 2:
                btn.setText("O")
                btn.setEnabled(False)
            # Если не наш ход или игра не идёт, отключаем кнопки
            if not self.is_my_turn or self.game_state != MainWindow.IN_GAME:
                btn.setEnabled(False)

    def clear_board(self):
        for btn in self.board_buttons:
            btn.setText("")
            btn.setEnabled(False)
        self.board = [0] * 9


    def reset_game_state(self):
        self.game_state = MainWindow.IDLE
        self.match_id = None
        self.board = [0] * 9
        self.current_turn_uid = None
        self.is_my_turn = False
        self.my_mark = 0
        self.opponent_uid = None
        self.opponent_nickname = ""
        self.opponent_elo = 0
        self.ui.pushButton_10.setText("Start")
        self.ui.label_6.setText("You: ")
        self.ui.label_7.setText("Opponent: ")
        self.ui.label_8.setText("")
        self.ui.label_9.setText("ELO: ")
        self.ui.label_10.setText("Нажмите старт")
        self.clear_board()
        self.update_player_stats()

    def update_player_stats(self):
        global nickname, uid, elo, wins, loses, matches, p_status
        try:
            # Добавлена переменная status_new для корректной распаковки 7 значений
            uid_new, elo_new, wins_new, loses_new, matches_new, p_status_new, status_new = Player.get_player_info_for_nickname(Player, nickname)
            
            # Обновляем глобальные переменные
            uid = uid_new
            elo = elo_new
            wins = wins_new
            loses = loses_new
            matches = matches_new
            p_status = p_status_new
            
            # Обновляем UI
            self.ui.label.setText(f"Wins: {wins}")
            self.ui.label_3.setText(f"Loses: {loses}")
            self.ui.label_2.setText(f"ELO: {elo}")
            self.ui.label_5.setText(f"W/L: {round(wins/loses + 0.000000001, 2) if loses != 0 else wins}")
            
        except Exception as e:
            # Выводим ошибку в консоль, чтобы в будущем сразу видеть проблему, а не гадать
            print(f"Ошибка при обновлении статистики: {e}")
    
    def update_rating_tables(self):
        """Обновляет все таблицы во вкладке Rating"""
        def refresh_table(view, r_type):
            try:
                # Получаем новые данные. Обрати внимание, вызываем через класс Rating
                data_table, keys = Rating.get_rating(r_type)
                
                model = QStandardItemModel()
                model.setHorizontalHeaderLabels(['№'] + keys)

                for i, row_dict in enumerate(data_table):
                    num_item = QtGui.QStandardItem(str(i + 1))
                    num_item.setTextAlignment(QtCore.Qt.AlignCenter)
                    
                    row_items = [num_item]
                    for key in keys:
                        val = str(row_dict.get(key, ''))
                        row_items.append(QtGui.QStandardItem(val))

                    model.appendRow(row_items)

                view.setModel(model)
            except Exception as e:
                print(f"Ошибка обновления таблицы {r_type}: {e}")

        # Обновляем каждую таблицу по её типу
        refresh_table(self.ui.tableView, "elo")
        refresh_table(self.ui.tableView_2, "wins")
        refresh_table(self.ui.tableView_3, "loses")
        refresh_table(self.ui.tableView_4, "matches")

    def update_ui(self):
        # Первоначальное обновление статистики
        self.update_player_stats()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())