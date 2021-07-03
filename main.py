import os
import random
from PIL import Image
import hashlib
import string
import json
import concurrent.futures

set_percentage = {
    # assets
    'samurai': 2,

    # bodies
    'anatomicanis': 0,
    'android': 0
}
percentage_keys = list(set_percentage.keys())
body_types = ['normal', 'android', 'anatomicanis']
cwd = r'E:\chiichan\my drive\shibe NFT\assets\fixed_assets'
tdir = r'E:\junks'
bg_url = r'E:\chiichan\my drive\shibe NFT\assets\bg\bg.png'
img_size = (2000,2200)
assets_for_count = ['hand_F', 'hat_F', 'clothing_F', 'body_F']
full_set = [i for i in set_percentage.keys() if i not in body_types]
no_of_set = len(full_set)
dirs_list = sorted([d[0] for d in os.walk(cwd)][1:])

dirs_for_count = [s for s in dirs_list if any(xs in s for xs in assets_for_count)]

total_pets = 1
for d in dirs_for_count:
    total_pets *= len(os.listdir(d))

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

        name_split = name.split('_')

        if os.path.splitext(name)[0].split('_')[-1] in string.ascii_uppercase:
            self.set = os.path.splitext(name)[0][:-2]
            self.name = os.path.splitext(name)[0]
            if 'mouth' in name:
                self.mouth_shape = name_split[-2]
            if name_split[0] in body_types:
                self.type = name_split[0]
            else:
                self.type = 'asset'
def getpercentage(n):
    for _ in percentage_keys:
        if _ in n:
            return set_percentage[_]
    return 100

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

        while picked == False:
            picked_asset = files_list[random.randint(0, len(files_list)) - 1]
            if random.randint(1,100) <= getpercentage(picked_asset):
                picked_assets.append(picked_asset)
                picked_set.add(Asset(picked_asset).set)
                picked = True
            else:
                picked = False

    return picked_assets


def getset(lst):
    result = set()
    for i in lst:
        result.add(Asset(i).set)

    return result


def getvalidlist(num):
    valid_lists = []
    to_compare = []
    if no_of_set >= num:
        for n in full_set[:num]:
            new_list = []
            for d in dirs_list:
                files_list = sorted(os.listdir(d))
                if 'mouth' in d:
                    continue
                if 'body' in d:
                    for a in files_list:
                        if 'normal' in a:
                            new_list.append(a)
                else:
                    for f in files_list:
                        if n in f:
                            new_list.append(f)
            valid_lists.append(new_list)
            to_compare.append(getset(new_list))

    else:
        for n in full_set:
            new_list = []
            for d in dirs_list:
                files_list = sorted(os.listdir(d))
                if 'mouth' in d:
                    continue
                if 'body' in d:
                    for a in files_list:
                        if 'normal' in a:
                            new_list.append(a)
                else:
                    for f in files_list:
                        if n in f:
                            new_list.append(f)
            valid_lists.append(new_list)
            to_compare.append(getset(new_list))
        
        while len(valid_lists) < num:
            generated = pickrandom()
            generated_set = getset(generated)

            if generated_set not in to_compare:
                valid_lists.append(generated)
                to_compare.append(generated_set)

    return valid_lists, to_compare


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

        # resize to img_size
        bg1 = bg.resize(img_size)
        bg1.save(file_path)

        # add hash
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        data[f'{mouth_shape}_hash'] = sha256_hash.hexdigest()
        data[f'{mouth_shape}_img'] = file_name

    return data


def imgmergenoemo(lst, name):
    cur_body_type = getbodytype(lst)
    
    mouth_f = Asset(f'{cur_body_type}_mouth_happy_F.png').path
    mouth_b = Asset(f'{cur_body_type}_mouth_happy_B.png').path
    bg = Image.open(bg_url)
    new_list = lst[:]
    new_list.reverse()

    data = {}

    for i in new_list:
        img = Image.open(Asset(i).path)

        bg = Image.alpha_composite(bg, img)

        if 'body_F' in i:
            img_b = Image.open(mouth_b)
            bg = Image.alpha_composite(bg, img_b)
            img_f = Image.open(mouth_f)
            bg = Image.alpha_composite(bg, img_f)

        file_name = f'shiba_{str(name).zfill(6)}.png'
        file_path = os.path.join(tdir, file_name)

        # resize to img_size
        bg1 = bg.resize(img_size)
        bg1.save(file_path)

        # add hash
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        data[f'hash'] = sha256_hash.hexdigest()
        data[f'img'] = file_name

    return data


def mainapp(num):
    generated = getvalidlist(num)
    asset_set = generated[1]
    results = generated[0]

    data = {'tokens': [], 'profile': {'name': 'Token2021'}}

    def printimg(i):
        info = imgmerge(results[i], i + 1)
        return {
            'id': i + 1,
            'title': f'Sipherian #{i + 1}',
            'description:': '',
            'name': f'Sipherian #{i + 1}',
            'attributes': list(asset_set[i]),
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
        }

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        result_data = executor.map(printimg, [_ for _ in range(len(results))])

    for _ in result_data:
        data['tokens'].append(_)

    with open(os.path.join(tdir, 'data.json'), 'w') as f:
        json.dump(data, f, indent=2)


def testapp(num):
    generated = getvalidlist(num)
    asset_set = generated[1]
    results = generated[0]

    data = {'tokens': [], 'profile': {'name': 'Token2021'}}

    def printimg(i):
        info = imgmergenoemo(results[i], i + 1)
        return {
            'id': i + 1,
            'title': f'Sipherian #{i + 1}',
            'description:': '',
            'name': f'Sipherian #{i + 1}',
            'attributes': list(asset_set[i]),
            'image': info['img'],
            'imageHash': info['hash'],
        }

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        result_data = executor.map(printimg, [_ for _ in range(len(results))])

    for _ in result_data:
        data['tokens'].append(_)

    with open(os.path.join(tdir, 'data.json'), 'w') as f:
        json.dump(data, f, indent=2)


def initapp():

    user_in = 0

    while user_in == 0 or user_in > total_pets:
        user_in = int(input(f'Nhap so pet muon tao (Tong so pet co the tao: {total_pets}): '))

    type_of_generator = input(f'1 cam xuc (1)? Nhieu cam xuc (2)? ')

    while type_of_generator not in ['1', '2']:
        print('Nhap 1 hoac 2')
        type_of_generator = input(f'1 cam xuc (1)? Nhieu cam xuc (2)? ')

    if type_of_generator == '1':
        print(f'Dang generate {user_in} pet co 1 cam xuc...')
        testapp(user_in)
    else:
        print(f'Dang generate {user_in} pet co 5 cam xuc...')
        mainapp(user_in)


initapp()
