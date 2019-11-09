from os import path

from google.cloud import storage


def download_from_gs(url, destination):
    print("Downloading '%s' to '%s'" % (url, destination))

    # url will be in the format gs://<bucket_name>, and we just want the name of the bucket
    _, gs_path = url.split("//")
    bucket_name, object_name = gs_path.split("/", 1)

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    # Setting a prefix will essentially allow us to only see blobs within a certain directory path
    blobs = bucket.list_blobs(prefix=object_name)

    # Download each file in the blob separately, as downloading a whole folder is not possible
    for blob in blobs:
        destination_path = path.join(destination, blob.name.split("/")[-1])
        print("Object '%s' will be downloaded to '%s'" % (blob.name, destination_path))
        blob.download_to_filename(destination_path)
        print("File Downloaded")


def upload_to_gs(url, file_path):
    print("Uploading file '%s' to '%s'" % (file_path, url))

    # url will be in the format gs://<bucket_name>, and we just want the name of the bucket
    _, gs_path = url.split("//")
    bucket_name, object_name = gs_path.split("/", 1)

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(object_name)

    blob.upload_from_filename(file_path)

    print("File Uploaded")