from configparser import ConfigParser
from os import listdir, environ, startfile, path as pt
from re import compile
from sys import exit, _MEIPASS

from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import (QApplication, QMessageBox)
from requests import get


class ServerSwitcher:
    od_path = "C:{}\\OneDrive\\Documents\\My Games\\Rainbow Six - Siege".format(environ['HOMEPATH'])
    normal_path = "C:{}\\Documents\\My Games\\Rainbow Six - Siege".format(environ['HOMEPATH'])
    pid_pattern = compile(r"\w{8}-\w{4}-\w{4}-\w{4}-\w{12}")
    areas = [
        "default",
        "eus",
        "cus",
        "scus",
        "wus",
        "sbr",
        "neu",
        "weu",
        "eas",
        "seas",
        "eau",
        "wja"
    ]

    def __init__(self, path: str = None):
        self.path = path

    def get_pids(self) -> list:

        return [x for x in listdir(self.path) if self.pid_pattern.fullmatch(x)]

    @staticmethod
    def get_username(p_id):
        return get("https://r6tab.com/api/player.php", params={"p_id": p_id}).json()['p_name']

    def edit(self, pid, area):
        file = pt.join(self.path, pid, "GameSettings.ini")
        config = ConfigParser()
        config.read(file)
        config['ONLINE']['DataCenterHint'] = area
        with open(file, mode='w') as f:
            config.write(f)


class GUI:
    def __init__(self):
        try:
            """
            Initialize ui
            """
            self.app = QApplication([])
            try:
                Form, Base = uic.loadUiType(pt.join(_MEIPASS, 'files/MainWindow.ui'))
            except Exception as e:
                self.alert(e)
                return
            # Base Qt app
            # initialize form from .ui file
            self.form = Form()
            # base app from .ui file
            self.base = Base()
            try:
                self.icon = QtGui.QIcon(pt.join(_MEIPASS, 'files/icon.ico'))
            except Exception:
                self.icon = QtGui.QIcon()
            self.form.setupUi(self.base)
            # Combobox for areas
            self.area = self.form.area
            # Combobox for username
            self.username = self.form.username
            # Initialize ServerSwitcher
            self.ss = ServerSwitcher(path=ServerSwitcher.normal_path)
            self.area.addItems([x.upper() for x in ServerSwitcher.areas])
            # Player ID, assigned by ubi. Use r6tab api to get username
            self.pids = [x for x in self.ss.get_pids()]
            self.username.addItem("All")
            self.username.addItems(self.pids)
            # Switch button. When clicked call self.switch
            self.form.switch_btn.clicked.connect(self.switch)
            # Open folder button. When clicked call a lambda function that open the directory of config folders w/ file explorer
            self.form.open_folder.clicked.connect(lambda: startfile(self.ss.path))
            # Help TODO
            self.form.help.clicked.connect(lambda: self.message("TODO"))
            # Show UI
            self.base.show()
            try:
                for i in range(2, self.username.count()):
                    self.username.setItemText(i, ServerSwitcher.get_username(self.username.itemText(i)))
            except Exception as e:
                self.alert(e)
            # Start running the app. When exit the app, exit the entire program safely
            exit(self.app.exec_())
        except Exception as e:
            self.alert(e)

    def alert(self, txt, title="Alert"):
        """
        Show a message box w/ alert message
        :param txt: message to be displayed
        :param title:
        :return: None
        """
        self.message(txt, title)

    def message(self, txt, title="Message"):
        """
        Show a message box w/ normal message
        :param txt: message to be displayed
        :param title:
        :return: None
        """
        msg = QMessageBox()
        try:
            msg.setWindowIcon(self.icon)
        except Exception:
            pass
        msg.setWindowTitle(title)
        msg.setText(str(txt))
        msg.exec_()

    def switch(self):
        try:
            area_index = self.area.currentIndex()
            user_index = self.username.currentIndex()
            if area_index == 0:
                self.alert("Please choose an Area / 请选择地区")
                return
            else:
                area = self.ss.areas[self.area.currentIndex() - 1]
            if user_index == 0:
                self.alert("Please choose an account / 请选择账户")
                return
            elif user_index == 1:
                for pid in self.pids:
                    self.ss.edit(pid, area)
            else:
                self.ss.edit(self.pids[user_index - 2], area)
            self.message("Success / 成功")
        except Exception as e:
            self.alert(e)


GUI()
