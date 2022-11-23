FROM python:3.10
WORKDIR /rowmate-backend
COPY ./requirements.txt /rowmate-backend/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /rowmate-backend/requirements.txt
COPY . /rowmate-backend
