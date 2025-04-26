# pull official base image
FROM python:3.14.0a7-bookworm

#set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update -y && apt-get upgrade -y

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

CMD ["waitress-serve", "--threads=20", "--call", "peepin_pup:create_app"]
