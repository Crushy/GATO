# -*- coding: utf-8 -*-

import sys, traceback,subprocess


# TODO : Look into setuptools
def handle_Missing_Module(formalName, pipModuleName):
    print(formalName + " not found, trying to install")
    return_code = subprocess.call("pip install -U " + pipModuleName, shell=True)

    if return_code:
        print("Sucessfully")
    else:
        print("Failed")


try :
	from PySide.QtCore import *
	from PySide.QtGui import QSystemTrayIcon, QMenu, QAction, qApp, QApplication, QWidget, QIcon, QStyle, QMessageBox, \
		QPushButton
except ImportError :
    handle_Missing_Module("PySide","PySide")
	

try :
	import yaml
except ImportError :
    handle_Missing_Module("yaml","pyyaml")



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

        for single_task in task_list:
            task_action = QAction(single_task.name, self)
            
            # "Localizes" single_task.command so we're not just using a reference to the last one we added
            #see http://stackoverflow.com/questions/233673/lexical-closures-in-python
            command = lambda z=single_task.command: self.execute_task(z)

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

        # TODO: handle some particularities about using the exec command and exceptions
        try:
            print(command)
            exec(command)
        except:

            msg_box = QMessageBox()
            msg_box.setWindowTitle("Could not execute command")
            msg_box.setText("Failed to execute:\n " + command)

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
    logo_icon = QIcon("trayIcon.xpm")
    
    w = QWidget()
    # Important because otherwise closing any window would kill the tray icon
    app.setQuitOnLastWindowClosed(False)
    app.setWindowIcon(logo_icon)
    tray_icon = SystemTrayIcon(logo_icon, tasks, w)

    tray_icon.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
