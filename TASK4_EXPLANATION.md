# CPSY-300 Project 1 — Task 4 Explanation

## CI/CD with GitHub Actions (no Azure, no Docker Hub)

The repository already holds the Task 2 image (`Dockerfile`, `data_analysis.py`) and the Task 3 simulated function (`lambda_function.py`, `upload_to_azurite.py`, Azurite). Task 4 automates those steps on every push.

Workflow file: `.github/workflows/deploy.yml`

### What the pipeline does

1. **Test.** Installs `requirements.txt` and runs `pytest`.
   - `tests/test_data_analysis.py` checks the diet dataset and runs `data_analysis.py`.
   - `tests/test_serverless.py` checks `average_macros()` and the saved `simulated_nosql/results.json` document.
2. **Build.** `docker build -t diet-analysis:local .` using the existing Dockerfile.
3. **Push.** Starts `registry:2` on port **5001** (the host port already used in `docker-compose.yml`) and pushes `localhost:5001/diet-analysis:latest`. The registry lives only for that job, so nothing is published to Docker Hub.
4. **Deploy the container.** `scripts/simulate_deploy.sh` runs the image that was just pushed and records stdout (`rows`, average macros, highest-protein diet).
5. **Deploy the serverless path.** Starts Azurite with `--skipApiVersionCheck`, uploads `All_Diets.csv` into the `datasets` container, and invokes `lambda_function.py`. Results are written again to `simulated_nosql/results.json`.

Logs and JSON are uploaded as the `simulated-deployment` artifact.

### Why this stays local

Azurite replaces Azure Blob Storage. A throwaway registry container replaces Docker Hub. The Python function is still started explicitly, because Azurite does not emit blob triggers. GitHub Actions only supplies the runner that executes those local tools.
