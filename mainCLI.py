import os
import sys
import youtubedownload.downloadFromYoutube as downloadFromYoutube

def musicFormat(dictDirectories: dict):
    format = 'music'
    downloadPath = dictDirectories['musicDownloadPath']
    
    return downloadPath, format
    
def videoFormat(dictDirectories:dict ):
    format = 'video'
    downloadPath = dictDirectories['videoDownloadPath']
    
    return downloadPath, format
    
def createDirectory(pathToDirectory: str):
    statusCode = 0
    
    if(type(pathToDirectory) is str):
        try:
            if (not os.path.exists(pathToDirectory)):
                print(f"\nCreating directory {pathToDirectory} ...")
                os.mkdir(pathToDirectory)
                print(f"\nDirectory {pathToDirectory} successfully created")
        except:
            statusCode = 1            
    else:
        print(f"\ncreateDirectory: This method requires a string with path.")

    return statusCode
    
def initializeYTWorkspace():
    dictDirectories = {}
    dictDirectories['appDownloadPath'] = f"{os.path.expanduser('~')}/YTDownloads"
    dictDirectories['musicDownloadPath'] = f"{dictDirectories['appDownloadPath']}/Music"
    dictDirectories['videoDownloadPath'] = f"{dictDirectories['appDownloadPath']}/Video"

    createDirectory(dictDirectories['appDownloadPath'])
    
    return dictDirectories

def formatOptions(dictDirectories: dict):
    formatList = ["Music","Video"]
    switcher = {
        "1":musicFormat,
        "2":videoFormat
    }
    
    downloadPath = ""
    format = ""
    
    for index,format in enumerate(formatList):
        print(f'{index + 1}. {format}')
    formatOption = input("\nOption: ")
    
    if(formatOption in switcher.keys()):
        downloadPath, format = switcher[formatOption](dictDirectories)
    else:
        print("\nInvalid option.")
    
    return downloadPath, format
    
def YTMenu():
    dictDirectories = initializeYTWorkspace()

    url = input("\nURL from YouTube: ")
    if(url != ""):
        if("youtube" in url or "youtu.be" in url):
            downloadPath = ""
            format = ""
            downloadPath,format = formatOptions(dictDirectories)
            
            if format != "" and downloadPath!="":
                statusCode = createDirectory(downloadPath)
                if statusCode == 0:
                    downloadFromYoutube.download(url,downloadPath,format)
                else:
                    print(f"\nError creating directory {downloadPath} ...")      
        else:
            print("\nThis is not a YouTube URL.")
    else:
        print("\nURL cannot be empty.")

    return ""

switcher = {
    "0":sys.exit,
    "1":YTMenu
}

option = ""

while (option != "0"):
    optionList = ["Exit","Download from YouTube"]
    for index,format in enumerate(optionList):
        print(f'{index}. {format}')
        
    option = input("\nOption: ")
    
    function = switcher.get(option,lambda:"\nInvalid option")
    print(function())