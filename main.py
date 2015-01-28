import sys, traceback

from PySide.QtCore import *
from PySide.QtGui import QSystemTrayIcon, QMenu, QAction, qApp, QApplication, QWidget, QIcon, QStyle, QMessageBox, \
    QPushButton

import yaml


class SystemTrayIcon(QSystemTrayIcon):
    """
    GATO - Gamedev Auxiliary TOol
    Mostly sits on your taskbar, wasting a few resources and looking pretty. Occasionally it may turn out to be useful (like it's namesake)
    """

    def __init__(self, icon, task_list, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        menu.setContextMenuPolicy(Qt.ActionsContextMenu)

        all_actions = []

        def gen_task(j):
            def func():
                self.execute_task(j)

            return func

        for single_task in task_list:
            task_action = QAction(single_task.name, self)

            command = gen_task(single_task.command)

            task_action.triggered.connect(command)
            all_actions.append(task_action)

        icon_about = QIcon("help-browser.xpm")
        action_about = QAction(icon_about, "About", self)
        action_about.triggered.connect(self.about)
        all_actions.append(action_about)

        # Quit
        icon_quit = QIcon("process-stop.xpm")
        action_quit = QAction(icon_quit, "Quit", self)
        action_quit.triggered.connect(qApp.quit)
        all_actions.append(action_quit)

        menu.addActions(all_actions)

        self.setContextMenu(menu)

    def execute_task(self, command):

        # TODO: handle some particularities about using the exec command and exceptions
        try:
            print(command)
            exec(command)
        except:

            msg_box = QMessageBox()

            msg_box.setText("Could not execute command: " + command)

            # msg_box.setWindowIcon())
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setDetailedText(traceback.format_exc())

            button = QPushButton("Well, fuck me then")
            button.clicked.connect(msg_box.close)

            msg_box.addButton(button, QMessageBox.AcceptRole)
            msg_box.exec_()



    def about(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("About GATO")
        msg_box.setIcon(QMessageBox.Information)

        msg_box.setText("GATO was made by Pedro Caetano")

        button = QPushButton("Indeed")
        button.clicked.connect(msg_box.close)

        msg_box.addButton(button, QMessageBox.AcceptRole)

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
    import sys

    sys.argv[0] = 'whatevernameyouwant'
    app = QApplication("GATO")

    #app.setAttribute(Qt.AA_DontShowIconsInMenus, False)
    logo_icon = QIcon("logo.xpm")
    
    w = QWidget()
    # Important because otherwise closing any window would kill the tray icon
    app.setQuitOnLastWindowClosed(False)
    app.setWindowIcon(logo_icon)
    tray_icon = SystemTrayIcon(logo_icon, tasks, w)

    tray_icon.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()