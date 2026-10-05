"""
Helper: create the Azurite 'datasets' container (if needed) and upload All_Diets.csv.
Run this once before invoking lambda_function.py.
"""

from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError
import os

CONNECT_STR = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

CONTAINER_NAME = "datasets"
BLOB_NAME = "All_Diets.csv"
LOCAL_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "All_Diets.csv")


def main():
    client = BlobServiceClient.from_connection_string(CONNECT_STR)
    container = client.get_container_client(CONTAINER_NAME)

    try:
        container.create_container()
        print(f"Created container '{CONTAINER_NAME}'.")
    except ResourceExistsError:
        print(f"Container '{CONTAINER_NAME}' already exists.")

    if not os.path.isfile(LOCAL_CSV):
        raise FileNotFoundError(f"CSV not found: {LOCAL_CSV}")

    with open(LOCAL_CSV, "rb") as data:
        container.upload_blob(name=BLOB_NAME, data=data, overwrite=True)

    print(f"Uploaded '{BLOB_NAME}' to container '{CONTAINER_NAME}'.")


if __name__ == "__main__":
    main()
