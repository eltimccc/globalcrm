from cars.models import Car

# Замените значения ниже на фактические данные
model = "Mercedes"
license_plate = "FFR23"
year = 2022
color = "Blue"
registration_number = "RN1234"
registration_date = "2022-01-01"

# Создаем экземпляр Car и сохраняем его в базе данных
car = Car.objects.create(
    model=model,
    license_plate=license_plate,
    year=year,
    color=color,
    registration_number=registration_number,
    registration_date=registration_date,
)

# Выводим информацию об автомобиле
print(f"Car added: {car}")
