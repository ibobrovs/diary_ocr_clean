import cv2
import os
import matplotlib.pyplot as plt

INPUT_DIR = "data/images"
OUTPUT_DIR = "data/binarized"
VISUALIZE = True  # включить отображение до/после

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Получаем список PNG-файлов, отсортированных по имени
files = sorted(f for f in os.listdir(INPUT_DIR) if f.endswith(".png"))

for filename in files:
    input_path = os.path.join(INPUT_DIR, filename)
    output_path = os.path.join(OUTPUT_DIR, filename)

    # Загружаем изображение в оттенках серого
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print(f"[!] Пропущен: {filename} (не удалось прочитать)")
        continue

    # Адаптивная бинаризация
    binary = cv2.adaptiveThreshold(
        img,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  # метод пороговой обработки
        cv2.THRESH_BINARY,
        25,   # размер блока пикселей (должен быть нечётным)
        15    # смещение от среднего (чем больше, тем светлее)
    )

    # Сохраняем бинаризованный файл
    cv2.imwrite(output_path, binary)
    print(f"[✓] Сохранено: {output_path}")

    # Визуализация до/после
    if VISUALIZE:
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))
        axs[0].imshow(img, cmap="gray")
        axs[0].set_title("Оригинал")
        axs[0].axis("off")

        axs[1].imshow(binary, cmap="gray")
        axs[1].set_title("Бинаризация (adaptive)")
        axs[1].axis("off")

        plt.suptitle(f"Файл: {filename}")
        plt.tight_layout()
        plt.show()
