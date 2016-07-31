from file import File

class ConfigurationFile(File):
    def __init__(self, file_name, is_excluded = False):
        if type(file_name) is not str:
            raise Exception
        
        super().__init__(file_name)
        self.__is_excluded = is_excluded

    def __str__(self):
        return super().__str__()
		

    def is_excluded(self):
        return self.__is_excluded

    def extension(self):
        return super().extension()
