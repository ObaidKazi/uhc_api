# Use the official Python image as the base image
FROM python:3.10
WORKDIR /app
ADD requirements.txt .
COPY ./ /app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]