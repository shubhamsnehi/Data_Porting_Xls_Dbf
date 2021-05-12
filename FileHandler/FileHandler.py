import os
import pandas as pd
from simpledbf import Dbf5
import logging


# Director class handles builder
class Director:
    __builder = None

    def setBuilder(self, builder):
        self.__builder = builder

    def parseFile(self, blob, sourcefile):
        parse = Parser() # Parser object
        df = self.__builder.convert(blob)
        parse.convertedFile(df)
        logging.info("File conversion Done : ", sourcefile.fileName)
        return parse


# Parse File
class Parser:
    def __init__(self):
        self.__df = None

    def convertedFile(self, df):
        self.__df = df

    def saveConvertedFile(self, sourcefile):
        if not os.path.exists(sourcefile.destPath):
            os.makedirs(sourcefile.destPath)
            logging.info("Destinaton directory created.")
        self.__df.to_csv('./' + sourcefile.destPath + '/' +
                         sourcefile.fileName + '.csv', '|',  index=False)
        logging.info("Ported file saved at : ", './' + sourcefile.destPath + '/' +
                     sourcefile.fileName + '.csv')

    def deleteTempFile(self, path):
        if os.path.exists(path):
            try:
                os.remove(path)
                logging.info("Temp file deleted at : ", path)
            except:
                logging.error("Can't delete file at : ", path)


class Builder:
    def convert(self): pass

# XLS builder classs
class XLS(Builder):

    def convert(self, blob):
        try:
            df = pd.DataFrame(pd.read_excel(blob.download_as_bytes()))
            logging.info("Data ported form '.xls' to '.csv")
            return df
        except:
            logging.error("Data porting for .xls or .xlsx failed")


# DBF builder class
class DBF(Builder):

    def __init__(self, tempFile) -> None:
        self.__tempfile = tempFile

    def convert(self, blob):
        try:
            blob.download_to_filename(
                './TempFiles/' + self.__tempfile + '.DBF')
            dbf = Dbf5('./TempFiles/' + self.__tempfile +
                       '.DBF', codec='utf-8')
            logging.info("Data ported from '.dbf' to '.csv'")
            df = dbf.to_dataframe()
            return df
        except:
            logging.error("Data porting for .dbf failed")


# Parser handle function
def handlefile(sourcefile, blob):
    if sourcefile.fileType == '.xlsx' or sourcefile.fileType == '.xls':
        logging.info("File type Identified")
        parser = XLS()  # initializing the class
    elif sourcefile.fileType == '.DBF' or sourcefile.fileType == '.dbf':
        logging.info("File type Identified")
        parser = DBF(sourcefile.fileName)

    director = Director()

    # Build Parser
    logging.info("File porting initialized")
    director.setBuilder(parser)
    convert = director.parseFile(blob, sourcefile)
    convert.saveConvertedFile(sourcefile)
    convert.deleteTempFile(
        './TempFiles/' + sourcefile.fileName + sourcefile.fileType)
    print("")
