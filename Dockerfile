From python

RUN pip install -r /backed/requirments.txt
COPY /backend /tmp/pet-share-backend/


CMD ["python","/tmp/pet-share-backedn/app.py"]
