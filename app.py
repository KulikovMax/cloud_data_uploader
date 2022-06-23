from flask import Flask, url_for
from flask_restful import Api

from api import Smoke, Service, FilesList, Files

app = Flask(__name__)
api = Api(app, prefix='/api')

api.add_resource(Smoke, '/smoke')
api.add_resource(Service, '/<service_name>')
api.add_resource(FilesList, '/<service_name>/files',
                 '/<service_name>/<bucket_name>/files')
api.add_resource(Files, '/<service_name>/files/<file_name>',
                 '/<service_name>/<bucket_name>/files/<file_name>')


@app.route("/")
def site_map():
    routes = {'/': 'Returns list of all urls',
              '/api': {
                  '/smoke': 'check if api sends response properly',
                  '/<service_name>': 'connects to chosen Service. Available: s3, dropbox',
                  's3': {
                      '/<service_name>/<bucket_name>/files': 'returns all files from selected bucket',
                      '/<service_name>/<bucket_name>/files/<file_name>':
                          'returns one file from selected bucket. If method is POST, writes data to the file on S3.'
                          'Data to write must be placed in requestBody: {"data": "your_data"}'
                  },
                  'dropbox': {
                      '/<service_name>/files': 'returns all files from selected bucket',
                      '/<service_name>/files/<file_name>':
                          'returns one file from selected bucket. '
                          'If method is POST, writes data to the file on Dropbox.'
                          'Data to write must be placed in requestBody: {"data": "your_data"}'
                  }
              }
              }
    return routes


if __name__ == '__main__':
    app.run(port=5555)
