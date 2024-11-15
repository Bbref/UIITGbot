import cv2
from fer import FER

# Загрузка модели
detector = FER()


def main():
    # Путь к изображению
    path_to_img = 'img.png'

    # Загрузка изображения
    img = cv2.imread(path_to_img)

    # Предикт модели
    results = detector.detect_emotions(img)
    if results:
        # Извлечение эмоций и определение максимальной
        emotions = results[0]['emotions']
        dominant_emotion = max(emotions, key=emotions.get)  # Находим эмоцию с максимальным значением
        print(f"Доминирующая эмоция: {dominant_emotion}")
    else:
        print("На изображении не обнаружены лица.")


if __name__ == '__main__':
    main()
