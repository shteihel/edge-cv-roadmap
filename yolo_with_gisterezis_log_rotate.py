from ultralytics import YOLO
import cv2, time
from datetime import datetime
import os
import glob

def manage_storage():
    list_of_files = glob.glob('defect_*.jpg')
    
    if len(list_of_files) > 5:
        list_of_files.sort(key=os.path.getctime)
        old_file = list_of_files[0]
        os.remove(old_file)
        print(f'РОТАЦИЯ: Удален старый файл {old_file}')

def main():
    # --- 1. НАСТРОЙКА ---
    model = YOLO('yolo11n.pt') 
    cap = cv2.VideoCapture(0)
    cap.set(3, 320)
    cap.set(4, 320)

    if not cap.isOpened():
        print('Камера не обнаружена')
        return

    # --- 2. ИНИЦИАЛИЗАЦИЯ ПЕРЕМЕННЫХ ---
    # ТУТ нужны:
    # - Пороги (TRIGGER_THRESH, CLEAN_THRESH)
    # - Счетчики (defect_streak, clean_streak)
    # - Флаг состояния (alarm_active)
    # - Цвета (RED, GREEN)
    
    TRIGGER_TRESH = 5
    CLEAN_THRESH = 10

    defect_streak = 0
    clean_streak = 0

    alarm_active = False

    red = (0, 0, 255)
    green = (0, 255, 0)


    prev_time = time.time()
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret: break
        
        # Инференс
        results = model(frame, stream=True, verbose=False)

        for result in results:
            # Картинка для рисования
            final_image = result.plot()
            
            # --- 3. ЛОГИКА () ---
            if len(result.boxes) > 0:
                is_defect_now = True
            else:
                is_defect_now = False
            
            if is_defect_now == True:
                defect_streak += 1
                clean_streak = 0
                if defect_streak >= 5:
                    alarm_active = True
                
            else:
                clean_streak += 1
                defect_streak = 0
                if clean_streak >= CLEAN_THRESH:
                    alarm_active = False
                
            
            if alarm_active == True and frame_count % 30 == 0:
                    tim = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                    name_img = f'defect_{tim}.jpg'
                    cv2.imwrite(name_img, final_image)
                    with open('events_log.csv', 'a') as f:
                        f.write(f'{tim},ALARM,{name_img}\n')
                    print(name_img)

                    manage_storage()

            if alarm_active == True:
                cv2.circle(final_image, (30, 30), 15, red, -1 )
                cv2.putText(final_image, 'ALARM', (60, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2)
            else:
                cv2.circle(final_image, (30, 30), 15, green, -1)
                cv2.putText(final_image, "OK", (60, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, green, 2)


            if frame_count % 5 == 0:
                cv2.imwrite('live_view.jpg', final_image)

        # Расчет FPS (Оставляем)
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
        prev_time = curr_time
        # Можешь добавить вывод счетчиков в принт для отладки
        print(f"FPS: {fps:.1f}") 
        
        frame_count += 1
    
    cap.release()

if __name__ == '__main__':
    main()