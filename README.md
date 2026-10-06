# CloudProject1
Cloud-Native Nutritional Insights Application

## CI/CD (Task 4)

`.github/workflows/deploy.yml` runs on every push. It does not use Azure or Docker Hub.

1. Install dependencies from `requirements.txt` and run `pytest`.
2. Build the image from `Dockerfile` (`diet-analysis:local`).
3. Start a local registry on port 5001 and push `localhost:5001/diet-analysis:latest` (same image name as `docker-compose.yml`).
4. Run that image and keep the container log as deployment evidence.
5. Start Azurite, upload `All_Diets.csv`, and invoke `lambda_function.py`.

Local registry deploy, after `docker build -t diet-analysis:local .` and a registry on port 5001:

```bash
REGISTRY=localhost:5001 ./scripts/simulate_deploy.sh
```
