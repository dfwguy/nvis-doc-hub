FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 NVIS_HUB_DB=/data/hub.sqlite3
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir . && useradd --uid 10001 --create-home hub && mkdir /data && chown hub /data
USER hub
VOLUME ["/data"]
EXPOSE 8000
ENTRYPOINT ["nvis-hub"]
CMD ["serve", "--host", "0.0.0.0", "--port", "8000"]
