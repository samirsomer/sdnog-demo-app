FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependency list
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Expose FastAPI app port
EXPOSE 3000

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
