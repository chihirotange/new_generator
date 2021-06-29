import os
import random
from PIL import Image
import hashlib
import string
import json

no_of_set = 9
cwd = r'E:\chiichan\backups\assets\fixed_assets'
tdir = r'E:\junks'
bg_url = r'E:\chiichan\backups\assets\bg\bg.png'
body_types = ['normal', 'cyborg', 'anatomy']

dirs_list = sorted([d[0] for d in os.walk(cwd)][1:])

for d in dirs_list:
    if 'mouth_F' in d:
        mouth_dir_f = d
    elif 'mouth_B' in d:
        mouth_dir_b = d

mouth_img_f = sorted(os.listdir(mouth_dir_f))
mouth_img_b = sorted(os.listdir(mouth_dir_b))


class Asset:
    def __init__(self, name):
        files_path = []
        for root, dirs, files in os.walk(cwd):
            for f in files:
                files_path.append(os.path.join(root, f))
        for p in files_path:
            if name in p:
                self.path = p
        self.set = os.path.splitext(name)[0][:-2]

        name_split = name.split('_')

        if os.path.splitext(name)[0].split('_')[-1] in string.ascii_uppercase:
            self.name = os.path.splitext(name)[0]
            if name_split[-3] == 'mouth':
                self.mouth_shape = name_split[-2]

            if name_split[0] in body_types:
                self.type = name_split[0]
            else:
                self.type = 'asset'


def pickrandom():
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

        if not picked:
            picked_asset = files_list[random.randint(0, len(files_list)) - 1]
            picked_assets.append(picked_asset)
            picked_set.add(Asset(picked_asset).set)

    return picked_assets


def getvalidlist(num):
    valid_lists = []
    while len(valid_lists) < num:

        for _ in range(no_of_set):
            set_list = []
            for d in dirs_list:
                if 'mouth' in d:
                    continue
                assets_list = os.listdir(d)
                if 'body' in d:
                    for a in assets_list:
                        if 'normal' in a:
                            set_list.append(a)
                else:
                    set_list.append(assets_list[_])
            valid_lists.append(set_list)

        list_generated = pickrandom()
        if list_generated not in valid_lists:
            valid_lists.append(list_generated)

    return valid_lists


def getbodytype(lst):
    for i in lst:
        if Asset(i).type in body_types:
            return Asset(i).type


def imgmerge(lst, name):
    cur_body_type = getbodytype(lst)

    cr_mouth_f = []
    cr_mouth_b = []

    for img in mouth_img_f:
        if cur_body_type in img:
            cr_mouth_f.append(img)
    for img in mouth_img_b:
        if cur_body_type in img:
            cr_mouth_b.append(img)

    bg = Image.open(bg_url)
    new_list = lst[:]
    new_list.reverse()

    data = {}
    for m in range(len(cr_mouth_f)):
        for i in new_list:
            img = Image.open(Asset(i).path)

            bg = Image.alpha_composite(bg, img)

            if 'body_F' in i:
                img_b = Image.open(Asset(cr_mouth_b[m]).path)
                bg = Image.alpha_composite(bg, img_b)
                img_f = Image.open(Asset(cr_mouth_f[m]).path)
                bg = Image.alpha_composite(bg, img_f)

        mouth_shape = Asset(cr_mouth_f[m]).mouth_shape
        file_name = f'shiba_{str(name).zfill(6)}_{mouth_shape}.png'
        file_path = os.path.join(tdir, file_name)
        bg.save(file_path)

        # add hash
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        data[f'{mouth_shape}_hash'] = sha256_hash.hexdigest()
        data[f'{mouth_shape}_img'] = file_name

    return data


def mainapp(num):
    num_of_pet = int(num)
    asset_set = []
    results = getvalidlist(num_of_pet)

    for i in results:
        i_set = set()
        for e in i:
            i_set.add(Asset(e).set)
        asset_set.append(i_set)

    data = {'tokens': [], 'profile': {'name': 'Token2021'}}

    for _ in range(int(num_of_pet)):
        info = imgmerge(results[_], _ + 1)
        data['tokens'].append({
            'id': _ + 1,
            'title': f'Sipherian #{_ + 1}',
            'description:': '',
            'name': f'Sipherian #{_ + 1}',
            'attributes': list(asset_set[_]),
            'image': info['happy_img'],
            'imageHash': info['happy_hash'],
            'emotions': {
                "HAPPY": {
                    'image': info['happy_img'],
                    'imageHash': info['happy_hash']
                },
                "SAD": {
                    'image': info['sad_img'],
                    'imageHash': info['sad_hash']
                },
                "NERVOUS": {
                    'image': info['nervous_img'],
                    'imageHash': info['nervous_hash']
                },
                "ANGRY": {
                    'image': info['angry_img'],
                    'imageHash': info['angry_hash']
                },
                "WORRIED": {
                    'image': info['worried_img'],
                    'imageHash': info['worried_hash']
                }
            }
        })

    with open(os.path.join(tdir, 'data.json'), 'w') as f:
        json.dump(data, f, indent=2)


mainapp(3)
