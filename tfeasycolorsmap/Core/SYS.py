
# **** System management ***********************************************************************++*

class SYS:
    def __init__(self):
        super().__init__()

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, value):
        self.__version = value

    def getVersionString():
        return str(SYS.version / 10).replace(",", ".")

    