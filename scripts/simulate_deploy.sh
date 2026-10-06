#!/usr/bin/env bash
# Simulated deployment: tag the locally built image, push it to a registry
# running on this machine, and run the container. No Docker Hub or Azure.
set -euo pipefail

IMAGE_NAME="${IMAGE_NAME:-diet-analysis}"
LOCAL_TAG="${LOCAL_TAG:-${IMAGE_NAME}:local}"
REGISTRY="${REGISTRY:-localhost:5001}"
TAG="${TAG:-latest}"
FULL="${REGISTRY}/${IMAGE_NAME}:${TAG}"

echo "=== Simulated deployment $(date) ==="
echo "Source image: ${LOCAL_TAG}"
echo "Registry image: ${FULL}"

docker tag "${LOCAL_TAG}" "${FULL}"

echo "=== Push to local registry ==="
docker push "${FULL}"

echo "=== Running container ==="
docker run --rm "${FULL}"
echo "=== Deployment finished $(date) ==="
