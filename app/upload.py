import logging

from botocore.exceptions import ClientError


def upload_file_to_bucket(s3_client, profile, bucket,  object_name=None):
    """Upload a file to an S3 bucket
    :param file_obj: File to upload
    :param bucket: Bucket to upload to
    :param folder: Folder to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = profile

    # Upload the file
    try:
        response = s3_client.upload_fileobj(profile, bucket, f"{object_name}")

    except ClientError as e:
        logging.error(e)
        return False
    return True
