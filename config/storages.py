from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """Static files at static/ in the R2 bucket."""

    location = 'static'
    default_acl = None
    querystring_auth = False


class MediaStorage(S3Boto3Storage):
    """Uploaded media at media/ in the R2 bucket."""

    location = 'media'
    file_overwrite = False
    default_acl = None
    querystring_auth = False
