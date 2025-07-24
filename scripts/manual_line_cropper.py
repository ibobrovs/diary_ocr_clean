import cv2
import os

# 🔁 Настройки путей
img_path = "../data/images/page-000.png"   # используем НЕ бинарное изображение!
output_dir = "../data/lines"
lines_txt_path = "../data/gt/lines.txt"

os.makedirs(output_dir, exist_ok=True)
lines_txt = []

# 🧠 Переменные
clone = cv2.imread(img_path)
image = clone.copy()
cropping = False
start_point = ()
end_point = ()
line_counter = 1

# 💡 Обработка мыши
def mouse_crop(event, x, y, flags, param):
    global start_point, end_point, cropping, line_counter, image, clone

    if event == cv2.EVENT_LBUTTONDOWN:
        start_point = (x, y)
        cropping = True

    elif event == cv2.EVENT_MOUSEMOVE and cropping:
        img_copy = clone.copy()
        cv2.rectangle(img_copy, start_point, (x, y), (0, 255, 0), 1)
        cv2.imshow("Выдели строку", img_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        end_point = (x, y)
        cropping = False

        x1, y1 = start_point
        x2, y2 = end_point

        # нормализуем координаты
        roi = clone[min(y1,y2):max(y1,y2), min(x1,x2):max(x1,x2)]
        if roi.size == 0:
            print("⚠️ Пустое выделение — пропущено.")
            return

        # сохраняем строку
        filename = f"line_{line_counter:04}.png"
        full_path = os.path.join(output_dir, filename)
        cv2.imwrite(full_path, roi)
        print(f"✅ Сохранено: {filename}")

        # просим текст строки
        line_text = input(f"✍️ Введите текст для {filename}: ").strip()
        lines_txt.append(f"data/lines/{filename}\t{line_text}")
        line_counter += 1

        cv2.imshow("Выдели строку", clone)

# 🖼 Запуск окна
cv2.namedWindow("Выдели строку")
cv2.setMouseCallback("Выдели строку", mouse_crop)
cv2.imshow("Выдели строку", clone)
print("\n🔧 Используй мышь для выделения строки (нажми → потяни → отпусти)\nНажми ESC чтобы выйти.\n")

# Ожидание выхода
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        break

cv2.destroyAllWindows()

# 💾 Сохраняем lines.txt
os.makedirs(os.path.dirname(lines_txt_path), exist_ok=True)
with open(lines_txt_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines_txt))

print(f"\n📄 Готово! Разметка записана в: {lines_txt_path}")
