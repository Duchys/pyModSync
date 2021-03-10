# Duchy seš blbeček, co to po mně chceš za píčoviny, mám jeden semestr programování v C#, a tohl hlavně proto, abych to uměl zhruba číst, proč s takovými věcmi obtěžuje mě, ale máš to mít, bude to trvat 10 let, ty se zhroutíš, 417 se rozpadne mezitím, a já tohle v životě nikdy nevyužiju, WIN WIN


from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys



       
        
        

class Wokno(QWidget):

    def __init__(self):
        super().__init__()       
#Jednotlivá okna

    layout = QGridLayout()
        self.setLayout(layout)
        label1 = QLabel("")
        label2 = QLabel("")
        label3 = QLabel("")
        tabwidget = QTabWidget()
        tabwidget.addTab(label1, "Main")
        tabwidget.addTab(label2, "Settings")
        tabwidget.addTab(label3, "Custom mods")    
        layout.addWidget(tabwidget, 0, 0)
  
        Dropdown = QComboBox(self)
        Dropdown.addItem("Server1")
        Dropdown.addItem("Server2")
        Dropdown.move(25, 40)
        Dropdown.resize (100,20)
        
        ServerList = QCheckBox("Connect",self)
        ServerList.move(42,220)
        ServerList.resize(320,40)

        button1 = QPushButton("Check addons",self)
        button1.setToolTip("Kontrola aktuálnosti addonů")
        button1.resize(button1.sizeHint())
        button1.move(25,65)
        button1.resize (100,50)
        button1.setStyleSheet("Background-color:lightgrey")
        
        button2 = QPushButton("Download/Pause",self)
        button2.setToolTip("Stahování i s programem můžeš kdykoliv přerušit")
        button2.resize(button2.sizeHint())
        button2.move(25,120)
        button2.resize (100,50)
        button2.setStyleSheet("Background-color:lightgrey")
        
        button3 = QPushButton("Start",self)
        button3.setToolTip("Spustit hru")
        button3.resize(button3.sizeHint())
        button3.move(25,175)
        button3.resize (100,50)
        button3.setStyleSheet("Background-color:lightgrey")

        self.PROGRESS = QProgressBar(self)
        self.PROGRESS.setGeometry(10, 280, 520, 32)
        
        self.MODTEXTBOX = QLineEdit(self)
        self.MODTEXTBOX.move(140, 40)
        self.MODTEXTBOX.resize(150,204)
        self.MODTEXTBOX.setReadOnly(True)
        
        #self.setStyleSheet("background-color: #69884c;")
#Menu



    
        
      
#Centrování     
        self.center()
    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

#Okno    
        self.setWindowIcon(QIcon('logo.ico'))
        self.setWindowTitle('417.RCT Launcher v0.1 ')
        self.setFixedSize(507, 320)
        
        self.show()

        

def main():

    app = QApplication(sys.argv)
    ex = Wokno()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()