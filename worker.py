# worker.py
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
import pytube
import os
import time
import downloadFromYoutube


class Worker(QObject):
    finished = pyqtSignal()
    intReady = pyqtSignal(int)

    @pyqtSlot()
    def procCounter(self): # A slot takes no params
        self.download(self.url,self.downloadPath,self.format)
        self.finished.emit()
        
    def progress_function(self,chunk, file_handle, bytes_remaining):
        global filesize,progress
        
        current = ((filesize - bytes_remaining)/filesize)
        percent = ('{0:.1f}').format(current*100)
        progress = int(50*current)
        status = '█' * progress + '-' * (50 - progress)
        total = ' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percent)
        self.intReady.emit(int(float(percent)))

    def download(self,url,downloadPath,format):
        global filesize,progress
        try:
            youtube = pytube.YouTube(url,on_progress_callback=self.progress_function)
            downloaded_file = ""
            
            if (format == "music"):
                filesize = youtube.streams.filter(only_audio=True).first().filesize
                temp_file = youtube.streams.filter(only_audio=True).first().download(downloadPath)
                base, ext = os.path.splitext(temp_file)
                downloaded_file = base + ".mp3"
                if (os.path.exists(downloaded_file)):
                    os.remove(downloaded_file)
                os.rename(temp_file,downloaded_file)
            else:
                filesize = youtube.streams.get_highest_resolution().filesize
                downloaded_file = youtube.streams.get_highest_resolution().download(downloadPath)
                
            return 0
        except Exception as err:
            return 1
        
filesize = 0
progress = 0

"""
    def downloadOLD(url,downloadPath,format):
        global filesize,progress
        try:
            print("\nDownloading file...")
            youtube = pytube.YouTube(url,on_progress_callback=progress_function)
            downloaded_file = ""
            
            if (format == "music"):
                filesize = youtube.streams.filter(only_audio=True).first().filesize
                temp_file = youtube.streams.filter(only_audio=True).first().download(downloadPath)
                base, ext = os.path.splitext(temp_file)
                downloaded_file = base + ".mp3"
                if (os.path.exists(downloaded_file)):
                    os.remove(downloaded_file)
                os.rename(temp_file,downloaded_file)
            else:
                filesize = youtube.streams.get_highest_resolution().filesize
                downloaded_file = youtube.streams.get_highest_resolution().download(downloadPath)
                
            if (os.path.exists(f'{downloaded_file}')):
                print(f"\nFile downloaded successfully, check path: {downloadPath}")
            else:
                print(f"\nDownload fails, try it again or try another URL")
                
            return 0
        except Exception as err:
            print(f"\nUnexpected error: {err}")
            return 1
        
    def progress_functionOLD(chunk, file_handle, bytes_remaining):
        global filesize,progress
        current = ((filesize - bytes_remaining)/filesize)
        percent = ('{0:.1f}').format(current*100)
        progress = int(50*current)
        status = '█' * progress + '-' * (50 - progress)
        total = ' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percent)
        print(percent)
"""
