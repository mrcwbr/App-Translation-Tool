FROM python:3.7

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD ["python", "app.py"]

# docker build -t mrcwbr/app-translation-tool:latest .
# docker push mrcwbr/app-translation-tool:latest