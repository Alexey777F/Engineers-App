FROM python:3.9.18-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install -y \
    gcc \
    libc-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /project

COPY . /project

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "main.py"]