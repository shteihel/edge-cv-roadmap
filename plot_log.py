import pandas as pd
import matplotlib.pyplot as plt
import argparse

def main():
    # 1. Читаем аргументы (какой файл рисовать)
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default='system_status.csv')
    args = parser.parse_args()

    # 2. Загружаем данные через Pandas
    # names=['Time', 'Temp', 'RAM'] — даем названия колонкам, т.к. в CSV их нет
    try:
        df = pd.read_csv(args.file, names=['Time', 'Temp', 'RAM'])
    except FileNotFoundError:
        print("Файл не найден!")
        return

    # Превращаем колонку Time из текста в настоящий формат времени
    df['Time'] = pd.to_datetime(df['Time'])

    # 3. Рисуем график
    plt.figure(figsize=(10, 6)) # Размер картинки

    # Подграфик 1: Температура
    plt.subplot(2, 1, 1) # (2 строки, 1 колонка, график номер 1)
    plt.plot(df['Time'], df['Temp'], color='red', label='CPU Temp')
    plt.ylabel('Temp (°C)')
    plt.legend()
    plt.grid(True)

    # Подграфик 2: Память
    plt.subplot(2, 1, 2) # (2 строки, 1 колонка, график номер 2)
    plt.plot(df['Time'], df['RAM'], color='blue', label='RAM Usage')
    plt.ylabel('RAM (%)')
    plt.xlabel('Time')
    plt.legend()
    plt.grid(True)

    # 4. Сохраняем в файл (так как монитора нет)
    output_file = 'monitor_report.png'
    plt.savefig(output_file)
    print(f"График сохранен в {output_file}")

if __name__ == "__main__":
    main()