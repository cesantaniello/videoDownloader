import sys
import os
import pytube

from mainWindowTemplate import Ui_MainWindow
from PyQt5.QtCore import QSize, Qt, QObject, QThread,pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from worker import Worker

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("YouTube Downloader")
        
        # 1 - create Worker and Thread inside the Form
        self.worker = Worker()  # no parent!
        self.thread = QThread()  # no parent!

        # 2 - Connect Worker`s Signals to Form method slots to post data.
        self.worker.intReady.connect(self.onIntReady)

        # 3 - Move the Worker object to the Thread object
        self.worker.moveToThread(self.thread)

        # 4 - Connect Worker Signals to the Thread slots
        self.worker.finished.connect(self.thread.quit)

        # 5 - Connect Thread started signal to Worker operational slot method
        self.thread.started.connect(self.worker.procCounter)

        # * - Thread finished signal will close the app if you want!
        #self.thread.finished.connect(app.exit)
        
        self.filesize = 0
        self.progressBarValue = 0
        
        self.labelURL.setText("YouTube URL")
        self.labelPat.setText("Download folder")
        self.lineEditPath.setText(os.path.expanduser('~'))
        self.btnSearchPath.setText("Select folder...")
        self.rBtnMusic.setText("Music")
        self.rBtnMusic.setChecked(True)
        self.rBtnVideo.setText("Video")
        self.downloadButton.setText("Download")
        self.labelProgress.setText("")
        self.labelProgress.setFixedSize(QSize(600,25))

        self.setFixedSize(QSize(600, 250))
        self.progressBar.setValue(self.progressBarValue)
        
        self.downloadButton.clicked.connect(self.downloadButtonPressed)
        self.btnSearchPath.clicked.connect(self.selectFolder)
        
    def selectFolder(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select folder"))
        if file != "":
            self.lineEditPath.setText(file)
        
    def downloadButtonPressed(self):
        url = self.lineEditURL.text()
        if(url != ""):
            if("youtube" in url or "youtu.be" in url):
                downloadPath = self.lineEditPath.text()
                format = ""
                
                if (self.rBtnMusic.isChecked() == True):
                    format = 'music'
                    
                elif (self.rBtnVideo.isChecked() == True):
                    format = 'video'
                
                if format != "" and downloadPath!="":
                    self.progressBar.setValue(0)
                    self.worker.url = url
                    self.worker.downloadPath = downloadPath
                    self.worker.format = format
                    self.labelProgress.setText("Starting download process...")
                    self.thread.start()
                    
        return ""
    
    def onIntReady(self,value):
        self.progressBar.setValue(value)
        if(value < 100):
            self.labelProgress.setText("Downloading...")
        else:
            self.labelProgress.setText("Download complete!")
    

        


    
app = QApplication(sys.argv)
filesize = 0
progress = 0
window = MainWindow()
window.show()

app.exec()