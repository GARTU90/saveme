FROM Python 3.12.7
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "ubicacion.py"]
