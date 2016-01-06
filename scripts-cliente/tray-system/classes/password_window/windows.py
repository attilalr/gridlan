__author__ = 'Ildar Shirshov'
__copyright__ = 'Copyright 2015, The Tray Watcher Project'

__license__ = 'Unknown'
__version__ = '0.0.1'
__email__ = 'ildar-shirshov@ya.ru'
__status__ = 'Non-production'

import os
import locale
from subprocess import Popen

from base import PasswordWindowBase


class PasswordWindow(PasswordWindowBase):
    def __init__(self, script_name, parent=None):
        super(PasswordWindow, self).__init__(parent)

        if script_name is None:
            raise Exception('Script name can\'t be null.')
        if not os.path.exists(script_name):
            raise Exception('Can\'t find script.')

        self.setVisible(False)
        self.executive_cmd = "%s" % script_name
        self.executive_cmd = self.executive_cmd.decode(locale.getpreferredencoding())

    def exec_(self):
        if self.executive_cmd is not None:      # TODO: Get adming rights
            p = Popen(self.executive_cmd)
            (output, err) = p.communicate()     # TODO: Output text of external script