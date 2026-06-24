FROM python:3.12-slim

# Install Java
RUN apt-get update && apt-get install -y \
    default-jdk \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Java Environment
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH=$JAVA_HOME/bin:$PATH

# Install PySpark and JupyterLab
RUN pip install --no-cache-dir \
    pyspark==3.5.1 \
    jupyterlab

# Working Directory
WORKDIR /workspace

# Copy notebook files
COPY . .

# Expose Jupyter port
EXPOSE 9999

# Start Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=9999", "--no-browser", "--allow-root"]