# Импорт стандартных модулей
import os  # Для работы с файловой системой
import xml.etree.ElementTree as ET  # Для разбора XML-документов
from PIL import Image  # Для проверки открытия изображений

# Папка, где находятся XML-файлы и соответствующие изображения
xml_dir = 'data/train'

# Список для хранения ошибок (на будущее, сейчас не используется)
errors = []

# Функция, проверяющая один XML-файл
def check_file(xml_path):
    try:
        # Парсим XML-документ
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Пространство имён, используемое в PageXML
        ns = {'ns': 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15'}

        # Ищем элемент <Page> внутри XML
        page = root.find('.//ns:Page', ns)
        if page is None:
            return "❌ No <Page> element"  # Если нет элемента <Page>, это ошибка

        # Получаем имя изображения, указанное в атрибуте imageFilename
        img_file = page.get('imageFilename')
        if not img_file:
            return "❌ Missing imageFilename"  # Если не указан путь к изображению

        # Полный путь к изображению (предполагается, что оно лежит в той же папке)
        img_path = img_file if os.path.isabs(img_file) else os.path.join(xml_dir, os.path.basename(img_file))

        # Проверка существования файла изображения
        if not os.path.isfile(img_path):
            return f"❌ Image not found: {img_file}"

        # Проверка, можно ли открыть изображение (например, оно не повреждено)
        try:
            Image.open(img_path)
        except:
            return f"❌ Image cannot be opened: {img_file}"

        # Ищем все элементы <TextRegion> (области текста)
        regions = page.findall('.//ns:TextRegion', ns)
        if not regions:
            return "❌ No <TextRegion> elements"  # Если нет ни одной текстовой области

        # Обрабатываем каждую текстовую область
        for region in regions:
            # Проверяем наличие координат у области
            if region.find('ns:Coords', ns) is None:
                return "❌ Region without Coords"

            # Ищем все строки текста внутри этой области
            textlines = region.findall('.//ns:TextLine', ns)
            if not textlines:
                return "❌ No <TextLine> elements"  # Если строк нет — ошибка

            # Проверка каждой строки
            for line in textlines:
                # Должна быть геометрия (координаты) строки
                if line.find('ns:Coords', ns) is None:
                    return "❌ TextLine without Coords"

                # Проверка наличия текста (<Unicode>)
                unicode_elem = line.find('.//ns:Unicode', ns)
                # Если нет <Unicode> или текст пустой
                if unicode_elem is None or not unicode_elem.text.strip():
                    return "❌ TextLine without Unicode text"

        # Если всё прошло — XML пригоден
        return "✅ Valid"

    # Обработка ошибки парсинга XML
    except ET.ParseError:
        return "❌ XML parsing error"
    # Общая ошибка (например, файловая)
    except Exception as e:
        return f"❌ Unexpected error: {e}"

# === Основной блок запуска скрипта ===

# Выводим заголовок проверки
print("📄 Проверка XML файлов...\n")

# Обход всех файлов в папке
for fname in sorted(os.listdir(xml_dir)):
    # Только те, что заканчиваются на .xml
    if fname.endswith('.xml'):
        # Полный путь до файла
        xml_path = os.path.join(xml_dir, fname)
        # Выполняем проверку
        result = check_file(xml_path)
        # Печатаем имя файла и результат
        print(f"{fname:20} → {result}")
