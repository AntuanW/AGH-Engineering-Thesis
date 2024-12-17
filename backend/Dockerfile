FROM python:3.12.8

# Install Java
RUN apt-get update && apt-get install -y default-jre

# Install fontconfig for managing fonts
RUN apt-get update && apt-get install -y \
    fontconfig \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a directory for custom fonts
RUN mkdir -p /usr/share/fonts/truetype/custom

# Copy the font file into the container
COPY /app/pdf_generator/static/ /usr/share/fonts/truetype/custom/

# Refresh font cache
RUN fc-cache -fv

# Copy the current directory contents into the container at /backend
COPY . /backend
COPY .env .

# Set the working directory
WORKDIR /backend

RUN pip install .

CMD ["start-app"]