from file import File

class Folder(object):
    def __init__(self, folder_name):
        if type(folder_name) is not str:
            raise Exception

        self.__folder_name = folder_name
        self.__folders = []
        self.__files = []

    def __str__(self):
        return self.__folder_name
    

    def add_file(self, file):
        if type(file) is not File:
            raise Exception

        if file not in self.__files:
            self.__files.append(file)

    def add_folder(self, folder):
        if type(folder) is not Folder:
            raise Exception
        
        # checks if the same object is in the list
        if folder not in self.__folders:
            self.__folders.append(folder)
            

    def all_files(self):
        return self.__files

    def all_folders(self):
        return self.__folders
