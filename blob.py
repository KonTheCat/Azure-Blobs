import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient
import string, random, requests
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.identity import DefaultAzureCredential

app = Flask(__name__, instance_relative_config=True)

subscription = os.getenv("StorageAccountSubscriptionID")
account = os.getenv("StorageAccountName")
container = os.getenv("StorageContainerName")

def set_blob_data(data, storageAccountName, storageAccountKey, containerName, blobName):
    blob_service_client = BlobServiceClient(account_url = f"https://{storageAccountName}.blob.core.windows.net", credential = storageAccountKey)
    blob_client = blob_service_client.get_blob_client(container = containerName, blob = blobName)
    blob_client.upload_blob(data, blob_type = "BlockBlob", overwrite = True)

def get_primary_storage_account_key(storageAccountName, subscriptionID):
    default_credential = DefaultAzureCredential(exclude_shared_token_cache_credential=True)
    resource_client = ResourceManagementClient(default_credential, subscriptionID)
    resourceList = resource_client.resources.list()
    for item in resourceList:
        if(item.type == 'Microsoft.Storage/storageAccounts' and item.name == storageAccountName):
            resource_group_name = (item.id).split('/')[4]
    storageClient = StorageManagementClient(default_credential, subscriptionID)
    keys = storageClient.storage_accounts.list_keys(resource_group_name, storageAccountName)
    primaryKey = keys.keys[0].value
    return primaryKey

key = get_primary_storage_account_key(account, subscription)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        try:
            set_blob_data(file, account, key, container, filename)
        except Exception:
            print ('Exception=' + Exception) 
            pass
        ref =  'http://'+ account + '.blob.core.windows.net/' + container + '/' + filename
        return '''
	    <!doctype html>
	    <title>File Link</title>
	    <h1>Uploaded File Link</h1>
	    <p>''' + ref + '''</p>
	    <img src="'''+ ref +'''">
	    '''
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=81)
