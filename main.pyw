# -*- coding: utf-8 -*-

import sys
import traceback
import subprocess
import inspect

# TODO : Look into setuptools
def handle_missing_module(formalName, pipModuleName):
    print(formalName + " not found, trying to install")
    return_code = subprocess.call("pip install -U " + pipModuleName, shell=True)

    if return_code:
        print("Install Sucessful")
    else:
        print("Install Failed")

try:
    from PySide.QtCore import *
    from PySide.QtGui import QSystemTrayIcon, QMenu, QAction, qApp, QApplication, QWidget, QIcon, QStyle, QMessageBox, \
        QPushButton
except ImportError:
    handle_missing_module("PySide", "PySide")


class SystemTrayIcon(QSystemTrayIcon):
    """
    GATO - Gamedev Auxiliary TOol
    Mostly sits on your taskbar, wasting a few resources and looking pretty. Occasionally it may turn out to be useful (like it's namesake)
    """

    def __init__(self, icon, task_list, parent=None):
        #print(task_list)

        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        menu.setContextMenuPolicy(Qt.ActionsContextMenu)

        all_actions = []

        for single_task in task_list:
            transformedFunctionName = single_task[0].split("_")
            transformedFunctionName = ' '.join(str(x) for x in transformedFunctionName)
            task_action = QAction(transformedFunctionName, self)
            
            # "Localizes" single_task.command so we're not just using a reference to the last one we added
            #see http://stackoverflow.com/questions/233673/lexical-closures-in-python
            command = lambda z = single_task[1]: self.execute_task(z)

            task_action.triggered.connect(command)
            all_actions.append(task_action)

        menu.addActions(all_actions)

        #build help menu
        helpMenu = QMenu()
        helpMenu.setTitle("Help")
        helpMenu.setIcon(QIcon("help-browser.xpm"))

        # About GATO
        icon_about = QIcon("help-browser.xpm")
        action_about = QAction(icon_about, "About GATO", self)
        action_about.triggered.connect(self.about)
        #all_actions.append(action_about)
        helpMenu.addAction(action_about)

        # About QT
        icon_aboutQT = QIcon("help-browser.xpm")
        action_aboutQT = QAction(icon_about, "About QT", self)
        action_aboutQT.triggered.connect(self.aboutQT)
        #all_actions.append(action_aboutQT)
        helpMenu.addAction(action_aboutQT)

        menu.addSeparator()
        menu.addMenu(helpMenu)

        # Quit
        icon_quit = QIcon("process-stop.xpm")
        action_quit = QAction(icon_quit, "Quit", self)
        action_quit.triggered.connect(qApp.quit)

        menu.addAction(action_quit)

        self.setContextMenu(menu)

    def execute_task(self, command):

        try:
            #print("Executing:\n"+inspect.getsource(command)+"\n",flush=True)
            command()
        except :

            msg_box = QMessageBox()
            msg_box.setWindowTitle("Could not execute command")
            msg_box.setText("Failed to execute:\n " + inspect.getsource(command))

            # msg_box.setWindowIcon())
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setDetailedText(traceback.format_exc())

            button = QPushButton("Well, that sucks")
            button.clicked.connect(msg_box.close)

            msg_box.addButton(button, QMessageBox.AcceptRole)
            msg_box.exec_()

    def about(self):
        msg_box = QMessageBox.about(
            None,
            "About GATO",
            "GATO is an automation tool made by <a href='http://crushy.github.io/'>Pedro Caetano</a>")

    def aboutQT(self):
        msg_box = QMessageBox.aboutQt(None)


class Task:
    def __init__(self, name, command):
        self.name = name
        self.command = command

    def __repr__(self):
        return "Task: \nname: " + self.name + "\ncommand(s): " + self.command


def main():
    config_file = None
    try:
        config_stream = open("config.py")
        print("Loaded config file")
    except FileNotFoundError as e:
        print("Couldn't load config file: {0}".format(e.strerror))
        sys.exit(-1)


    import config as configModule
    all_functions = inspect.getmembers(configModule, inspect.isfunction)

    #sys.argv[0] = 'whatevernameyouwant'
    app = QApplication("GATO")

    #app.setAttribute(Qt.AA_DontShowIconsInMenus, False)
    logo_icon = QIcon("gato-icon.xpm")

    w = QWidget()
    # Important because otherwise closing any window would kill the tray icon
    app.setQuitOnLastWindowClosed(False)
    app.setWindowIcon(logo_icon)
    tray_icon = SystemTrayIcon(logo_icon, all_functions, w)

    tray_icon.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
