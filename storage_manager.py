import boto3
import dropbox
from abc import ABC, abstractmethod


class StorageCommunicator(ABC):
    """
    Abstract class. Represents required method for future classes, that would communicate to the Storage.
    """
    @abstractmethod
    def get_storage_connected(self) -> dict:
        """
        Check storage you are connected to.
        :return: {'message': 'your storage'
        """
        pass

    @abstractmethod
    def get_all_files(self, bucket_name: str) -> dict:
        """
        Get List of Files placed on storage
        :param bucket_name: name of S3 bucket. Required only for amazon S3 communication
        :return: {"filename1" : {"data": "your_file_data"}, ... "filenameN" : {"data": "your_file_data"}}
        """
        pass

    @abstractmethod
    def get_file(self, bucket_name: str, file_name: str) -> dict:
        """
        Returns data of specific file
        :param bucket_name: name of S3 bucket. Required only for amazon S3 communication
        :param file_name: name of the file you want to get
        :return: {'filename': 'your_file_data'}
        """
        pass

    @abstractmethod
    def create_file(self, bucket_name: str, file_name: str, file_data: str) -> dict:
        """
        Put file into Storage, returns it data
        :param bucket_name: name of S3 bucket. Required only for amazon S3 communication
        :param file_name: name of the file you want to get
        :param file_data: must be placed in requestBody. Data to write to your file
        :return:  {'filename': 'your_file_data'}
        """
        pass


class StorageFactory:
    """
    Factory Class that decides Communicator of which Storage to create
    """
    def __init__(self):
        self.__services = {'s3': S3Communicator,
                           'dropbox': DropboxCommunicator}

    def connect_to_storage(self, key, **kwargs):
        """
        Connect to chosen Storage
        :param key: storage name you want to connect
        :param kwargs: access keys dict
        :return: chosen service instance
        """
        service = self.__services.get(key)
        if not service:
            raise ValueError(key)
        return service(**kwargs)


class S3Communicator(StorageCommunicator):
    """
    Class that communicates with Amazon S3
    """
    def __init__(self, **kwargs):
        self.access_key = kwargs.get('s3_access_key')
        self.secret_key = kwargs.get('s3_secret_key')
        self.s3 = boto3.resource('s3', aws_access_key_id=self.access_key,
                                 aws_secret_access_key=self.secret_key)

    def get_storage_connected(self) -> dict:
        buckets = self.get_all_buckets()
        return {'Storage': 'S3', 'Buckets': buckets}

    def get_all_buckets(self):
        buckets = [bucket.name for bucket in self.s3.buckets.all()]
        return buckets

    def connect_to_bucket(self, bucket_name: str):
        return self.s3.Bucket(bucket_name)

    def get_all_files(self, bucket_name):
        bucket = self.connect_to_bucket(bucket_name)
        bucket_files = [o.key for o in bucket.objects.all()]
        data = {bucket_file: {
            'data': self.get_file(bucket_name, bucket_file)}
            for bucket_file in bucket_files}
        print(data)
        return data

    def get_file(self, bucket_name, file_name):
        bucket_file = self.s3.Object(bucket_name,
                                     file_name).get()['Body'].read().decode()
        return bucket_file

    def create_file(self, bucket_name, file_name, file_data):
        bf = self.s3.Object(bucket_name, file_name)
        res = bf.put(Body=file_data)
        print(res)
        return res


class DropboxCommunicator(StorageCommunicator):
    """
    Class that communicates with Dropbox
    """
    def __init__(self, **kwargs):
        self.access_token = kwargs['dropbox_access_token']
        self.dbx = dropbox.Dropbox(self.access_token)

    def get_storage_connected(self):
        return {'Storage': 'Dropbox'}

    def get_all_files(self, bucket_name: None = None):
        dbx_files_list = self.dbx.files_list_folder('')
        dbx_files = {d.name: {'data': self.get_file(d.name, '')}
                     for d in dbx_files_list.entries}
        return dbx_files

    def get_file(self,
                 file_name: str, folder_name: str = '', bucket_name: None = None, ):
        dbx_file = self.dbx.files_download('/' + file_name)[1].content.decode()
        print(dbx_file)
        return dbx_file

    def create_file(self, file_name: str, file_data: str,
                    bucket_name: None = None):
        data = bytes(file_data, encoding='utf-8')
        r = self.dbx.files_upload(data, f'/{file_name}')
        print(r)
