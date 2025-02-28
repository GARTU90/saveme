FROM python:3.12
WORKDIR /app
COPY . .
EXPOSE 80
RUN pip install -r requirements.txt
CMD ["python", "ubicacion.py"]
