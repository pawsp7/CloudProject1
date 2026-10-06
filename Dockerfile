# Builder stage installs the scientific packages. The runtime stage below
# copies only those packages plus the two files the analysis needs, so the
# image does not carry tests, screenshots, or the rest of the repository.
FROM python:3.9-slim AS builder
WORKDIR /build
ARG HTTP_PROXY
ARG HTTPS_PROXY
COPY . /build
# Prefer local wheels.
RUN if [ -d /build/wheels ]; then \
      pip install --no-cache-dir --prefix=/install --no-index --find-links=/build/wheels pandas matplotlib seaborn; \
    else \
      pip install --no-cache-dir --prefix=/install pandas matplotlib seaborn; \
    fi

FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY data_analysis.py All_Diets.csv ./
ENV MPLBACKEND=Agg
ENV SHOW=0
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
CMD ["python", "data_analysis.py"]
