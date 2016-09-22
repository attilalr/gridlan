__author__ = 'Ildar Shirshov'
__copyright__ = 'Copyright 2015, The Tray Watcher Project'

__license__ = 'Unknown'
__version__ = '0.0.1'
__email__ = 'ildar-shirshov@ya.ru'
__status__ = 'Non-production'

import os
import locale

from PyQt4 import QtGui, QtCore

from base import PasswordWindowBase


class PasswordWindow(PasswordWindowBase):
    def __init__(self, script_name, parent=None):
        super(PasswordWindow, self).__init__(parent)

        if script_name is None:
            raise Exception('Script name can\'t be null.')
        if not os.path.exists(script_name):
            raise Exception('Can\'t find script.')

        self.__script_name = script_name
        self.__script_name = self.__script_name.decode(locale.getpreferredencoding())
        self.__box = QtGui.QLineEdit(self)
        self.__visible = QtGui.QCheckBox(self)
        self.__request_button = QtGui.QPushButton(self)

        self.__visible.setText('Show password')
        self.__box.setEchoMode(QtGui.QLineEdit.Password)
        self.__request_button.setText('OK')

        layout = self.layout()
        layout.addWidget(self.__box)
        layout.addWidget(self.__visible)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.addSpacerItem(QtGui.QSpacerItem(0, 10, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))
        button_layout = QtGui.QHBoxLayout()
        button_layout.addSpacerItem(QtGui.QSpacerItem(0, 10, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))
        button_layout.addWidget(self.__request_button)
        button_layout.addSpacerItem(QtGui.QSpacerItem(0, 10, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))
        layout.addLayout(button_layout)

        self.__visible.stateChanged.connect(self.changeEchoMode)
        self.__request_button.clicked.connect(self.readPassword)
        self.__request_button.clicked.connect(self.hide)
        self.setWindowTitle('Password')

    def changeEchoMode(self, state):
        if state == QtCore.Qt.Unchecked:
            self.__box.setEchoMode(QtGui.QLineEdit.Password)
        elif state == QtCore.Qt.Checked:
            self.__box.setEchoMode(QtGui.QLineEdit.Normal)

    def readPassword(self):
        passw = self.__box.text()
        self.executive_cmd = "echo {0} | sudo -S {1}".format(passw, self.__script_name)

        if self.executive_cmd is not None:
            cmd = os.popen(self.executive_cmd)
            output = cmd.read()  # TODO: Output text of external script