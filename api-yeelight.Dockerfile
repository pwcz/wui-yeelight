FROM python:3.10

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY src/api.py /code/api.py

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]