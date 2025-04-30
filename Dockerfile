
FROM python:3.12.2-slim

WORKDIR /app

ARG SECRET_KEY
ARG DATABASE_URL
ARG JWT_SECRET_KEY

ENV SECRET_KEY=${SECRET_KEY}
ENV DATABASE_URL=${DATABASE_URL}
ENV JWT_SECRET_KEY=${JWT_SECRET_KEY}

COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY . .


EXPOSE 5000

CMD ["flask", "db", "upgrade"]
CMD ["flask", "run", "--host=0.0.0.0"]
