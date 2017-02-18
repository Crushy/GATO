GATO - Gamedev Auxiliary TOol
====

 ![Example Usage](./docs/demo/gato_v0.1.gif)
  
  GATO mostly sits on your taskbar, wasting a few resources and looking pretty. Occasionally it may turn out to be useful (like it's namesake).
  
  Right clicking on it will display a list of automated tasks, which are read from a python file. 
  
  These tasks can be quite useful for game development and may include:
  * Link to your Issues page
  * Go to your current project's wiki
  * Pull changes from several repositories
  * Open your entire work toolset 
  * Setup a newly-formated PC for work
  * etc

How to make new tasks
=====================

Simply edit the config.py file and add new functions. The function name will be the name on the task list. Underscores will be replaced with spaces.

Prerequisites
=============
  * Pyside
  * Python 3.4.3
  * You can open up the project file using PyCharm

TODO
====

Dev Notes
========

The main idea behind GATO was to allow non-programmers to easily perform certain functions and make everything 
Inspired by [this blog post](http://blog.spaceduststudios.com/tools-and-processes-for-remote-game-development-part-2-collaboration).
