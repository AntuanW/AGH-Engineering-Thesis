FROM python:3.12.8

# Install Java
RUN apt-get update && apt-get install -y default-jre

# Install ping for healthcheck
RUN apt-get install -y iputils-ping

# Copy the current directory contents into the container at /backend
COPY . /backend
COPY .env .

# Set the working directory
WORKDIR /backend

RUN mkdir -p /backend/tmp

RUN pip install .

CMD ["start-app"]