class File(object):
    def __init__(self, file_name):
        if type(file_name) is not str:
            raise Exception
        
        self.__file_name = file_name

    def __str__(self):
        return self.__file_name

    def extension(self):
        name = self.__file_name.split(".")
        return name[len(name) -1]
