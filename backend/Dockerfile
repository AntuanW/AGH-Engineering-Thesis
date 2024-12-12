FROM python:3.12.8-slim

# Set the working directory
WORKDIR /backend

# Copy the current directory contents into the container at /backend
COPY . /backend

# Create and activate virtual environment
RUN python -m venv .venv && \
    . .venv/bin/activate && \
    pip install --no-cache-dir .

# Set the environment PATH for the virtual environment
ENV PATH="/backend/.venv/bin:$PATH"

EXPOSE 8000

# Run the application
CMD ["start-app"]
