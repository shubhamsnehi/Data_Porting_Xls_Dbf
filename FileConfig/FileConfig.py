from FileHandler import FileHandler
import os.path
from datetime import datetime
from BucketHandler import BucketCon


class FileConfig:

    def __init__(self, awacslogger):
        self.filePath = None
        self.fileName = None
        self.fileDate = datetime.now()
        self.fileType = None
        self.bucketName = None
        self.destPath = None
        self.awacslogger = awacslogger
        self._blob = None

    # Properties, Getters and Setters
    # File Path
    @property
    def filepath(self):
        return self.filePath

    @filepath.setter
    def filepath(self, gspath):
        try:
            path = gspath.split('//')
            pathstr = path[1].split('/')
            self.bucketname = pathstr[0]
            self.filename = pathstr[len(pathstr) - 1]
            if len(pathstr) > 2:
                self.filePath = '/'.join(pathstr[1:len(pathstr) - 1]) + '/'
            else:
                self.filePath = ''
        except Exception as e:
            self.awacslogger.error("File path argument incorrect:" + e)

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
            self.awacslogger.warn(
                "Destination is blank, file will save in pwd !")
        pathstr = path.split('/')
        self.destFile = pathstr[len(pathstr) - 1]
        if os.path.splitext(self.destFile)[1]:
            # add '/'
            if pathstr[len(pathstr) - 1] == '':
                self.destPath = '/'.join(pathstr[0:len(pathstr) - 1])
            else:
                self.destPath = '/'.join(pathstr[0:len(pathstr) - 1])
            if os.path.splitext(self.destFile)[1] == '.csv':
                self.destFile = pathstr[len(pathstr) - 1]
            else:
                self.awacslogger.error(
                    "Invalid destination file name: " + path)
        # add '/'
        else:
            if pathstr[len(pathstr) - 1] == '':
                self.destPath = '/'.join(pathstr[0:len(pathstr) - 1])
            else:
                self.destPath = '/'.join(pathstr[0:len(pathstr)])
            self.destFile = self.fileName + '.csv'

    # Set Config
    def setConfig(self, args):
        self.filepath = args.filePath
        self.destpath = args.destPath

        self.awacslogger.info("File Details -- File :" + self.filePath + self.fileName + self.fileType +
                              "  Bucket Name:" + self.bucketName + "  Destination File:" + self.destPath)

        # Bucket Connection
        try:
            bucketcon = BucketCon.BucketConfig(self.awacslogger)
            bucket = bucketcon.getbucketconn(self.bucketName)
            blob = bucket.get_blob(self.filePath +
                                   self.fileName + self.fileType)
            self._blob = blob
        except Exception as e:
            self.awacslogger.error("Failed to connect Bucket" + e)

    # File Convert
    def convert(self):
        converter = FileHandler.FileParser(self.awacslogger)
        converter.convertfile(self, self._blob)
