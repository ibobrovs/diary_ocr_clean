# fix_image_paths.py
import os
from lxml import etree

xml_dir = 'data/train'

for fname in os.listdir(xml_dir):
    if fname.endswith('.xml'):
        path = os.path.join(xml_dir, fname)
        tree = etree.parse(path)
        root = tree.getroot()
        
        page_elem = root.find('.//{http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15}Page')
        if page_elem is not None:
            image_file = page_elem.attrib['imageFilename']
            image_file = os.path.join('data/train', image_file)
            page_elem.attrib['imageFilename'] = image_file

            tree.write(path, encoding='UTF-8', xml_declaration=True)
            print(f"✅ Обновлено: {fname}")
