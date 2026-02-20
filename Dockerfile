# 1. Base Image: We start with a lightweight version of Python
FROM python:3.12-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy just the requirements first (this makes building faster later)
COPY requirements.txt .

# 4. Install all your dependencies (FastAPI, Uvicorn, Gunicorn, SQLAlchemy, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your API code into the container
COPY . .

# 6. Expose the port Gunicorn will run on
EXPOSE 8000

# 7. The exact command to start your server, just like you ran in the terminal
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000"]


