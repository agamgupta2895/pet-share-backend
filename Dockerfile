From python

#COPY /backend ./tmp/pet-share-backend/
COPY ./ ./
#WORKDIR /tmp/pet-share-backend/backend
RUN pip install -r requirements.txt

ENV PYTHONPATH "/backend"
CMD ["sh","-c","python /backend/app.py"]
