import botocore.exceptions
import dropbox.exceptions
from flask import request
from flask_restful import Resource
from storage_manager import StorageFactory


def exception_handler(func):
    """
    Decorator that handles exception that may occur during work with an API
    :param func: function to decorate
    :return: wrapper
    """

    def wrapper(*args, **kwargs):
        try:
            function_result = func(*args, **kwargs)
        except botocore.exceptions.NoCredentialsError:
            msg = 'You have no credentials passed.'
            return {'Error Message': msg}
        except botocore.exceptions.PartialCredentialsError:
            msg = "You don't have one of credentials keys."
            return {'Error Message': msg}
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == 'InvalidAccessKeyId':
                msg = "Your s3_access_key is invalid. Please check it."
                return {'Error Message': msg}
            if error.response['Error']['Code'] == 'SignatureDoesNotMatch':
                msg = 'Your s3_secret_access_key is invalid. Please check it.'
                return {'Error Message': msg}
        except dropbox.exceptions.BadInputError:
            msg = "Your dropbox_access_token is invalid. Please check it"
            return {'Error Message': msg}
        else:
            return function_result

    return wrapper


def crete_service(service_name: str):
    """
    Connects to selected Storage
    :param service_name: name of service you want to use
    :return: service
    """
    kwargs = request.args.to_dict()
    factory = StorageFactory()
    service = factory.connect_to_storage(service_name, **kwargs)
    return service


class Smoke(Resource):
    def get(self) -> dict:
        return {'message': 'OK'}


class Service(Resource):
    @exception_handler
    def get(self, service_name: str) -> dict:
        service = crete_service(service_name)
        return service.get_storage_connected()


class FilesList(Resource):
    @exception_handler
    def get(self, service_name: str, bucket_name: str or None = None) -> dict:
        service = crete_service(service_name)
        files_list = service.get_all_files(bucket_name=bucket_name)
        print(files_list)
        return {'Files': files_list}


class Files(Resource):
    @exception_handler
    def get(self, service_name: str, file_name: str, bucket_name: str or None = None) -> dict:
        service = crete_service(service_name)
        file_data = service.get_file(bucket_name=bucket_name,
                                     file_name=file_name)
        return {'File': file_name, 'File Data': str(file_data)}

    @exception_handler
    def post(self, service_name: str, file_name: str, bucket_name: str or None = None) -> dict:
        service = crete_service(service_name)
        file_data = request.json['data']
        result = service.create_file(bucket_name=bucket_name,
                                     file_name=file_name, file_data=file_data)
        print(result)
        file_data = service.get_file(bucket_name=bucket_name,
                                     file_name=file_name)
        return {'File': file_name, 'File Data': str(file_data)}
