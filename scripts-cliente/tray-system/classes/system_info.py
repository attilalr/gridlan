__author__ = 'Ildar Shirshov'
__copyright__ = 'Copyright 2015, The Tray Watcher Project'

__license__ = 'Unknown'
__version__ = '0.0.1'
__email__ = 'ildar-shirshov@ya.ru'
__status__ = 'Non-production'

import socket
import locale
import sys
import os, subprocess
from random import randint

from PyQt4 import QtGui, QtCore

from classes.password_window import PasswordWindow

class SystemInfo(QtGui.QFrame):
    def __init__(self, image_dir, script_dir, menu,parent=None):
        super(SystemInfo, self).__init__(parent)

        self.__trust_hostnames = ['www.google.com', 'www.amazon.com',
                                  'www.yahoo.com', 'www.ya.ru']

        self.__status_images = {'ok': image_dir + '/ok.png',
                                'warn': image_dir + '/warn.png',
                                'error': image_dir + '/error.png'}

        if sys.platform == "win32":
            self.__script_names = {'network': script_dir + '/network.bat',
                                   'vm': script_dir + '/vm.bat'}
        elif sys.platform == "linux2":
            self.__script_names = {'network': script_dir + '/network.sh',
                                   'vm': script_dir + '/vm.sh'}

        ### Guest name 
	if 'win' in sys.platform.lower():
		self.server_name=os.popen('more "%programfiles%\gridlocal\hostname.txt"').read()[:-1]
	if 'linux' in sys.platform.lower():
		self.server_name=os.popen("cat /opt/gridlocal/host").read()[:-1]
        self.image_dir = image_dir
        self.menu = menu

        # Convert paths to preferable encoding.
        for key, value in self.__status_images.iteritems():
            self.__status_images[key] = value.decode(locale.getpreferredencoding())
        for key, value in self.__script_names.iteritems():
            self.__script_names[key] = value.decode(locale.getpreferredencoding())

	self.running_processes=0

        self.__update_interval = 100
        self.__timer_id = None
        self.__window_size = QtCore.QSize(220, 130)

        self.__host_label = QtGui.QLabel(self)
        self.__vmstatus_label = QtGui.QLabel(self)
        self.__network_label = QtGui.QLabel(self)
        self.__jobs_label = QtGui.QLabel(self)
        self.__bitmap_label = QtGui.QLabel(self)

        groupbox_stylesheet = 'QGroupBox { border: 1px solid grey; border-radius: 0px; margin-top: 6px; } ' \
                              'QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; }'

        # Setup layouts for SystemInfo class
        status = QtGui.QGroupBox(self)
        status_layout = QtGui.QVBoxLayout()
        status_layout.addWidget(self.__bitmap_label)
        status.setStyleSheet(groupbox_stylesheet)
        status.setLayout(status_layout)
        status.setTitle('Status')

        info = QtGui.QGroupBox(self)
        info_layout = QtGui.QVBoxLayout()
        info_layout.addWidget(self.__host_label)
        info_layout.addWidget(self.__vmstatus_label)
        info_layout.addWidget(self.__network_label)
        info_layout.addWidget(self.__jobs_label)
        info.setStyleSheet(groupbox_stylesheet)
        info.setLayout(info_layout)
        info.setTitle('Info')

        spacer_layout = QtGui.QVBoxLayout()
        spacer_layout.addWidget(status)
        spacer_layout.addSpacerItem(QtGui.QSpacerItem(0, 10, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))

        horizontal_lyt = QtGui.QHBoxLayout()
        horizontal_lyt.addLayout(spacer_layout)
        horizontal_lyt.addWidget(info)

        self.setLayout(horizontal_lyt)
        self.setFixedSize(self.__window_size)

        self.setStyleSheet('.SystemInfo { border: 2px solid grey; border-radius: 5px; background-color: white; }')
        self.checkAllStatus()

    def networkStatus(self):
#        for hostname in self.__trust_hostnames:
#            try:
#                host = socket.gethostbyname(hostname)
#                sock_conn = socket.create_connection((host, 80), 2)
#                return 'on'
#            except:
#                pass
#
#        return 'off'
        if (os.popen("ps aux|grep 'openvpn --config /opt/gridloca[l]/'").read()[:-1]!=''):
          return 'on'
        else:
          return 'off'

    def vmStatus(self):
        if (os.popen("virsh list|grep "+self.server_name).read()[:-1]!=''):
          return 'on'
        else: 
          return 'off'

    def jobsStatus(self):

	flag=0
	running_process=0

	try:
		c = zerorpc.Client()
		c.connect('tcp::/143.54.155.233:4242')
		c.chk_stats(self.server_name)
		flag=1
	except:
		flag=0

	if (flag==1):
	        running_process = int(c.chk_stats(self.server_name))  
        	self.running_processes = c.chk_stats(self.server_name)
		c.close()

        return running_process 

    def checkAllStatus(self):
        nt_status = self.networkStatus()
        vm_status = self.vmStatus()

        if len(self.__status_images):
            pixmap = QtGui.QPixmap(self.__status_images['warn' if nt_status == 'off' or vm_status == 'off' else 'ok'])
            self.__bitmap_label.setPixmap(pixmap.scaled(self.__window_size / 4, QtCore.Qt.KeepAspectRatio))
        else:
            self.setText('No images founded!', self.__bitmap_label)

        self.setText('Noh: %s' % self.server_name, self.__host_label)
        self.setText('VPN: %s' % nt_status, self.__network_label)
        self.setText('VM: %s' % vm_status, self.__vmstatus_label)
        self.setText('Processos: %s' % self.jobsStatus(), self.__jobs_label)

#        if nt_status == 'off':
#            self.somethingDown('network')
#        if vm_status == 'off':
#            self.somethingDown('vm')

        self.reformmenu()

    def somethingDown(self, reason_text):
#        script = self.__script_names[reason_text]
        msg_box = QtGui.QMessageBox()

        msg_box.setText('The status of %s down.' % reason_text)
        msg_box.setInformativeText('Do you want to restart %s?' % reason_text)
        msg_box.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)

        button = msg_box.exec_()
        if QtGui.QMessageBox.Ok == button:
            pass_win = PasswordWindow("/opt/gridlocal/script")
            pass_win.exec_()

    def timerEvent(self,event):
        if event.timerId() == self.__timer_id:
            self.checkAllStatus()

    def setText(self, str, label):
        if label is not None:  # TODO: Add convert function
            label.setText(str)

    def stopTimer(self):
        if self.__timer_id is not None:
            self.killTimer(self.__timer_id)
            self.__timer_id = 0

    def setTimerInterval(self, msec):
        if msec <= 0:
            self.stopTimer()
        else:
            self.stopTimer()
            self.__timer_id = self.startTimer(msec)

    def reformmenu(self,parent=None):

        self.menu.clear() 

        icon = QtGui.QIcon.fromTheme("computer-symbolic")
        self.menu.addAction(icon,'Noh: '+self.server_name)
        icon = QtGui.QIcon.fromTheme("emblem-synchronizing-symbolic")
        self.menu.addAction(icon,'Ping Servidor: '+self.pingserver())
        icon = QtGui.QIcon.fromTheme("emblem-shared-symbolic")
#        self.menu.addAction(icon,'VPN: '+self.networkStatus())
#        icon = QtGui.QIcon.fromTheme("preferences-other-symbolic")
#        self.menu.addAction(icon,'VM: '+self.vmStatus())
#        icon = QtGui.QIcon.fromTheme("utilities-system-monitor-symbolic")
        self.menu.addAction(icon,'Processos: '+str(self.running_processes))

#        self.menu.addSeparator()

#        if (self.networkStatus()=='off' or self.vmStatus()=='off'):
#          icon = QtGui.QIcon.fromTheme("view-refresh-symbolic")
#          restart_action = self.menu.addAction(icon,'Reiniciar servico')
#          self.menu.addSeparator()
#          restart_action.triggered.connect(self.restartservice)
#          restart_action.triggered.connect(self.somethingDown)

        icon = QtGui.QIcon.fromTheme("system-shutdown-symbolic")
        quit_action = self.menu.addAction(icon,'Fechar')
        quit_action.triggered.connect(QtGui.qApp.quit)

        self.__window = None

        if 'win' in sys.platform.lower():
          icon_name = self.image_dir + '\\icon2.png'
        if 'linux' in sys.platform.lower():
          icon_name = self.image_dir + '//icon2.png'
        print icon_name
        icon_name = icon_name.decode(locale.getpreferredencoding())


    def restartservice(self,parent=None):
        subprocess.call("gksudo /etc/init.d/gridlocal restart -g --sudo-mode -d --message 'Digite a sua senha sudo para reiniciar o servico Grilocal'", shell=True, executable='/bin/bash')

    def pingserver(self,parent=None):
	if 'win' in sys.platform.lower():
		ping = os.popen('ping -n 1 -w 1000 143.54.155.233').read()
		if ping.count('100%') == 1:
			return 'fail'
		if ping.count('100%') == 0:
			return 'ok'
	if 'linux' in sys.platform.lower():
	        ping = os.popen("ping -q -n -c1 -W1 143.54.155.233").read()
	        if (ping.find('max')!=-1):
	          return 'ok'
	        else:
	          return 'fail'
        
