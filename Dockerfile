From python

#COPY /backend ./tmp/pet-share-backend/
COPY ./ ./
#WORKDIR /tmp/pet-share-backend/backend
RUN pip install -r requirements.txt

ENV PYTHONPATH "/backend/Services"
ENV PYTHONPATH "/backend/modules" 
ENV PYTHONPATH "/backend/Cosntants"
ENV PYTHONPATH "/backend/CommonUtils"

CMD ["python","/backend/app.py"]
