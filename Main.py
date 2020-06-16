# import playsound
import sys, os
from PyQt5 import uic, QtWidgets


#############################################################################################################
#  Resource para o PyInstaller
def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def start_script():
    from autostart import autostart
    interface.hide()
    autostart()


def logatt():
    interface.hide()
    att.show()

def voltar():
    att.close()
    interface.show()



app = QtWidgets.QApplication([])
interface = uic.loadUi(resource_path('interface/desinglolbot.ui'))
att = uic.loadUi(resource_path('interface/att.ui'))
interface.pushButton.clicked.connect(start_script)
interface.pushButton_2.clicked.connect(logatt)
att.pushButton.clicked.connect(voltar)
interface.show()
app.exec()
