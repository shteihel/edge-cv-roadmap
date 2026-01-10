from ultralytics import YOLO
import cv2, time

def main():
    # На Raspberry Pi не забудь поменять на 'best_ncnn_model'!
    model = YOLO('yolo11n.pt') 
    cap = cv2.VideoCapture(0)
    cap.set(3, 320)
    cap.set(4, 320)

    if not cap.isOpened():
        print('Камера не обнаружена')
        return

    prev_time = time.time()
    frame_count = 0

    r = (0, 0, 255)   # Красный
    g = (0, 255, 0)   # Зеленый

    while True:
        ret, frame = cap.read()
        if ret is False:
            break

        if frame_count == 0:
            print(f'Разрешение {frame.shape}')
        
        results = model(frame, stream=True, verbose=False)

        for result in results:
            # 1. Сначала получаем картинку с рамками (всегда!)
            image_box = result.plot()
            
            # 2. Проверяем наличие дефектов
            # Используем len(result.boxes), это надежнее
            if len(result.boxes) > 0:
                # --- ТРЕВОГА (Красный) ---
                cv2.circle(image_box, (30, 30), 15, r, -1)
                cv2.putText(image_box, "ALARM", (60, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, r, 2)
            else:
                # --- НОРМА (Зеленый) ---
                # Этот блок теперь сработает, так как он не внутри if len > 0
                cv2.circle(image_box, (30, 30), 15, g, -1)
                cv2.putText(image_box, "OK", (60, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, g, 2)
            
            # 3. Сохраняем (тоже вынесли на уровень цикла for)
            if frame_count % 5 == 0:
                cv2.imwrite('live_data.jpg', image_box)

        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
        print(f"FPS: {fps:.1f}")
        frame_count += 1
        
    cap.release()

if __name__ == '__main__':
    main()