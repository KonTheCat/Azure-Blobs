# Uploading file from Python-Flask to Azure Blob 

A simple Python flask application to upload files to Azure Blob

**Steps**

1. Go to Azure management portal and create a Storage Account
2. Provide the subscription ID, the storage account name, and the container name as environment variables
3. Run the requirements file to install the required dependencies
4. Run az login in the local console to log into Azure so that the flask app has authentication it can use using DefaultAzureCredential
5. Run the python flask app locally to get access no the upload page

Now you can select any file from your system and upload to the designated Azure Blob. Once the upload is completed, the system will return a url for future access.

__Note__ - Larger files may take longer to upload
