from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import gzip
import datetime
import json

def initialize_storage_account():
    client_id = "<client-id>"
    secret = "<client-secret>"
    tenant = "<tenant-id>"
    adls_storage_account_name = "https://<storage-account>.blob.core.windows.net"

    try:
        token_credential = ClientSecretCredential(tenant_id=tenant, client_id=client_id,
                                                  client_secret=secret)

        blob_service_client = BlobServiceClient(
            account_url=adls_storage_account_name,
            credential=token_credential)
        return blob_service_client
    except Exception as e:
        print(e)


def create_blob(data, resource_name, extract_date):
    """Writing the API response to Blob"""
    dt = datetime.datetime.strptime(extract_date, '%Y-%m-%dT%H:%M:%S')
    year = dt.strftime("%Y")
    month = dt.strftime("%m")
    date = dt.strftime("%d")
    time = dt.strftime("%H%M%S")
    adls_container_name = '<container-name>'

    if data is not None:
        filename = "{0}-{1}{2}{3}{4}.json.gz".format(resource_name, year, month, date, time)
        blob_service_client = initialize_storage_account()
        print("Writing data to current for file:{}".format(filename))
        blob = "{0}\current\{1}".format(resource_name, filename)
        print(blob)
        blob_client = blob_service_client.get_blob_client(container=adls_container_name, blob=blob)
        data = gzip.compress(data)
        blob_client.upload_blob(data)
        print("Successfully written file to blob:{}".format(filename))
    else:
        raise ValueError("No Data Present to Write")


def main():
    data = [
            ['foo', 'bar', 'col1', 'col2'],
            ['val1', 'val1', 'val1', 'val1'],
            ['val2', 'val2', 'val2', 'val2']
    ]
    extract_date = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    create_blob(json.dumps(data).encode(), '<folder-name>', extract_date)


if __name__ == '__main__':
    main()
