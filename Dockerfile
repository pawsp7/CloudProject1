FROM python:3.9-slim
WORKDIR /app
COPY . /app
ARG HTTP_PROXY
ARG HTTPS_PROXY
# Prefer local wheels.
RUN if [ -d /app/wheels ]; then \
      pip install --no-cache-dir --no-index --find-links=/app/wheels pandas matplotlib seaborn; \
    else \
      pip install --no-cache-dir pandas matplotlib seaborn; \
    fi
ENV MPLBACKEND=Agg
ENV SHOW=0
CMD ["python", "data_analysis.py"]
