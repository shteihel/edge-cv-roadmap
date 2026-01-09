from ultralytics import YOLO
import cv2, time


def main():
    model = YOLO('yolo11n.pt')
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    if not cap.isOpened():
        print('Камера не обнаружена')
        return

    prev_time = time.time()
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if ret is False:
            break

        if frame_count == 0:
            print(f'Разрешение {frame.shape}')
        results = model(frame, stream=True, verbose=False)


        for result in results:
            classes = result.boxes.cls.cpu().numpy()

            if len(classes) > 0:
                for cls in classes:
                    name = model.names[int(cls)]
                    pass

            if frame_count % 30 == 0:
                image_box = result.plot()
                cv2.imwrite('live_view.jpg', image_box)

        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
        print(fps)
        frame_count += 1
        
        
    
    cap.release()



if __name__ == '__main__':
    main()
