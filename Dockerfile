FROM python:3.12-slim

WORKDIR /app

# Copy all project files
COPY pyproject.toml .
COPY src/ src/

# Install the package and its dependencies
RUN pip install --no-cache-dir .

EXPOSE 8000

CMD ["python", "-m", "ynab_mcp"]
