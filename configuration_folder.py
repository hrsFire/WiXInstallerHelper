from folder import Folder
from configuration_file import ConfigurationFile

class ConfigurationFolder(Folder):
    def __init__(self, folder_name, is_excluded = False, copy_files_to_same_folder = False):
        if folder_name == "":
            raise Exception

        super().__init__(folder_name)
        self.__extensions = []
        self.__folders = []
        self.__files = []
        self.__is_excluded = is_excluded            
        self.__copy_files_to_same_folder = copy_files_to_same_folder

    def __str__(self):
        return super().__str__()
    

    def add_file(self, file):
        if type(file) is not ConfigurationFile:
            raise Exception
        
        self.__files.append(file)
        
    def add_extension(self, extension):
        if type(extension) is not str:
            raise Exception
        
        if extension not in self.__extensions:       
            self.__extensions.append(extension)

    def add_folder(self, folder):
        if type(folder) is not ConfigurationFolder:
            raise Exception
        
        if folder not in self.__folders:
            self.__folders.append(folder)

        else:
            raise Exception
        

    def all_extensions(self):
        return self.__extensions

    def all_folders(self):
        return self.__folders

    def all_files(self):
        return self.__files


    def is_excluded(self):
        return self.__is_excluded

    def copy_files_to_same_folder(self):
        return self.__copy_files_to_same_folder


    def is_allowed_extension(self, extension):
        if type(extension) is not str:
            raise Exception

        return extension in self.__extensions
    

    def find_folder_for_extension(self, extension, folder):
        if type(extension) is not str:
            raise Exception

        if type(folder) is not ConfigurationFolder:
            raise Exception

        if is_extension_in_folder(self, extension, self.all_extensions()):
            return folder

        for current_folder in self.all_folders:
            new_folder = None
            new_folder = find_folder_for_extension(self, extension, current_folder)

            if new_folder is not None:
                return folder.add_folder(new_folder)

        return None
            

    def is_extension_in_folder(self, extension, extensions):
        for available_extension in extensions:
            return available_extension == extension
