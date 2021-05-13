from google.cloud import storage


class BucketConfig:

    def __init__(self, awacslogger) -> None:
        self.__storage_client = storage.Client.from_service_account_json(
            'C:/Users/Shubham Snehi/Downloads/awacs-dev-160bf0e57dc1.json')
        self.awacslogger = awacslogger

    # Cloud Storage Bucket Methods
    # Bucket Connection
    def getbucketconn(self, bucketname):
        try:
            bucket = self.__storage_client.get_bucket(bucketname)
            self.awacslogger.logger.info("Bucket Connection Successful")
            return bucket
        except Exception as e:
            self.awacslogger.logger.error("Unable to connect bucket :" + e)
