FROM python:3.11-slim

# Install LibreOffice + Headless dependencies
RUN apt update && apt install -y \
    libreoffice \
    libreoffice-java-common \
    libxinerama1 \
    libfontconfig1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Set Environment Variable so Python knows where LibreOffice lives
ENV OFFICE_PATH=/usr/bin/libreoffice

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure the temporary directory for conversions exists
RUN mkdir -p /app/temp

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]