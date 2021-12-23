FROM python:3.8-alpine
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers libpq-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY . .
CMD ["flask", "run"]