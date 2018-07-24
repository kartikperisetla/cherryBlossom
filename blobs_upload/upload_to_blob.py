import os, sys
from azure.storage.blob import BlockBlobService

def upload_file_to_blob(sysargs):
    try:
        # Create the BlockBlockService that is used to call the Blob service for the storage account
        block_blob_service = BlockBlobService(account_name='gringotts', account_key='+HzZwDi7i9vK1eSaQzrAY1DWnf5PbYI9ZrpVBSbbLzRIL3toIziiiMnpf0TbbhqIITSuUSfzeAVCZoROBreSyw==')

        # Create a container called 'quickstartblobs'.
        container_name ='vault713'

        # Upload the created file, use local_file_name for the blob name
        block_blob_service.create_blob_from_path(container_name, 'stone1.json', sysargs[0])
    
    except Exception as e:
        print(e)


# Main method.
if __name__ == '__main__':
    upload_file_to_blob(sys.argv[1:])