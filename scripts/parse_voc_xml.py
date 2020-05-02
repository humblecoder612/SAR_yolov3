# coding: utf-8

import xml.etree.ElementTree as ET
import os

names_dict = {}
cnt = 0
f = open('./voc_names.txt', 'r').readlines()
for line in f:
    line = line.strip()
    names_dict[line] = cnt
    cnt += 1

voc_07 = '../data/my_data/'
#voc_12 = '/data/my_data/'

anno_path = [os.path.join(voc_07, 'Annot')]
img_path = [os.path.join(voc_07, 'Images')]

trainval_path = [os.path.join(voc_07, 'train.txt')]
test_path = [os.path.join(voc_07, 'test.txt')]


def parse_xml(path):
    tree = ET.parse(path)
    img_name = path.split('/')[-1][:-4]
    
    height = tree.findtext("./size/height")
    width = tree.findtext("./size/width")

    objects = [img_name, width, height]

    for obj in tree.findall('object'):
        #difficult = obj.find('difficult').text
        #if difficult == '1':
        #    continue
        name = obj.find('name').text
        bbox = obj.find('bndbox')
        xmin = bbox.find('xmin').text
        ymin = bbox.find('ymin').text
        xmax = bbox.find('xmax').text
        ymax = bbox.find('ymax').text

        name = str(names_dict[name])
        objects.extend([name, xmin, ymin, xmax, ymax])
    if len(objects) > 1:
        return objects
    else:
        return None

test_cnt = 0
def gen_test_txt(txt_path):
    global test_cnt
    f = open(txt_path, 'w')

    for i, path in enumerate(test_path):
        img_names = open(path, 'r').readlines()
        for img_name in img_names:
            img_name = img_name.strip()
            xml_path = anno_path[i] + '/' + img_name + '.xml'
            objects = parse_xml(xml_path)
            if objects:
                objects[0] = img_path[i] + '/' + img_name + '.jpg'
                if os.path.exists(objects[0]):
                    objects.insert(0, str(test_cnt))
                    test_cnt =0
                    objects = ' '.join(objects) + '\n'
                    f.write(objects)
    f.close()


train_cnt = 0
def gen_train_txt(txt_path):
    global train_cnt
    f = open(txt_path, 'w')

    for i, path in enumerate(trainval_path):
        img_names = open(path, 'r').readlines()
        for img_name in img_names:
            img_name = img_name.strip()
            xml_path = anno_path[i] + '/' + img_name + '.xml'
            objects = parse_xml(xml_path)
            if objects:
                objects[0] = img_path[i] + '/' + img_name + '.jpg'
                if os.path.exists(objects[0]):
                    objects.insert(0, str(train_cnt))
                    train_cnt =0
                    objects = ' '.join(objects) + '\n'
                    f.write(objects)
    f.close()


gen_train_txt('train.txt')
gen_test_txt('val.txt')

