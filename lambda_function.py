"""
CPSY-300 Project 1 – Task 3
Simulated serverless function: read All_Diets.csv from Azurite (local Azure Blob
emulator), compute average Protein/Carbs/Fat by Diet_type, and save results to
a local JSON file (simulating NoSQL storage).
"""

from azure.storage.blob import BlobServiceClient
import pandas as pd
import io
import json
import os

# Well-known Azurite development storage account credentials
CONNECT_STR = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

CONTAINER_NAME = "datasets"
BLOB_NAME = "All_Diets.csv"
OUTPUT_DIR = "simulated_nosql"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "results.json")
MACROS = ["Protein(g)", "Carbs(g)", "Fat(g)"]


def average_macros(df):
    """Mean protein, carbs, and fat grouped by Diet_type."""
    return df.groupby("Diet_type")[MACROS].mean()


def process_nutritional_data_from_azurite():
    """Download CSV from Azurite, aggregate macros by diet, save JSON results."""
    blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)

    container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    blob_client = container_client.get_blob_client(BLOB_NAME)

    # Download blob content into memory and load as DataFrame.
    # Only the columns used by the aggregation are parsed. Recipe name,
    # cuisine, and extraction timestamps are not needed for the diet means.
    stream = blob_client.download_blob().readall()
    df = pd.read_csv(
        io.BytesIO(stream),
        usecols=["Diet_type", *MACROS],
    )

    # Group by diet type and compute mean of the three macro columns
    avg_macros = average_macros(df)

    # Persist as JSON records (simulates writing to a NoSQL store)
    result = avg_macros.reset_index().to_dict(orient="records")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f, indent=2)

    return "Data processed and stored successfully."


if __name__ == "__main__":
    # Manual invoke (Azurite has no real Blob-trigger support like Azure Functions)
    message = process_nutritional_data_from_azurite()
    print(message)
