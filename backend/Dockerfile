FROM python:3.12.8

# Copy the current directory contents into the container at /backend
COPY . /backend
COPY .env .

# Set the working directory
WORKDIR /backend

RUN pip install .

CMD ["start-app"]