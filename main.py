import sqlite3
import sys

from addEditCoffeeForm import Ui_MainWindow
from UI_main import Ui_MainWindow as ui_main
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QInputDialog
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow, ui_main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.titles = None
        self.con = sqlite3.connect("data/coffee.sqlite")
        self.init_item()
        self.edit_window = None
        self.pushButton.clicked.connect(self.run_edit)

    def init_item(self):
        cur = self.con.cursor()
        item = cur.execute("""SELECT * from coffe""").fetchall()
        self.tableWidget.setRowCount(len(item))

        if not item:
            return

        self.tableWidget.setColumnCount(len(item[0]))
        self.titles = [description[0] for description in cur.description]

        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(item):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def run_edit(self):
        self.edit_window = EditCoffe()
        self.edit_window.show()


class EditCoffe(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("data/coffee.sqlite")
        self.modified = {}
        self.init_item()
        self.btn_new.clicked.connect(self.run_new)
        self.btn_save.clicked.connect(self.run_save)
        self.ind = []
        self.tableWidget.itemChanged.connect(self.item_changed)

    def run_save(self):
        if self.modified:
            print(", ".join([f"{key}='{self.modified.get(key)}'"
                             for key in self.modified.keys()]))
            cur = self.con.cursor()
            que = "UPDATE coffe SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                              for key in self.modified.keys()])
            que += "WHERE id = ?"
            cur.execute(que, (self.ind[-1],))
            self.con.commit()
            self.modified.clear()

    def run_new(self):
        sort, ok_pressed = QInputDialog.getText(self, "", "Введите сорт нового кофе")
        if not ok_pressed:
            return

        roast_degree, ok_pressed = QInputDialog.getText(self, "", "Введите обжарку нового кофе")
        if not ok_pressed:
            return

        ground_or_cereal, ok_pressed = QInputDialog.getText(self, "", "Молотый / в зернах новый кофе?")
        if not ok_pressed:
            return

        flavour_description, ok_pressed = QInputDialog.getText(self, "", "Опишите вкус нового кофе")
        if not ok_pressed:
            return

        price, ok_pressed = QInputDialog.getText(self, "", "Цена нового кофе?")
        if not ok_pressed:
            return

        volume, ok_pressed = QInputDialog.getText(self, "", "Объём нового кофе?")
        if not ok_pressed:
            return

        cur = self.con.cursor()
        cur.execute("""INSERT INTO coffe(sort,roast_degree,ground_or_cereal,flavour_description,price,package_volume) 
                        VALUES(?,?,?,?,?,?)""", (sort, roast_degree, ground_or_cereal, flavour_description, int(price),
                                                 volume)).fetchall()
        self.con.commit()
        self.init_item()

    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = item.text()
        self.ind.append(item.row() + 1)

    def init_item(self):
        cur = self.con.cursor()
        item = cur.execute("""SELECT * from coffe""").fetchall()
        self.tableWidget.setRowCount(len(item))

        if not item:
            return

        self.tableWidget.setColumnCount(len(item[0]))
        self.titles = [description[0] for description in cur.description]

        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(item):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyWidget()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
