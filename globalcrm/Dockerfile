FROM python:3.11-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py migrate && \
    python manage.py collectstatic --noinput

# CMD ["gunicorn", "globalcrm.wsgi:application", "--bind", "0:8000", "--reload"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]