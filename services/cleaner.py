import os

# A class that removes the files that match a certain format
class Cleaner:
    def __init__(self):
        pass

    @staticmethod
    def remove_mp3_files(folder="staticfiles", exceptions=["silence_1.mp3"]): 
        if folder:
            os.chdir(folder)
        for file in os.listdir():
            print(file)
            if file.endswith(".mp3") and file not in exceptions:
                os.remove(file)


    @staticmethod
    def remove_apkg_files(exceptions=[]):
        for file in os.listdir():
            if file.endswith(".apkg") and file not in exceptions:
                os.remove(file)
    
    @staticmethod
    def remove_pdf_files(exceptions=[]):
        for file in os.listdir():
            if file.endswith(".pdf") and file not in exceptions:
                os.remove(file)