# Use the official Miniconda3 image from Docker Hub
FROM continuumio/miniconda3

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create the conda environment from the environment.yml file
RUN conda env create -f environment.yml

# Initialize conda in bash
SHELL ["/bin/bash", "-c"]
RUN echo "source activate agentic-ai" > ~/.bashrc
ENV PATH /opt/conda/envs/agentic-ai/bin:$PATH

# Expose the port that streamlit uses
EXPOSE 8501

# Run the streamlit app
CMD ["streamlit", "run", "./coding_components/app.py"]