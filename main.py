import sys

from PySide.QtCore import *
from PySide.QtGui import QSystemTrayIcon, QMenu, QAction, qApp, QApplication, QWidget, QIcon, QStyle, QMessageBox

import yaml


class SystemTrayIcon(QSystemTrayIcon):
    """
    GATO - Gamedev Auxiliary TOol
    Mostly sits on your taskbar, wasting a few resources and looking pretty. Occasionally it may turn out to be useful (like it's namesake)
    """
    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        menu.setContextMenuPolicy(Qt.ActionsContextMenu)

        task1_action = QAction("Task 1", self)
        task1_action.triggered.connect(self.execute_task)

        #Quit
        icon_quit = QIcon("process-stop.xpm")
        action_quit = QAction(icon_quit, "Quit", self)
        action_quit.triggered.connect(qApp.quit)

        icon_about = QIcon("help-browser.xpm")
        action_about = QAction(icon_about, "About", self)
        action_about.triggered.connect(self.about)

        menu.addActions([task1_action, action_about, action_quit])

        print("tet")
        self.setContextMenu(menu)

    def execute_task(self):
        print("Testing a task")

    def about(self):
        msg_box = QMessageBox()
        msg_box.setText("Made by Pedro Caetano")
        #TODO: this quits
        msg_box.exec_()

def main():

    try:
        #config_stream = open("config.yaml")
        #yaml.load(config_stream, Loader=yaml.CLoader)
        print("Loaded config file")
    except FileNotFoundError as e:
        print("Couldn't load config file: {0}".format(e.strerror))
        sys.exit(-1)

    app = QApplication(sys.argv)

    #app.setAttribute(Qt.AA_DontShowIconsInMenus, False)

    w = QWidget()
    tray_icon = SystemTrayIcon(QIcon("logo.xpm"), w)

    tray_icon.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()