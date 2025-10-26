# Dockerfile

# 1. Use the official Python image as a base image
FROM python:3.13-slim

# 2. Set the working directory in the container
WORKDIR /app

# 3. Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. Install uv
RUN pip install uv

# 5. Copy the dependency files and install dependencies
COPY pyproject.toml uv.lock ./
RUN uv pip sync --no-cache

# 6. Copy the application code into the container
COPY ./app /app/app

# 7. Expose the port the app runs on
EXPOSE 8000

# 8. Define the command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
