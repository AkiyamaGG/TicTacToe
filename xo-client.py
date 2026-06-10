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
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform, QStandardItemModel)
from PySide6.QtWidgets import (QApplication, QFrame, QHeaderView, QLabel,
                               QMainWindow, QPushButton, QSizePolicy, QStatusBar,
                               QTabWidget, QTableView, QWidget, QVBoxLayout)
import sys, socket, os, json, requests

HOST_URL = "http://127.0.0.1:8000"

nickname = socket.gethostname()
try:
    player = requests.get(f'{HOST_URL}/player/info/nickname/{nickname}')
    uid = player.json()["uid"]
    elo = player.json()["elo"]
    wins = player.json()["wins"]
    loses = player.json()["loses"]
    matches = player.json()["matches"]
    status = "Нажмите старт"
except requests.exceptions.JSONDecodeError:
    requests.post(f'{HOST_URL}/player/create',json={'nickname':nickname})
    player = requests.get(f'{HOST_URL}/player/info/nickname/{nickname}')
    uid = player.json()["uid"]
    elo = player.json()["elo"]
    wins = player.json()["wins"]
    loses = player.json()["loses"]
    matches = player.json()["matches"]
    status = "Нажмите старт"
except requests.exceptions.ConnectionError:
    uid = ''
    elo = 0
    wins = 0
    loses = 0
    matches = 0
    p_status = 'offline'
    status = "Сервер недоступен😭"
mid = ""
o_nickname = ""
o_elo = 0

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

        elo_table = requests.get(f"{HOST_URL}/rating/elo").json()
        keys = list(elo_table[0].keys())

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

        wins_table = requests.get(f"{HOST_URL}/rating/wins").json()
        keys = list(wins_table[0].keys())

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

        loses_table = requests.get(f"{HOST_URL}/rating/loses").json()
        keys = list(loses_table[0].keys())

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

        matches_table = requests.get(f"{HOST_URL}/rating/matches").json()
        keys = list(matches_table[0].keys())

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
        self.pushButton_10.setText(QCoreApplication.translate("TicTacToe", u"Start", None))
        self.label_4.setText(QCoreApplication.translate("TicTacToe", f"{nickname}", None))
        self.label_5.setText(QCoreApplication.translate("TicTacToe", f"W/L: {wins/loses if loses != 0 else 0}", None))
        self.label_6.setText(QCoreApplication.translate("TicTacToe", f"You:", None))
        self.label_7.setText(QCoreApplication.translate("TicTacToe", f"Opponent:", None))
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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_TicTacToe()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())