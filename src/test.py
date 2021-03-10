import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *




class Wokno(QDialog):
    def __init__(self):
                super().__init__()

                self.setWindowTitle('417.RCT Launcher v0.1 ')
                self.setWindowIcon(QIcon('logo.ico'))
                self.setFixedSize(535, 370)
        
                tabwidget = QTabWidget()
                tabwidget.addTab(FirstTab(),"Main")
                tabwidget.addTab(SecondTab(),"Settings")
                tabwidget.addTab(ThirdTab(),"Custom mods")

                vboxLayout = QVBoxLayout()
                vboxLayout.addWidget(tabwidget)

                self.setLayout(vboxLayout)
        
        
class FirstTab(QWidget):     
        def __init__(self):
                super().__init__()    
                
                
                
                
                self.Dropdown = QComboBox(self)
                self.Dropdown.addItem("Official")
                self.Dropdown.addItem("Training")
                self.Dropdown.move(25, 40)
                self.Dropdown.resize (100,20)
                
                self.ServerList = QCheckBox("Connect",self)
                self.ServerList.move(42,220)
                self.ServerList.resize(320,40)

                button1 = QPushButton("Check addons",self)
                button1.setToolTip("Kontrola aktuálnosti addonů")
                button1.resize(button1.sizeHint())
                button1.move(25,65)
                button1.resize (100,50)
                button1.setStyleSheet("Background-color:lightgrey")
                #button1.clicked.connect(lambda:self.run("config_manager.py"))
                button1.clicked.connect(self.start_process)
                #if      config_manager == 1
                button1.clicked.connect(self.LocalPath)
                #        print("gudas")
                #else: print("gud")
                #button1.clicked.connect(lambda:self.run("check_for_update.py"))
                
                button2 = QPushButton("Download/Pause",self)
                button2.setToolTip("Stahování i s programem můžeš kdykoliv přerušit")
                button2.resize(button2.sizeHint())
                button2.move(25,120)
                button2.resize (100,50)
                button2.setStyleSheet("Background-color:lightgrey")
                button2.clicked.connect(lambda:self.run("file_downloader.py"))              
                
                button3 = QPushButton("Start",self)
                button3.setToolTip("Spustit hru")
                button3.resize(button3.sizeHint())
                button3.move(25,175)
                button3.resize (100,50)
                button3.setStyleSheet("Background-color:lightgrey")
                button3.clicked.connect(self.Test)

                self.PROGRESS = QProgressBar(self)
                self.PROGRESS.setGeometry(10, 280, 520, 32)
                
                self.MODTEXTBOX = QLineEdit(self)
                self.MODTEXTBOX.move(140, 40)
                self.MODTEXTBOX.resize(150,204)
                self.MODTEXTBOX.setReadOnly(True)

        def start_process(self):
                from config_manager import check_if_config_exists 
                check_if_config_exists()
           
                '''print("zapisuji URL")
                remote_repository_url = "https://a3.417rct.org/addons/a_debilek_roku_vyhrava_duchy.csv"
        '''
        def LocalPath(self):
              
                local_addon_path = QFileDialog.getExistingDirectory(self, 'Vyber složku, kde chceš mít addony!')
                
                print("zaznamenávám "+local_addon_path)
                

        def Test(self):
                import main
                main()


        #def filePath(self, fileName: str)
        
        
        '''def CFG_MNG(self):
                if addon_path_check == 1:

                        
                
                        print("Nefunguje") '''     
                       
                 
                

class SecondTab(QWidget):
        def __init__(self):
                super().__init__()

class ThirdTab(QWidget):
        def __init__(self):
                super().__init__()



        
        #self.setStyleSheet("background-color: #69884c;")
      

        
        
               

        

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
