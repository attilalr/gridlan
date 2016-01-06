#!/usr/bin/python

__author__ = 'Ildar Shirshov'
__copyright__ = 'Copyright 2015, The Tray Watcher Project'

__license__ = 'Unknown'
__version__ = '0.0.1'
__email__ = 'ildar-shirshov@ya.ru'
__status__ = 'Non-production'

import os

from classes import *

def main():
    app = QtGui.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    image_dir = os.getcwd() + '/img'
    script_dir = os.getcwd() + '/bin'

    transp_box = TransparentBox()
    tray_watcher = TrayWatcher(image_dir)
    system_info = SystemInfo(image_dir, script_dir,tray_watcher.menu)

    transp_box.setMainWindow(system_info)
    system_info.setTimerInterval(8000)

    tray_watcher.setSystemInfoWindow(transp_box)
    tray_watcher.setVisible(True)

    tray_watcher.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
