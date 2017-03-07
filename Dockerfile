FROM python:3.6

MAINTAINER Oliver Steele <steele@osteele.com>

# provide cached layer for requirements, beneath rest of sources
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT ["python3", "create-slideshow.py"]
