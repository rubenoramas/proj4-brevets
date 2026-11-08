FROM python:3.11-slim
LABEL maintainer="Ruben Oramas <ruben.oramas05@gmail.com>"
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["python"]
CMD ["flask_brevets.py"]
