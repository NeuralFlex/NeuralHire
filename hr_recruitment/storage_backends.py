from storages.backends.s3boto3 import S3Boto3Storage

# Storage for confidential media (Resumes/CVs)
class PrivateMediaStorage(S3Boto3Storage):
    location = 'media/resumes'  # Path inside S3 bucket
    default_acl = 'private'     
    file_overwrite = False


class StaticRootStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'