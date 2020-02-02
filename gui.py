from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import (QApplication, QMessageBox)
from ServerSwitch import ServerSwitcher as SS
from os import startfile
from sys import exit


class GUI:
    def __init__(self):
        try:
            """
            Initialize ui
            """
            Form, Base = uic.loadUiType("MainWindow.ui")
            # Base Qt app
            self.app = QApplication([])
            # initialize form from .ui file
            self.form = Form()
            # base app from .ui file
            self.base = Base()
            self.icon = QtGui.QIcon('3d-printable-rainbow-six-siege-icons-3d-model-stl.jpg')
            self.form.setupUi(self.base)
            # Combobox for areas
            self.area = self.form.area
            # Combobox for username
            self.username = self.form.username
            # Initialize ServerSwitcher
            self.ss = SS(path=SS.normal_path)
            self.area.addItems([x.upper() for x in SS.areas])
            # Player ID, assigned by ubi. Use r6tab api to get username
            self.pids = [x for x in self.ss.get_pids()]
            self.username.addItem("All")
            try:
                self.username.addItems([SS.get_username(x) for x in self.pids])
            except Exception:
                self.username.addItems(self.pids)
            # Switch button. When clicked call self.switch
            self.form.switch_btn.clicked.connect(self.switch)
            # Open folder button. When clicked call a lambda function that open the directory of config folders w/ file explorer
            self.form.open_folder.clicked.connect(lambda: startfile(self.ss.path))
            # Help TODO
            self.form.help.clicked.connect(lambda: self.message("TODO"))
            # Show UI
            self.base.show()
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
        msg.setWindowIcon(self.icon)
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
