import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.init_item()

    def init_item(self):
        cur = self.con.cursor()
        item = cur.execute("""SELECT * from coffe""").fetchall()
        self.tableWidget.setRowCount(len(item))

        if not item:
            self.statusBar().showMessage('Ничего не нашлось')
            return

        self.tableWidget.setColumnCount(len(item[0]))

        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(item):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyWidget()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())