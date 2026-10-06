# CPSY-300 Project 1 — Task 3 Explanation

## Cloud-Native Data Processing with Azurite (Local Azure Blob Emulator)

### 1. How Azurite simulates cloud Blob Storage locally

Azure Blob Storage is Microsoft’s object-storage service in the cloud: you upload files (blobs) into containers, and applications (including Azure Functions) can read or write those blobs over HTTP with a connection string and SDK. For local development and coursework, spinning up a full Azure subscription is unnecessary. **Azurite** is Microsoft’s open-source emulator that implements the same Blob (and Queue/Table) REST APIs on your machine.

In this project Azurite listens on:

- Blob: `http://127.0.0.1:10000`
- Queue: `http://127.0.0.1:10001`
- Table: `http://127.0.0.1:10002`

It uses the well-known development account `devstoreaccount1` and a published sample account key. Client code connects with a connection string that points `BlobEndpoint` at localhost instead of `*.blob.core.windows.net`. From the Python SDK’s point of view (`BlobServiceClient`), the calls look the same as production Azure Storage—create a container, upload a blob, download a blob—so the workflow is cloud-native even though nothing leaves the laptop.

Because Azurite stores data under a local data directory (here `.azurite-data/`), you can reset state by clearing that folder or recreating containers. That makes it ideal for demos and screenshots without cloud cost or network dependency.

> **Note for this environment:** Docker was not available on the Linux box, so Azurite was started with the npm package (`npm install -g azurite`) and the flag `--skipApiVersionCheck` so the current `azure-storage-blob` Python SDK’s API version is accepted. Equivalent Docker command (preferred when Docker is installed):  
> `docker run -d --name azurite -p 10000:10000 -p 10001:10001 -p 10002:10002 mcr.microsoft.com/azure-storage/azurite`

### 2. How the serverless workflow runs (manual invoke)

A typical **serverless** pattern in Azure is: upload a file to Blob Storage → an **Azure Function** with a Blob trigger runs automatically → the function processes the file and writes results elsewhere (e.g. Cosmos DB / another blob).

**Azurite does not provide real event triggers.** It only emulates the storage APIs. There is no built-in “blob created → invoke function” hook like in the Azure Functions host against real Storage. Therefore our workflow is:

1. **Start Azurite** (emulator stays running).
2. **Upload** `All_Diets.csv` into container `datasets` using `upload_to_azurite.py` (creates the container if needed).
3. **Manually invoke** `lambda_function.py`, which plays the role of the serverless function: it reads the blob from Azurite, computes aggregates, and writes output locally.

This still demonstrates the cloud-native idea—stateless processing driven by data in object storage—while staying fully local. The assignment notes also suggest tools like `watchdog` to watch the filesystem and re-run the script when a new file appears; that would more closely mimic an event-driven trigger, but a clean manual invoke is sufficient and easier to document with screenshots.

### 3. What the function computes and where results go

`lambda_function.py` does the following:

1. Connects to Azurite with `BlobServiceClient.from_connection_string(...)`.
2. Downloads blob `All_Diets.csv` from container `datasets` into memory.
3. Loads the bytes with pandas (`pd.read_csv`).
4. Groups rows by **`Diet_type`** and computes the **mean** of:
   - `Protein(g)`
   - `Carbs(g)`
   - `Fat(g)`
5. Converts the grouped table to a list of JSON records and saves them to  
   **`simulated_nosql/results.json`**.

The `simulated_nosql/` folder stands in for a NoSQL document store (for example Azure Cosmos DB or DynamoDB). Each JSON object is one diet type with its average macros—document-oriented data that a real NoSQL API could store as items/documents. Keeping results as a local JSON file keeps the project self-contained while still showing the “process → persist structured documents” pattern.

Example summary of results produced in our run (averages by diet):

| Diet_type     | Protein (g) | Carbs (g) | Fat (g) |
|---------------|------------:|----------:|--------:|
| dash          | ~69.28      | ~160.54   | ~101.15 |
| keto          | ~101.27     | ~57.97    | ~153.12 |
| mediterranean | ~101.11     | ~152.91   | ~101.42 |
| paleo         | ~88.67      | ~129.55   | ~135.67 |
| vegan         | ~56.16      | ~254.00   | ~103.30 |

These values match expectations from Task 1 analysis (e.g. keto lower carbs / higher fat; vegan higher carbs / lower protein).

### 4. Files added for Task 3

| File | Role |
|------|------|
| `lambda_function.py` | Simulated serverless processor |
| `upload_to_azurite.py` | Creates `datasets` and uploads the CSV |
| `requirements-task3.txt` | `azure-storage-blob`, `pandas` |
| `simulated_nosql/results.json` | Output document store simulation |
| `task3_run_log.txt` | Timestamped run evidence |
| `TASK3_EXPLANATION.md` | This write-up |

Task 1–2 artifacts (`data_analysis.py`, `Dockerfile`, screenshots, etc.) were left unchanged.

### 5. Commands to re-run locally

```bash
cd /workspace/cloud-project1

# Terminal 1 — keep Azurite running
export PATH="$HOME/.local/bin:$PATH"
azurite --blobHost 127.0.0.1 --blobPort 10000 \
  --queueHost 127.0.0.1 --queuePort 10001 \
  --tableHost 127.0.0.1 --tablePort 10002 \
  --location .azurite-data --skipApiVersionCheck

# Terminal 2 — once (venv already created under .venv/)
.venv/bin/python upload_to_azurite.py
.venv/bin/python lambda_function.py
# Expect: Data processed and stored successfully.
# Inspect: simulated_nosql/results.json
```

If Docker is available instead of npm Azurite:

```bash
docker run -d --name azurite -p 10000:10000 -p 10001:10001 -p 10002:10002 \
  mcr.microsoft.com/azure-storage/azurite
# (May still need API-version compatibility depending on image vs SDK versions.)
```

---

*Prepared for the CPSY-300 Project 1 team PDF report (Task 3 section).*
