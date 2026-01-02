counter = 0
threshold = 46.0
try:
    with open('system_status.csv', 'r') as f:
        for line in f:
            parts = line.split(",")
            try:
                t = float(parts[1])

                if t > threshold:
                    timestamp = parts[0]
                    print(f'WARNING: Перегрев {t}°C в {timestamp}')
                    counter += 1
            except ValueError:
                continue
    print(f'--------------------------')
    print(f'Всего перегревов: {counter}')

except FileNotFoundError:
    print("Ошибка: Файл system_status.csv не найден. Запусти monitor_service.py!")