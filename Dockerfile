FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md requirements.txt ./
COPY src ./src
COPY cwe_map.json ./cwe_map.json

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir .

EXPOSE 8080

CMD ["hexa-ai-server"]
