import logging
from FileConfig import FileConfig
from BucketHandler import BucketCon
from FileHandler import FileHandler
import argparse
from google.cloud import storage

if __name__ == '__main__':

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
    # Setting File Details
    sourcefile = FileConfig.FileConfig()
    sourcefile.setConfig(args)

    # Bucket Connection
    bc = BucketCon.BucketConfig()
    bucket = bc.getbucketconn(sourcefile.bucketName)
    blob = bucket.get_blob(sourcefile.filePath +
                           sourcefile.fileName + sourcefile.fileType)

    FileHandler.handlefile(sourcefile, blob)

    logging.info("File Name:", sourcefile.fileName + sourcefile.fileType, "\nFile Time:", sourcefile.fileDate,
                 "\nFile Path:", sourcefile.filePath, "\nBucket Name:", sourcefile.bucketName, "\nDestination File:", sourcefile.destPath)

# py main.py -p gs://balatestawacs/SampleFiles/AIOCD0923/AIOCD0923_02_2021_511b9d2d-76c3-4e4e-a2a4-35840fc612ce.xls --dpath Tempfiles2
# py main.py -p gs://balatestawacs/SALE_DTL.DBF --dpath Tempfiles3
