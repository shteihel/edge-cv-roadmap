import cv2

def main():
    img = cv2.imread('created_image.jpg')
    if img is None:
        print("Изображение отсутсвует в текущем ремозитории")
    
    img_g = img.copy()
    #Создаем маску
    img_g = cv2.cvtColor(img_g, cv2.COLOR_BGR2GRAY)
    #Создаем порог
    _, thr_img = cv2.threshold(img_g, 50, 255, cv2.THRESH_BINARY)
    #Ищем контуры
    contours, hierarchy = cv2.findContours(thr_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0, 255, 255), 2)
    cv2.imwrite('musk.jpg', thr_img)
    cv2.imwrite('result.jpg', img)
    print(f'Найдено объектов {len(contours)}')

# ... (начало стандартное: чтение, порог, поиск контуров RETR_TREE) ...

    print(f"Найдено контуров: {len(contours)}")

    for cnt in contours:
        # 1. Считаем моменты
        M = cv2.moments(cnt)
    
    # ЗАЩИТА: Если площадь (M['m00']) равна 0 (шум), делить нельзя!
        if M['m00'] != 0:
            cX = int(M['m10'] / M['m00'])
            cY = int(M['m01'] / M['m00'])
        else:
        # Если площадь 0, пропускаем этот контур
            cX, cY = 0, 0
            continue

    # 2. Рисуем точку центра (на ОРИГИНАЛЕ)
    # (cX, cY) - координаты, 5 - радиус, (255, 255, 255) - белый, -1 - закрашенный
        cv2.circle(img_g, (cX, cY), 5, (255, 255, 255), -1)
    
    # 3. Пишем текст координат
    # cv2.putText(куда, текст, (x,y), шрифт, размер, цвет, толщина)
        cv2.putText(img_g, f"x:{cX} y:{cY}", (cX - 20, cY - 20), 
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # 4. Обводим сам контур (для красоты)
        cv2.drawContours(img_g, [cnt], -1, (0, 255, 255), 2)

    # Сохраняем результат
        cv2.imwrite('radar_result.jpg', img_g)
if __name__ == '__main__':
    main()
