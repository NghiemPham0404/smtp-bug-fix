from .config.aws_s3_config import settings
import boto3

def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )

def generate_presigned_url(key: str, expires_in: int = 3600) -> str:
    """Generate a presigned URL for private S3 objects."""
    s3_client = get_s3_client()
    if key.startswith("public"):
        return f"https://{settings.AWS_S3_BUCKET}.s3.amazonaws.com/{key}"
    else:
        return s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.AWS_S3_BUCKET, "Key": key},
            ExpiresIn=expires_in,
        )