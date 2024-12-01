FROM python:3.9

WORKDIR app

COPY . /app

RUN pip install -r requirements.txt 

# Intentional error to trigger rollback
#RUN exit 1 
# This will cause the build to fail

EXPOSE 8002

CMD ["python","manage.py","runserver","0.0.0.0:8002"]
