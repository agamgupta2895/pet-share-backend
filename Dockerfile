From python

#COPY /backend ./tmp/pet-share-backend/
COPY ./ ./
#WORKDIR /tmp/pet-share-backend/backend
RUN pip install -r requirements.txt


CMD ["python","./backend/app.py"]
