import requests

# Задайте URL API контроллера
controller_url = 'http://ip-адрес-контроллера/api/temperature'

# Функция для получения данных о температуре
def get_temperature():
    response = requests.get(controller_url)
    data = response.json()
    return data['temperature']

# Функция для управления вентилятором
def control_fan(temperature, threshold=25):
    if temperature > threshold:
        # URL для включения вентилятора
        requests.post('http://ip-адрес-контроллера/api/fan', data={'state': 'on'})
        print("Вентилятор включен")
    else:
        # URL для выключения вентилятора
        requests.post('http://ip-адрес-контроллера/api/fan', data={'state': 'off'})
        print("Вентилятор выключен")

# Основной цикл программы
while True:
    current_temperature = get_temperature()
    control_fan(current_temperature)
