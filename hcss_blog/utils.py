import os
import secrets
from hcss_blog import S3_KEY, S3_SECRET, S3_BUCKET
from hcss_blog.models import User
import boto3
from botocore.exceptions import ClientError

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + file_ext

    s3 = boto3.client(
       "s3",
       aws_access_key_id=S3_KEY,
       aws_secret_access_key=S3_SECRET
    )

    try:
        s3.upload_fileobj(
            form_picture,
            S3_BUCKET,
            picture_fn,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": form_picture.content_type
            }
        )
    except ClientError as e:
        print(e)
        return None

    return "https://{}.s3.amazonaws.com/{}".format(S3_BUCKET, picture_fn)
