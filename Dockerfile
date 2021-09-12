# Define base image
FROM continuumio/miniconda3

# Set working directory for the project
WORKDIR /app

# Install latest version of pyCSEP
# Todo: Build versioned base pyCSEP image
RUN conda install --channel conda-forge pycsep

# Copy everything into Docker container
ADD . /app

# Run experiment when container runs
ENTRYPOINT ["python", "/app/scripts/main_experiment.py"]
