**Binary Data Uploader**
***Quick Start***

 - Copy this git repository.
 - Install required packages:
 - `pip install -r requirements.txt`
 
 ***URLs***
`/` - Returns list of all urls,

`/api` - Prefix for all RESTfull API urls, described below

`/<service_name>` -  connects to chosen Service. Available: s3, dropbox

`/smoke`  - check if api sends response properly

**Dropbox urls**: 

`/<service_name>/files` - returns all files from Dropbox

`/<service_name>/files/<file_name>`  returns one file from selected bucket. If method is POST, writes data to the file on Dropbox.Data to write must be placed in requestBody: `{"data": "your_data"}`


**S3 urls**

`/<service_name>/<bucket_name>/files` - returns all files from selected bucket

`/<service_name>/<bucket_name>/files/<file_name>`-  returns one file from selected bucket. If method is POST, writes data to the file on S3.Data to write must be placed in requestBody: `{data: your_data}`

**Request Params:**
dropbox_access_token  - str, your dropbox token
s3_access_key - str, your s3 access toke
s3_secret_key - str, your s3 secret token