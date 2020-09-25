From python



WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENV PYTHONPATH "/app"
CMD ["python","app.py"]
