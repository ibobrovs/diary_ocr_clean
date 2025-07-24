import cv2
import os

image_path = '../data/binarized/page-000.png'  # заменяй имя файла здесь
output_img_dir = '../gt/images'
output_txt_path = '../gt/lines.txt'

os.makedirs(output_img_dir, exist_ok=True)
lines = []

image = cv2.imread(image_path)
clone = image.copy()
roi_count = 0

def crop_and_save(event, x, y, flags, param):
    global ref_point, cropping, roi_count

    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]
        cropping = True

    elif event == cv2.EVENT_LBUTTONUP:
        ref_point.append((x, y))
        cropping = False

        x1, y1 = ref_point[0]
        x2, y2 = ref_point[1]

        roi = clone[min(y1,y2):max(y1,y2), min(x1,x2):max(x1,x2)]

        # Показываем выделенную строку
        cv2.imshow("Выделенная строка", roi)
        print("Введите текст строки:")
        text = input("> ")

        # Сохраняем
        filename = f"line_{roi_count:04}.png"
        filepath = os.path.join(output_img_dir, filename)
        cv2.imwrite(filepath, roi)

        lines.append(f"{filename}\t{text}")
        roi_count += 1

        print("✅ Сохранено:", filename)
        print("Выделите следующую строку...")

cv2.namedWindow("Выдели строку")
cv2.setMouseCallback("Выдели строку", crop_and_save)

print("🔧 Инструкция: выделяй строку мышкой слева направо, затем введи текст.")
cv2.imshow("Выдели строку", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Сохраняем текстовую разметку
with open(output_txt_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"\n📄 Готово! Разметка записана в: {output_txt_path}")
