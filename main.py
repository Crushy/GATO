import sys

from PySide.QtCore import *
from PySide.QtGui import QSystemTrayIcon, QMenu, QAction, qApp, QApplication, QWidget, QIcon, QStyle, QMessageBox

import yaml


class SystemTrayIcon(QSystemTrayIcon):
    """
    GATO - Gamedev Auxiliary TOol
    Mostly sits on your taskbar, wasting a few resources and looking pretty. Occasionally it may turn out to be useful (like it's namesake)
    """

    def __init__(self, icon, tasks, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        menu.setContextMenuPolicy(Qt.ActionsContextMenu)

        for task in tasks:
            task1_action = QAction(task.name, self)
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


# TODO mark this as a safe object
class Task:
    def __init__(self, name, command):
        self.name = name
        self.command = command

    def __repr__(self):
        return "Task: \nname: " + self.name + "\ncommand(s): " + self.command


def main():
    config_file = None
    try:
        config_stream = open("config.yaml")
        print("Loaded config file")
    except FileNotFoundError as e:
        print("Couldn't load config file: {0}".format(e.strerror))
        sys.exit(-1)

    config_file = yaml.load(config_stream)

    tasks = config_file[0:]
    for task in config_file:
        # print("-  ")
        print(task)
        print("\n")
    # print( yaml.dump(config_file) )

    # sys.exit(0)
    app = QApplication(sys.argv)

    #app.setAttribute(Qt.AA_DontShowIconsInMenus, False)

    w = QWidget()
    print(tasks)
    tray_icon = SystemTrayIcon(QIcon("logo.xpm"), tasks, w)

    tray_icon.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()