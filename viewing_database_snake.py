import os
import sys
import multiprocessing
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
import sqlite3
from sqlite3 import Error


class DatabaseManager:
    def __init__(self, db_name):
        self.conn = None
        self.db_name = db_name

    def create_connection(self):
        try:
            self.conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)), self.db_name))
            print(sqlite3.version)
        except Error as e:
            print(e)

    def create_table(self, table_name):
        try:
            sql = f'''CREATE TABLE {table_name} (
                                score integer,
                                date text
                                ); '''
            c = self.conn.cursor()
            c.execute(sql)
        except Error as e:
            print(e)

    def add_data(self, table_name, score, date):
        c = self.conn.cursor()
        values = (score, date)
        c.execute(f"INSERT INTO {table_name} VALUES(?, ?)", values)
        self.conn.commit()


def print_table(table_name):
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('game_snake.db')

    db.open()
    model = QSqlTableModel(db=db)
    model.setTable(table_name)
    model.select()
    view = QTableView()
    view.setWindowTitle("Результаты")  # Установка названия окна
    view.setFixedSize(210, 300)  # Установка размера окна
    view.move(100, 100)
    view.setModel(model)
    view.show()

    return view


def print_app(tbl_name):
    app = QApplication([])
    db = DatabaseManager('game_snake.db')
    db.create_connection()

    table_name = tbl_name
    db.create_table(table_name)

    view = print_table(table_name)
    app.exec()


def tb_app(tbl_name, score, date):
    try:
        app = QApplication([])
        db = DatabaseManager('game_snake.db')
        db.create_connection()

        table_name = tbl_name
        db.create_table(table_name)
        db.add_data(table_name, score, date)

        # Запуск QApplication в отдельном процессе
        multiprocessing.Process(target=app.exec).start()
    except:
        pass
