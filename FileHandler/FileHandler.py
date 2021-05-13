import os
import pandas as pd
from simpledbf import Dbf5


# Director class handles builder
class Director:
    __builder = None

    def __init__(self, awacslogger) -> None:
        self.awacslogger = awacslogger

    def setBuilder(self, builder):
        self.__builder = builder

    def parseFile(self, blob, sourcefile):
        parse = Parser(self.awacslogger)  # Parser object
        df = self.__builder.convert(blob)
        parse.convertedFile(df)
        self.awacslogger.logger.info("File conversion Done : "+ sourcefile.fileName + sourcefile.fileType)
        return parse


# Parse File
class Parser:
    def __init__(self, awacslogger):
        self.__df = None
        self.awacslogger = awacslogger

    def convertedFile(self, df):
        self.__df = df

    def saveConvertedFile(self, sourcefile):
        if not os.path.exists(sourcefile.destPath):
            os.makedirs(sourcefile.destPath)
            self.awacslogger.logger.info("Destinaton directory created :/" + sourcefile.destPath)
        self.__df.to_csv('./' + sourcefile.destPath + '/' +
                         sourcefile.fileName + '.csv', '|',  index=False)
        self.awacslogger.logger.info("Ported file saved at : ./" + sourcefile.destPath + "/" +
                                sourcefile.fileName + ".csv")

    def deleteTempFile(self, path):
        if os.path.exists(path):
            try:
                os.remove(path)
                self.awacslogger.logger.info("Temp file deleted at : ", path)
            except:
                self.awacslogger.logger.error("Can't delete file at : ", path)


# Builder Class
class Builder:
    def convert(self): pass


# XLS builder classs
class XLS(Builder):

    def __init__(self, awacslogger) -> None:
        self.awacslogger = awacslogger

    def convert(self, blob):
        try:
            df = pd.DataFrame(pd.read_excel(blob.download_as_bytes()))
            self.awacslogger.logger.info("Data ported form '.xls' to '.csv'")
            return df
        except:
            self.awacslogger.logger.error("Data porting for .xls or .xlsx failed")


# DBF builder class
class DBF(Builder):

    def __init__(self, awacslogger, tempFile) -> None:
        self.awacslogger = awacslogger
        self.__tempfile = tempFile

    def convert(self, blob):
        try:
            blob.download_to_filename(
                './TempFiles/' + self.__tempfile + '.DBF')
            dbf = Dbf5('./TempFiles/' + self.__tempfile +
                       '.DBF', codec='utf-8')
            self.awacslogger.logger.info("Data ported from '.dbf' to '.csv'")
            df = dbf.to_dataframe()
            return df
        except:
            self.awacslogger.logger.error("Data porting for .dbf failed")


# Parser handle function
def handlefile(awacslogger, sourcefile, blob):
    if sourcefile.fileType == '.xlsx' or sourcefile.fileType == '.xls':
        awacslogger.logger.info(sourcefile.fileType + " File type Identified: " + sourcefile.fileName + sourcefile.fileType)
        parser = XLS(awacslogger)  # initializing the class
    elif sourcefile.fileType == '.DBF' or sourcefile.fileType == '.dbf':
        awacslogger.logger.info(sourcefile.fileType + " File type Identified: " + sourcefile.fileName + sourcefile.fileType)
        parser = DBF(awacslogger, sourcefile.fileName)

    director = Director(awacslogger)

    # Build Parser
    awacslogger.logger.info("File porting initialized: " + sourcefile.fileName + sourcefile.fileType)
    director.setBuilder(parser)
    convert = director.parseFile(blob, sourcefile)
    convert.saveConvertedFile(sourcefile)
    convert.deleteTempFile(
        './TempFiles/' + sourcefile.fileName + sourcefile.fileType)
    print("")
