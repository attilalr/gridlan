__author__ = 'Ildar Shirshov'
__copyright__ = 'Copyright 2015, The Tray Watcher Project'

__license__ = 'Unknown'
__version__ = '0.0.1'
__email__ = 'ildar-shirshov@ya.ru'
__status__ = 'Non-production'

from PyQt4 import QtGui, QtCore


class TransparentBox(QtGui.QWidget):
    def __init__(self, parent=None):
        super(TransparentBox, self).__init__(parent)

        self.__main_layout = QtGui.QGridLayout(self)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)
        self.__main_window = None

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.Popup | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

    def setMainWindow(self, window):
        if (self.__main_window is not None):
            self.__main_layout.removeWidget(self.__main_window)
            self.__main_window = None

        self.setFixedSize(window.size())
        self.__main_layout.addWidget(window)
        self.__main_window = window
