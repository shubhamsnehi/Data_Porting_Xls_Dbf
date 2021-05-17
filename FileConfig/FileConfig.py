import os.path
from datetime import datetime
from BucketHandler import BucketCon
import os
import pandas as pd
from simpledbf import Dbf5


class FileConfig:

    def __init__(self, awacslogger):
        self.filePath = None
        self.fileName = None
        self.fileDate = datetime.now()
        self.fileType = None
        self.bucketName = None
        self.destPath = None
        self._awacslogger = awacslogger
        self._blob = None

    # Properties, Getters and Setters
    # File Path
    @property
    def filepath(self):
        return self.filePath

    @filepath.setter
    def filepath(self, gspath):
        try:
            path = gspath.split('//') # gs:// seperation
            pathstr = path[1].split('/') 
            self.bucketname = pathstr[0] # bucket name extraction
            self.filename = pathstr[len(pathstr) - 1] # filename extraction
            if len(pathstr) > 2:
                self.filePath = '/'.join(pathstr[1:len(pathstr) - 1]) + '/' # filepath extraction
            else:
                self.filePath = ''
        except Exception as e:
            self._awacslogger.error("File path argument incorrect:" + e)

    # File Name
    @property
    def filename(self):
        return self.fileName

    @filename.setter
    def filename(self, file):
        self.fileName = os.path.splitext(file)[0]
        self.filetype = os.path.splitext(file)[1]

    # File Type
    @property
    def filetype(self):
        # self.fileType = os.path.splitext(self.fileName)[1]
        return self.fileType

    @filetype.setter
    def filetype(self, file):
        self.fileType = file

    # File Date
    @property
    def filedate(self):
        self.fileDate = datetime.now()
        return self.fileDate

    @filedate.setter
    def filedate(self, val):
        self.fileDate = val

    # Upload Bucket Name
    @property
    def bucketname(self):
        return self.bucketName

    @bucketname.setter
    def bucketname(self, bucketname):
        self.bucketName = bucketname

    # Destination Path
    @property
    def destpath(self):
        return self.destPath

    @destpath.setter
    def destpath(self, path):
        if path == '/':
            self._awacslogger.warn(
                "Destination is blank, file will save in pwd !")
            print("Destination is blank, file will save in pwd !")
        pathstr = path.split('/')
        self.destFile = pathstr[len(pathstr) - 1]
        if os.path.splitext(self.destFile)[1]:
            # add '/'
            if pathstr[len(pathstr) - 1] == '': # if dpath in blank only dest filename provided
                self.destPath = '/'.join(pathstr[0:len(pathstr) - 1])
            else:
                self.destPath = '/'.join(pathstr[0:len(pathstr) - 1])
            if os.path.splitext(self.destFile)[1] == '.csv': # if file name is specified
                self.destFile = pathstr[len(pathstr) - 1]
            else:
                self._awacslogger.error(
                    "Invalid destination file name: " + path)
        # add '/'
        else: # if dpath in blank
            if pathstr[len(pathstr) - 1] == '':
                self.destPath = '/'.join(pathstr[0:len(pathstr) - 1])
            else:
                self.destPath = '/'.join(pathstr[0:len(pathstr)])
            self.destFile = self.fileName + '.csv'


    # Set Config
    def setConfig(self, args):
        self.filepath = args.filePath
        self.destpath = args.destPath

        self._awacslogger.info("File Details -- File :" + self.filePath + self.fileName + self.fileType +
                               "  Bucket Name:" + self.bucketName + "  Destination File:" + self.destPath)

        # Bucket Connection
        try:
            bucketcon = BucketCon.BucketConfig(self._awacslogger)
            bucket = bucketcon.getbucketconn(self.bucketName)
            blob = bucket.get_blob(self.filePath +
                                   self.fileName + self.fileType)
            self._blob = blob
        except Exception as e:
            self._awacslogger.error("Failed to connect Bucket" + e)


    # File Convert
    def convert(self):
        # Identify file type and create desired file type parsing object
        if self.fileType == '.xlsx' or self.fileType == '.xls':
            self._awacslogger.info(
                self.fileType + " File type Identified: " + self.fileName + self.fileType)
            # initializing the class
            parser = XLS(self._awacslogger)
        elif self.fileType == '.DBF' or self.fileType == '.dbf':
            self._awacslogger.info(
                self.fileType + " File type Identified: " + self.fileName + self.fileType)
            # initializing the class
            parser = DBF(self._awacslogger, self.fileName)
        else:
            parser = None
            self._awacslogger.error("File not found or Invalid file")
            return

        # Director object
        director = Director(self._awacslogger)

        # Build Parser
        self._awacslogger.info("File porting initialized: " +
                               self.fileName + self.fileType)
        director.setBuilder(parser)  # Setting type of builder
        convert = director.parseFile(self._blob, self)  # Parse method call
        convert.saveConvertedFile(self)  # Saving parsed file
        convert.deleteTempFile(self.fileName + self.fileType)  # Deleting temp file if created
        print("")


# Director class handles builder
class Director:
    __builder = None

    def __init__(self, awacslogger) -> None:
        self._awacslogger = awacslogger

    # Set builder according to file type
    def setBuilder(self, builder) -> None:
        self.__builder = builder

    # Parse file through builder
    def parseFile(self, blob, sourcefile):
        parse = Parser(self._awacslogger)  # Parser object
        df = self.__builder.convert(blob)
        parse.convertedFile(df)
        self._awacslogger.info(
            "File conversion Done : " + sourcefile.fileName + sourcefile.fileType)
        return parse


# Parse File
class Parser:
    def __init__(self, awacslogger) -> None:
        self.__df = None
        self._awacslogger = awacslogger

    def convertedFile(self, df) -> None:
        self.__df = df

    def saveConvertedFile(self, sourcefile) -> None:
        if not os.path.exists('.' + sourcefile.destPath):
            os.makedirs('.' + sourcefile.destPath)
            self._awacslogger.info(
                "Destinaton directory created :" + sourcefile.destPath)
        self.__df.to_csv('.' + sourcefile.destPath + '/' +
                         sourcefile.destFile, '|',  index=False)
        self._awacslogger.info(
            "Ported file saved at : ." + sourcefile.destPath + "/" + sourcefile.destFile)
        print("Porting Done: ." + sourcefile.destPath + "/" + sourcefile.destFile)

    def deleteTempFile(self, path) -> None:
        if os.path.exists(path):
            try:
                os.remove(path)
                self._awacslogger.info("Temp file deleted at : " + path)
            except Exception as e:
                self._awacslogger.error(
                    "Can't delete file at : " + path + e)


# Builder Class
class Builder:

    # builder convert method pass
    def convert(self) -> None: pass


# XLS builder class
class XLS(Builder):

    def __init__(self, awacslogger) -> None:
        self._awacslogger = awacslogger

    # File conversion from xls or xlsx to csv
    def convert(self, blob):
        try:
            df = pd.DataFrame(pd.read_excel(blob.download_as_bytes()))
            self._awacslogger.info(
                "Data ported form '.xls' to '.csv' : ")
            return df
        except Exception as e:
            self._awacslogger.error(
                "Data porting for .xls or .xlsx failed")


# DBF builder class
class DBF(Builder):

    def __init__(self, awacslogger, tempFile) -> None:
        self._awacslogger = awacslogger
        self.__tempfile = tempFile

    # File conversion from dbf to csv
    def convert(self, blob):
        try:
            blob.download_to_filename(self.__tempfile + '.DBF')
            dbf = Dbf5(self.__tempfile + '.DBF', codec='utf-8')
            self._awacslogger.info("Data ported from '.dbf' to '.csv'")
            df = dbf.to_dataframe()
            return df
        except Exception as e:
            self._awacslogger.error("Data porting for .dbf failed:" + e)
