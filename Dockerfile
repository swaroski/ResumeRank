#Use Python 3.6.5 container image
FROM python:3.6.5

# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt

#Install the dependencies
RUN pip install -r requirements.txt

# Mounts the application code to the image
COPY . code
WORKDIR /code

EXPOSE 5000

CMD python app.py

#Run the command to start uWSGI
CMD ["uwsgi", "app.ini"]
