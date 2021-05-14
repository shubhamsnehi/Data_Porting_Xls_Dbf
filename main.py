from FileConfig import FileConfig
from FileHandler import FileHandler
from AwacsLogger import AwacsLogger
import argparse


if __name__ == '__main__':

    # Logger File
    awacslogger = AwacsLogger.AWACSLogger("Logs")

    # Default Argument
    parser = argparse.ArgumentParser(description='File Porting Arguments.')
    # Adding Arguments with flags
    # Path of File
    parser.add_argument('-p', '--path', dest='filePath', type=str, default=None,
                        help='for input file path')
    # Destination Bucket of File
    parser.add_argument('-b', '--bucket', dest='bucket', type=str, default=None,
                        help='for destination bucket')
    # Destination File Path
    parser.add_argument('-d', '--dpath', dest='destPath', type=str, default=None,
                        help='for destination file path', )

    args = parser.parse_args()

    # Objects
    # Setting File Details and bucket conn
    sourcefile = FileConfig.FileConfig(awacslogger)
    dataobj = sourcefile.setConfig(args)

    # File Parse and save
    awacslogger.logger.debug(FileHandler.handlefile(
        awacslogger, sourcefile, dataobj))

# py main.py -p gs://balatestawacs/SampleFiles/AIOCD0923/AIOCD0923_02_2021_511b9d2d-76c3-4e4e-a2a4-35840fc612ce.xls --dpath /Tempfiles2/pqr.csv
# py main.py -p gs://balatestawacs/SALE_DTL.DBF --dpath /Tempfiles3/abcd.csv
