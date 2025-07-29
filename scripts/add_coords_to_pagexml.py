import os
from lxml import etree

# Папка с PAGE XML файлами
xml_dir = 'data/train'

# Обходим каждый файл в папке
for fname in os.listdir(xml_dir):
    if fname.endswith('.xml'):
        path = os.path.join(xml_dir, fname)

        # Парсим XML-файл
        tree = etree.parse(path)
        root = tree.getroot()

        # Учитываем namespace PAGE XML
        ns = {'ns': 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15'}

        # Извлекаем <Page> и его размеры
        page = root.find('ns:Page', ns)
        width = page.get('imageWidth', '800')
        height = page.get('imageHeight', '50')

        # Добавляем <Coords> в TextRegion
        for region in root.xpath('//ns:TextRegion', namespaces=ns):
            if region.find('ns:Coords', namespaces=ns) is None:
                coords = etree.Element('{http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15}Coords')
                coords.set('points', f'0,0 {width},0 {width},{height} 0,{height}')
                region.insert(0, coords)

        # Добавляем <Coords> в TextLine
        for line in root.xpath('//ns:TextLine', namespaces=ns):
            if line.find('ns:Coords', namespaces=ns) is None:
                coords = etree.Element('{http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15}Coords')
                coords.set('points', f'0,0 {width},0 {width},{height} 0,{height}')
                line.insert(0, coords)

        # Сохраняем изменения обратно в XML
        tree.write(path, encoding='UTF-8', xml_declaration=True)
        print(f'✅ Обновлён: {fname}')
