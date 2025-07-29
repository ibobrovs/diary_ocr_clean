import os
from lxml import etree
from pathlib import Path

# Путь до папки с изображениями и где будут храниться XML
image_dir = Path("data/train")
text_file = Path("data/gt/lines.txt")  # Твой файл со строками

# Чтение строк
with open(text_file, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

# Генерация XML-файлов
for idx, text in enumerate(lines, start=1):
    image_name = f"line_{idx:04d}.png"
    xml_name = image_dir / f"line_{idx:04d}.xml"

    # Создание структуры PAGE XML
    PcGts = etree.Element("PcGts", nsmap={None: "http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15"})
    page = etree.SubElement(PcGts, "Page", imageFilename=image_name, imageWidth="800", imageHeight="50")
    text_region = etree.SubElement(page, "TextRegion", id="r1")
    text_line = etree.SubElement(text_region, "TextLine", id="l1")
    coords = etree.SubElement(text_line, "Coords", points="0,0 800,0 800,50 0,50")
    text_equiv = etree.SubElement(text_line, "TextEquiv")
    unicode_elem = etree.SubElement(text_equiv, "Unicode")
    unicode_elem.text = text

    # Сохранение XML
    tree = etree.ElementTree(PcGts)
    tree.write(str(xml_name), encoding="UTF-8", xml_declaration=True, pretty_print=True)

print(f"✅ Сгенерировано {len(lines)} PAGE XML файлов в {image_dir}")
