__author__ = 'Ildar Shirshov'
__copyright__ = 'Copyright 2015, The Tray Watcher Project'

__license__ = 'Unknown'
__version__ = '0.0.1'
__email__ = 'ildar-shirshov@ya.ru'
__status__ = 'Non-production'

import sys
import signal
import locale

from PyQt4 import QtGui, QtCore


class TrayWatcher(QtGui.QSystemTrayIcon):
    def __init__(self, image_dir, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, parent)

        self.menu = QtGui.QMenu(parent)

#        icon = QtGui.QIcon.fromTheme("computer-symbolic")
#        info_action = self.menu.addAction(icon,'Abrir info')
#        info_action.triggered.connect(self.activatedEvent)

#        self.menu.addSeparator()

#        icon = QtGui.QIcon.fromTheme("computer-symbolic")
#        self.menu.addAction(icon,'Noh:')
#        icon = QtGui.QIcon.fromTheme("emblem-shared-symbolic")
#        self.menu.addAction(icon,'VPN:')
#        icon = QtGui.QIcon.fromTheme("preferences-other-symbolic")
#        self.menu.addAction(icon,'VM:')
#        icon = QtGui.QIcon.fromTheme("utilities-system-monitor-symbolic")
#        self.menu.addAction(icon,'Processos:')

#        self.menu.addSeparator()

        icon = QtGui.QIcon.fromTheme("system-shutdown-symbolic")
        quit_action = self.menu.addAction(icon,'Fechar')
        quit_action.triggered.connect(QtGui.qApp.quit)

        #menu.clear() 

        #self.activated.connect(self.activatedEvent)

        self.__window = None
        icon_name = image_dir + '/icon2.png'
        icon_name = icon_name.decode(locale.getpreferredencoding())

        # Register termination signals
        if (sys.platform == "win32"):
            self.__signals = {signal.SIGTERM: 'terminate', signal.SIGBREAK: 'close', signal.SIGINT: 'quit'}
        elif (sys.platform == "linux2"):
            self.__signals = {signal.SIGTERM: 'terminate', signal.SIGHUP: 'close', signal.SIGQUIT: 'quit'}

        for key, val in self.__signals.iteritems():
            signal.signal(key, self.signalHandler)
         
        # Setup tray icon
        self.setIcon(QtGui.QIcon(icon_name))
        self.setContextMenu(self.menu)

    def setSystemInfoWindow(self, window):
        self.__window = window

    def activatedEvent(self, reason):
#        if (reason in (QtGui.QSystemTrayIcon.Trigger, QtGui.QSystemTrayIcon.DoubleClick)):
            if ((self.__window is not None) and (not self.__window.isVisible())):
                # Before show the info window,
                # need correct geometry of window for all corners.
                tray_geometry = self.geometry()
                tray_position = tray_geometry.center()
                available_screen = (QtGui.QApplication.desktop()).availableGeometry(tray_position)

                center_x = available_screen.width() / 2
                center_y = available_screen.height() / 2

                tray_x = tray_position.x()
                tray_y = tray_position.y()
#                tray_x = 500
#                tray_y = 22

                window_geometry = self.__window.geometry()
                window_geometry.moveCenter(QtCore.QPoint(center_x, center_y))
#                print "tray: %s %s" % (self.geometry(),tray_geometry.center())
#                print "avail screen: %s" % (available_screen)
#                print "avail screen width: %s" % (available_screen.width())
#                print "avail screen height: %s" % (available_screen.height())

                if tray_y < center_y:
                    window_geometry.moveTop(tray_y + tray_geometry.width())
                if tray_y > center_y:
                    window_geometry.moveBottom(tray_y - tray_geometry.width())

                if tray_x < center_x:
                    window_geometry.moveRight(tray_x + (window_geometry.width() / 2))
                elif tray_x > center_x:
                    window_geometry.moveLeft(tray_x - (window_geometry.width() / 2))

                self.__window.setGeometry(window_geometry)
                self.__window.show()

    def signalHandler(self, signum, frame):
        msg_box = QtGui.QMessageBox()

        msg_box.setText('Receive %s signal.' % self.__signals[signum])
        msg_box.setInformativeText('Do you want to abort?')
        msg_box.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)

        button = msg_box.exec_()
        if (QtGui.QMessageBox.Ok != button):
            sys.exit(0)

        self.abortSignal()

    def abortSignal(self):
        pass  # Here your script 'init 5'
