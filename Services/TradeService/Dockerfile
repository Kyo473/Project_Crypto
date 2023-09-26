FROM python:3.11
WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt
COPY ./app /src/app
CMD ["alembic", "stamp", "head"]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
