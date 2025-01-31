# Use an official Python runtime
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all project files
COPY . .

# Expose the port for Streamlit
EXPOSE 8501

# Run Streamlit app with the correct port
CMD ["sh", "-c", "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.enableCORS false"]