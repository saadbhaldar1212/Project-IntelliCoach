import boto3
import os

from dotenv import find_dotenv, load_dotenv

_ = load_dotenv(find_dotenv())

# S3 configuration
ENDPOINT_URL = os.environ["ENDPOINT_URL"]
ACCESS_KEY = os.environ["ACCESS_KEY"]
SECRET_KEY = os.environ["SECRET_KEY"]
BUCKET_NAME = os.environ["BUCKET_NAME"]

# File keys in the bucket
FAQ_VDB_PREFIX = "faq_vdb/FitnessBot_Questions_VDB/"
FAQ_SHEET_KEY = "faq_sheet/Fitnessbot_allInOneQA.xlsx"
SECRET_AUTH_KEY = "intellicoach-fitness-chatbot-589e0fc60f1e.json"

# Local paths
LOCAL_VDB_BASE = r"database\chroma\FitnessBot_Questions_VDB"
LOCAL_SHEET_PATH = r"database\chroma\Fitnessbot_allInOneQA.xlsx"
LOCAL_SECRET_KEY_BASE = r"settings\intellicoach-fitness-chatbot-589e0fc60f1e.json"


def create_s3_client():
    """
    Create and return a boto3 S3 client using the configured endpoint and credentials.
    """
    return boto3.client(
        "s3",
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )


def ensure_dir(path):
    """
    Ensure the directory for the given file path exists. Creates it if necessary.
    """
    dir_path = os.path.dirname(path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)


def download_s3_file(s3, bucket, key, local_path):
    """
    Download a single file from S3 to the specified local path.
    """
    ensure_dir(local_path)
    print(f"Downloading {key} to {local_path}...")
    s3.download_file(bucket, key, local_path)


def download_vdb_directory(s3, bucket, prefix, local_base):
    """
    Download all files under the given S3 prefix, preserving the directory structure locally.
    """
    print(f"Listing objects under {prefix}...")
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            if key.endswith("/"):
                continue
            rel_path = key[len(prefix) :]
            local_path = os.path.join(local_base, rel_path)
            download_s3_file(s3, bucket, key, local_path)


def download_faq_sheet(s3, bucket, key, local_path):
    """
    Download the FAQ sheet from S3 to the specified local path.
    """
    download_s3_file(s3, bucket, key, local_path)


def download_secret_key(s3, bucket, key, local_path):
    """
    Download the secret key file from S3 to the specified local path.
    """
    download_s3_file(s3, bucket, key, local_path)


def main():
    """
    Main function to download the FAQ VDB directory and FAQ sheet from S3.
    """
    s3 = create_s3_client()
    download_vdb_directory(s3, BUCKET_NAME, FAQ_VDB_PREFIX, LOCAL_VDB_BASE)
    download_faq_sheet(s3, BUCKET_NAME, FAQ_SHEET_KEY, LOCAL_SHEET_PATH)
    download_secret_key(s3, BUCKET_NAME, SECRET_AUTH_KEY, LOCAL_SECRET_KEY_BASE)
    print("Download complete.")


if __name__ == "__main__":
    main()
