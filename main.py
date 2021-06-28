import os
import random
from PIL import Image

cwd = r'/home/chii/Downloads/assets/fixed_assets'
dirs_list = sorted([ d[0] for d in os.walk(cwd)][1:])
tdir = r'/home/chii/junks'
body_types = ['normal', 'cyborg', 'anatomy']

for dir in dirs_list:
        if 'mouth_F' in dir:
            mouth_dir_f = dir
        elif 'mouth_B' in dir:
            mouth_dir_b = dir

mouth_img_f = sorted(os.listdir(mouth_dir_f))
mouth_img_b = sorted(os.listdir(mouth_dir_b))

class Asset:
    
    def __init__(self, name):
        files_path = []
        for root, dirs, files in os.walk(cwd):
            for f in files:
                files_path.append(os.path.join(root,f))
        for p in files_path:
            if name in p:
                self.path = p

        
        name_split = name.split('_')

        self.name = os.path.splitext(name)[0]
        if name_split[-3] == 'mouth':
            self.mouth_shape = name_split[-2]

        if name_split[0] in body_types:
            self.type = name_split[0]
        else:
            self.type = 'asset'
        self.set = os.path.splitext(name)[0][:-2]

def pickRandom():
    picked_assets = []
    picked_set = set()
    for d in dirs_list:
        if 'mouth' in d:
            continue
        picked = False
        files_list = os.listdir(d)

        for f in files_list:
            if Asset(f).set in picked_set:
                picked_asset = f
                picked_assets.append(picked_asset)
                picked = True
            
        if picked == False:
            picked_asset = files_list[random.randint(0, len(files_list)) - 1]
            picked_assets.append(picked_asset)
            picked_set.add(Asset(picked_asset).set)

    return picked_assets

def getValidList(num):
    valid_lists = []
    while len(valid_lists) < num:
        list_generated = pickRandom()
        if list_generated not in valid_lists:
            valid_lists.append(list_generated)

    return valid_lists

result = getValidList(4)

def getBodyType(lst):
    for l in lst:
        if Asset(l).type in body_types:
            return Asset(l).type

def imgMerge(lst,name):
    cur_body_type = getBodyType(lst)

    cr_mouth_f = []
    cr_mouth_b = []

    for img in mouth_img_f:
        if cur_body_type in img:
            cr_mouth_f.append(img)

    for img in mouth_img_b:
        if cur_body_type in img:
            cr_mouth_b.append(img)

    bg = Image.open(r'/home/chii/Downloads/assets/bg/bg.png')
    new_list = reversed(lst)

    for m in range(len(cr_mouth_f)):
        for i in new_list:
            img = Image.open(Asset(i).path)

            bg = Image.alpha_composite(bg, img)

            if 'body_F' in i:
                img_b = Image.open(Asset(cr_mouth_b[m]).path)
                print(Asset(cr_mouth_b[m]).path)
                bg = Image.alpha_composite(bg, img_b)
                img_f = Image.open(Asset(cr_mouth_f[m]).path)
                print(Asset(cr_mouth_f[m]).path)
                bg = Image.alpha_composite(bg, img_f)

        file_name = f'shiba_{str(name).zfill(6)}_{Asset(cr_mouth_f[m]).mouth_shape}.png'
        bg.save(os.path.join(tdir,file_name))



for _ in range(len(result)):
    imgMerge(result[_], _ + 1)

