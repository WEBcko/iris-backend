FROM python:3.12.2-slim

WORKDIR /app

ARG SECRET_KEY
ARG JWT_SECRET_KEY

ENV SECRET_KEY=${SECRET_KEY}
ENV JWT_SECRET_KEY=${JWT_SECRET_KEY}

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY . .

RUN chmod +x entrypoint.sh

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
