# Spring 2024 UML Editor
#### Authored by: LamdaLegion (Sprint 3), CWorld (Sprint 1 & 2) 

This readme contains the steps to launch the **Spring 2024 UML Editor**. This is a GUI/terminal based program that allows users to create a Class Diagram with Relations, Classes, and Attributes.

# Setup Your Environment
<B>The minimum required version of Python to run this program is 3.8. If your version of python, found in the section below, is less than that, please follow [this](https://www.python.org/downloads/) link to install a newer version. </B>

## Check that Python is Installed

### MacOS
<ol>
<li> In the top right corner of your screen, there will be a search bar, a magnifying glass, or both (depending on your version of Mac). Click that.
<li> Type 'terminal', then hit enter.
<li> Type 'python3 --version' and hit enter. If you don't have developer tools installed, accept the install and wait for it to complete before retyping this command.
<li> The terminal will print out "Python x.x.x", where x is a number, if python is installed.
</ol>

### Windows
<ol>
<li> Hold the windows key and click R.
<li> Type 'cmd' and hit enter
<li> Type 'py -V' and hit enter
<li> "Python x.x.x" will print if python is installed.
</ol>

### Linux
<ol>
<li> Open a terminal on your preferred Linux distro.
<li> Type 'python --version'
<li> "Python x.x.x" will print if python is installed.
</ol>

## Install Python
If you do not have python installed, install the latest version for your operating system [here](https://www.python.org/downloads/).

# Download the Project

### In a Terminal
To download the project directly into a terminal, git tools will be required. Follow the instructions [here](https://github.com/git-guides/install-git) to install git if it is not already installed.

### In a Desktop Environment
Download the zip [here](https://github.com/mucsci-students/2024sp-420-CWorld/archive/refs/heads/main.zip) and extract it.


# Build the Project

Regardless of operating system, this project will install dependencies when it is built. If the build script is run outside a virtual environment, it may modify files on your computer unpredictably. To setup a virtual environment, follow [this link](https://docs.python.org/3/library/venv.html).

**The command to execute a python program varies with operating system. On Mac, it is python3. On Windows both py and python work. On Linux it is python. Through the duration of these build instructions, py will be used. Substitute the command appropriate for your operating system in its place.**

<ol>
<li> Open a terminal and navigate to the folder that the project was cloned/extracted into. Basics of terminal navigation can be found at the links listed below this list. 
<li> Once you are in the source directory of the project (its name should be 2024sp-420-PythonA), type 'py build.py'. If you get a warning about not being in a virtual environment, hit enter to exit the script then follow the instructions at the top of this section to setup and enter a virtual environment before running 'py build.py' again.
<li> Type 'py main.py' to run the program in its default mode, or refer to the flags section below this for other options.
</ol>

[Mac Terminal Navigation](https://www.macworld.com/article/221277/command-line-navigating-files-folders-mac-terminal.html) \
[Windows PowerShell Navigation](https://wiki.communitydata.science/Windows_terminal_navigation) \
[Windows Command Prompt Navigation](https://www.digitalcitizen.life/command-prompt-how-use-basic-commands/) \
[Linux Terminal Navigation](https://www.linode.com/docs/guides/linux-navigation-commands/)

### Operation modes
- `'py main.py'       - default operation mode, opens a GUI.
- `'py main.py cli'   - runs the program in CLI mode instead of creating a gui.
- `'py main.py debug' - runs the program in CLI debug mode. This mode is nearly identical to the CLI mode, just with slightly less error handling. Use at your own risk.

### Keyboard Shortcut in CLI mode
* 'Ctrl+z' for undo.
* 'Ctrl+y' for redo.
* 'Up' and 'Down' for navigating through the history of input commands.



**If you are in the CLI mode, type 'help' for a list of commands.**
**In the gui, use the menu options available at the top of the screen and/or by right clicking to manipulate the diagram to your needs**

### Test the project
'pytest'         - from the source directory of the project, automatically finds and executes all test files.

## Design Patterns

* Momento
  * The momento.py file, which is located in src/umleditor/mvc_controller, implements the Momento design pattern.
* Singleton
  * The diagram.py file, which is located in src/umleditor/mvc_model, implements the Singleton design pattern.
* Controller
  * The controller.py file, which is located in src/umleditor/mvc_controller, implements the Controller design pattern.
* Strategy
  * The autofill.py file, which is located in src/umleditor/mvc_controller, implements the Strategy design pattern. 
* Command
  * The main.py file, which is located in the root directory of the project, implements the Command design pattern.
* MVC
  *  MVC pattern is clearly organized into three separate directories under src/umleditor.
## Authors

#### LamdaLegion 

- Zhang Chen
- Jillian Daggs
- Katie Dowlin
- Patrick McCullough
- Danish Zubari

#### CWorld

- Ganga Acharya
- Marshall Feng
- Peter Freedman
- Adam Glick-Lynch
- Tim Moser
