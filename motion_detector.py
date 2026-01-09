import cv2

def main():
    cap = cv2.VideoCapture(0)
    if  not cap.isOpened():
        print('Камера не обнаружена')
        return
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    print(f'Разрешение записи: {frame_width}x{frame_height}')
    
    fourcc = cv2.VideoWriter_fourcc(*"XVID")

    out = cv2.VideoWriter('evidence.avi', fourcc, 20.0, (frame_width, frame_height))

    try:
        prev_frame = None
        print('Система охраны запущена. Нажмми CTRL+C для выхода.')
        while True:
            ret, frame = cap.read()
            if ret is False:
                print("Кадра нет")
                break
            else:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (21, 21), 0)
                if prev_frame is None:
                    prev_frame = gray
                    continue
                delta = cv2.absdiff(prev_frame, gray)
                _, thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)
                if cv2.countNonZero(thresh) >= 1000:
                    print(f'Движение {cv2.countNonZero(thresh)}')
                    out.write(frame)
                prev_frame = gray
                
                

    except KeyboardInterrupt:
        print('Остановка скрипта')
        
    finally:
        cap.release()

        out.release()
        print('Камера выключена. Видео сохранено в evidence.avi')


if __name__ == '__main__':
    main()