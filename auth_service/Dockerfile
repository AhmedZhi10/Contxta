# =========================
# 1️⃣ Base image
# =========================
FROM python:3.13-slim

# =========================
# 2️⃣ Environment variables
# =========================
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PIP=1

# =========================
# 3️⃣ Working directory
# =========================
WORKDIR /app

# =========================
# 4️⃣ Install system deps
# =========================
RUN apt-get update && apt-get install -y \
    build-essential \
    libmariadb-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# =========================
# 5️⃣ Install uv
# =========================
RUN pip install --no-cache-dir uv

# =========================
# 6️⃣ Copy files to container
# =========================
COPY . /app

# =========================
# 7️⃣ Install Python deps
# =========================
RUN uv pip install --system --no-cache .

# =========================
# 8️⃣ Expose port
# =========================
EXPOSE 8000

# =========================
# 9️⃣ Run Django app
# =========================
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]