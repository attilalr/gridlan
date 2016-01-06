__author__ = 'Ildar Shirshov'
__copyright__ = 'Copyright 2015, The Tray Watcher Project'

__license__ = 'Unknown'
__version__ = '0.0.1'
__email__ = 'ildar-shirshov@ya.ru'
__status__ = 'Non-production'


from PyQt4 import QtGui, QtCore


class PasswordWindowBase(QtGui.QDialog):
    widgetClosed = QtCore.pyqtSignal()
    executive_cmd = None

    def __init__(self, parent=None):
        super(PasswordWindowBase, self).__init__(parent)

        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

    def closeEvent(self, event):
        self.widgetClosed.emit()
