from google.cloud import storage
import logging


class BucketConfig:

    def __init__(self) -> None:
        self.__storage_client = storage.Client.from_service_account_json(
            'C:/Users/Shubham Snehi/Downloads/awacs-dev-160bf0e57dc1.json')

    # Cloud Storage Bucket Methods
    # Bucket Connection
    def getbucketconn(self, bucketname):
        try:
            bucket = self.__storage_client.get_bucket(bucketname)
            logging.info("Bucket Connection Successful")
            return bucket
        except:
            logging.error("Unable to connect bucket")
        return

    # Get List of files in Bucket
    @staticmethod
    def getbuckectfilelist(bucket):
        try:
            files = [files.name for files in list(
                bucket.list_blobs(prefix=''))]
        except:
            files = "Failed to get files"
        return files
