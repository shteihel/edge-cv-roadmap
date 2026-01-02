import time
import argparse
import csv
import sys
import psutil
from datetime import datetime

# --- ЧАСТЬ 1: ФУНКЦИЯ ПОЛУЧЕНИЯ ТЕМПЕРАТУРЫ ---
def get_cpu_temp() -> float:
    try:
        # Открываем системный файл, где лежит температура
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            content = f.read()       # Читаем (например: "45123")
            temp = int(content) / 1000.0 # Делим на 1000 (получаем 45.123)
            return temp
    except FileNotFoundError:
        # Если запустишь на Windows, файла не будет - вернем заглушку
        return 0.0

# --- ЧАСТЬ 2: ФУНКЦИЯ ЗАПИСИ В CSV ---
def write_to_csv(filename: str, temp: float, ram:float):
    # Получаем текущее время (год-месяц-день час:минута:секунда)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ram = psutil.virtual_memory().percent
    
    # Открываем файл. Режим 'a' (append) значит "дописать в конец", а не стирать.
    # newline='' нужен, чтобы в CSV не было пустых строк между данными
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([now, temp, ram]) # Записываем список: [время, температура]

# --- ЧАСТЬ 3: ГЛАВНЫЙ БЛОК УПРАВЛЕНИЯ ---
def main():
    # 1. Настройка "Пульта управления" (Argparse)
    # Это позволяет запускать скрипт с параметрами, например:
    # python monitor_service.py --interval 2
    parser = argparse.ArgumentParser(description='Монитор температуры RPi')
    
    # Добавляем настройку интервала (по умолчанию 5 секунд)
    parser.add_argument('--interval', type=int, default=5, help='Пауза между замерами (сек)')
    
    # Добавляем настройку имени файла (по умолчанию system_status.csv)
    parser.add_argument('--filename', type=str, default='system_status.csv', help='Имя файла для логов')
    
    # Эта команда читает то, что ты написал в консоли, и кладет в переменную args
    args = parser.parse_args()

    print(f"--- ЗАПУСК МОНИТОРИНГА ---")
    print(f"Интервал: {args.interval} сек")
    print(f"Запись в файл: {args.filename}")
    print(f"Нажми Ctrl+C для остановки")

    # 2. Вечный цикл (пока не нажмешь Ctrl+C)
    try:
        while True:
            t = get_cpu_temp()              # 1. Узнали температуру
            ram = psutil.virtual_memory().percent
            print(f"Текущая t: {t}°C")      # 2. Показали на экране
            print(f'Текущая загрузка RAM: {ram}%')
            write_to_csv(args.filename, t, ram)  # 3. Записали в книгу
            time.sleep(args.interval)       # 4. Уснули на N секунд
            
    except KeyboardInterrupt:
        print("\nОстановка пользователем. Пока!")

# Это стандартная проверка: "Если этот файл запустили напрямую, а не импортировали"
if __name__ == "__main__":
    main()