import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from check_addons import check_addons


class Wokno(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('417.RCT Launcher v0.1 ')\
        #verify that this works @Furi
        self.setWindowIcon(QIcon('../img/logo.ico'))
        self.setFixedSize(535, 370)

        tabwidget = QTabWidget()
        tabwidget.addTab(FirstTab(), "Main")
        tabwidget.addTab(SecondTab(), "Settings")
        tabwidget.addTab(ThirdTab(), "Custom mods")

        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(tabwidget)

        self.setLayout(vboxLayout)


class FirstTab(QWidget):
    def __init__(self):
        super().__init__()

        self.drop_down = QComboBox(self)
        self.drop_down.addItem("Official")
        self.drop_down.addItem("Training")
        self.drop_down.move(25, 40)
        self.drop_down.resize(100, 20)

        self.server_list = QCheckBox("Connect", self)
        self.server_list.move(42, 220)
        self.server_list.resize(320, 40)

        button1 = QPushButton("Check addons", self)
        button1.setToolTip("Kontrola aktuálnosti addonů")
        button1.resize(button1.sizeHint())
        button1.move(25, 65)
        button1.resize(100, 50)
        button1.setStyleSheet("Background-color:lightgrey")
        # button1.clicked.connect(lambda:self.run("config_manager.py"))
        button1.clicked.connect(self.start_process)
        # if      config_manager == 1
        button1.clicked.connect(self.local_path)
        #        print("gudas")
        # else: print("gud")
        # button1.clicked.connect(lambda:self.run("check_for_update.py"))

        button2 = QPushButton("Download/Pause",self)
        button2.setToolTip("Stahování i s programem můžeš kdykoliv přerušit")
        button2.resize(button2.sizeHint())
        button2.move(25, 120)
        button2.resize(100, 50)
        button2.setStyleSheet("Background-color:lightgrey")
        button2.clicked.connect(lambda: self.run("file_downloader.py"))              

        self.PROGRESS = QProgressBar(self)
        self.PROGRESS.setGeometry(10, 280, 520, 32)

        self.MODTEXTBOX = QLineEdit(self)
        self.MODTEXTBOX.move(140, 40)
        self.MODTEXTBOX.resize(150, 204)
        self.MODTEXTBOX.setReadOnly(True)

    def start_process(self):
        """On press of Check Addons button calls the function check_addons
        """
        check_addons()

    def local_path(self):
        print("zaznamenávám")

        # def filePath(self, fileName: str)
        # def CFG_MNG(self):
        # if addon_path_check == 1:
        # print("Nefunguje") '''


class SecondTab(QWidget):
    def __init__(self):
        super().__init__()


class ThirdTab(QWidget):
    def __init__(self):
        super().__init__()

        # self.setStyleSheet("background-color: #69884c;")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Wokno = Wokno()
    Wokno.show()
    app.exec()

'''
check_if_config_exists - jestli je nebo není, když není, okno s cestou


check update vrací true(1) když je update

když je true, tak to pustí update_addons



repository věc - zepátám se znovu
https://a3.417rct.org/addons/a_debilek_roku_vyhrava_duchy.csv
'''
