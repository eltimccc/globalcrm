import random
import string
import datetime
from django.contrib.auth.models import User
from tasks.models import Task  # Подставьте правильный путь к вашей модели Task

# Функция для создания случайной строки
def random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

# Функция для создания случайной даты
def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + datetime.timedelta(days=random_days)

# Создаем 10000 задач
for _ in range(100):
    title = random_string(20)
    description = random_string(50)
    deadline = random_date(datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days=365))
    created_by = User.objects.order_by('?').first()  # Случайный пользователь
    worker = User.objects.order_by('?').first()  # Случайный пользователь
    completed = random.choice([True, False])
    completed_at = random_date(datetime.datetime.now() - datetime.timedelta(days=365), datetime.datetime.now()) if completed else None

    Task.objects.create(
        title=title,
        description=description,
        deadline=deadline,
        created_by=created_by,
        worker=worker,
        completed=completed,
        completed_at=completed_at
    )

print("Задачи успешно добавлены в базу данных.")