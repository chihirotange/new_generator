import os
import random
from PIL import Image
import hashlib
import json
import concurrent.futures
import itertools

body_types = ['normal', 'android', 'anatomicanis', 'alien']
cwd = r'D:\Chii chan drive\shibe NFT\hires_assets\fixed_assets'
tdir = r'D:\junks'
bg_url = r'D:\Chii chan drive\shibe NFT\hires_assets\bg'
bg_f = os.path.join(bg_url, 'bg')
bg_b = os.path.join(bg_url, 'solid')

bg_f_files = os.listdir(bg_f)
bg_b_files = os.listdir(bg_b)

# img_size = (400,451)
img_size = (500,564)
# img_size = (1000,1129)
assets_for_count = ['hand_F', 'hat_F', 'clothing_F', 'body_F']
dirs_list = sorted([d[0] for d in os.walk(cwd)][1:])
full_files = [f for root,dirs,files in os.walk(cwd) for f in files if 'eye' not in f]

full_files_list = []
masks_list = ('hat_neonKitty', 'hat_mecha', 'hat_cloneTrooper', 'hat_radiohead', 'hat_metro')

for d in dirs_list:
    if 'eye' in d:
        continue
    full_files_list.append(os.listdir(d))

dirs_for_count = [s for s in dirs_list if any(xs in s for xs in assets_for_count)]

total_pets = 1
for d in dirs_for_count:
    total_pets *= len(os.listdir(d))

for d in dirs_list:
    if 'eye' in d:
        eye_dir = d

eye_img = sorted(os.listdir(eye_dir))

class Asset:
    def __init__(self, name):

        if 'bg_' in name or 'solid_' in name:
            files_path = []
            for root, dirs, files in os.walk(bg_url):
                for f in files:
                    files_path.append(os.path.join(root,f))
            for p in files_path:
                if name in p:
                    self.path = p
        else:

            files_path = []
            for root, dirs, files in os.walk(cwd):
                for f in files:
                    files_path.append(os.path.join(root, f))
            for p in files_path:
                if name in p:
                    self.path = p

            name_split = name.split('_')
            name_wo_ext = os.path.splitext(name)[0]
            name_split_wo_ext = name_wo_ext.split('_')

            # if os.path.splitext(name)[0].split('_')[-1] in string.ascii_uppercase:
            self.set = os.path.splitext(name)[0][:-2]
            self.name = os.path.splitext(name)[0]
            if 'clothing' in name_split:
                self.type = 'clothing'
                self.pos = f'clothing_{name_split_wo_ext[-1]}'
            elif len(name_split) == 5 and name_split[1] == 'eye':
                self.type = 'eye'
                self.mouth_shape = name_split[-2]
            elif name_split[0] in body_types and len(name_split) == 3:
                self.type = name_split[0]
            else:
                self.type = 'asset'
                self.setName = name_split[1]

def getvalidlist(num):
    eye_list = ['eye_red', 'eye_amber', 'eye_grey', 'eye_heterochromia', 'eye_blue', 'eye_green', 'eye_purple', 'eye_brown']
    converted_list = []
    all_sets = {}
    for d in dirs_for_count:
        set_name = os.path.basename(d).split('_')[1]
        all_sets[set_name] = [Asset(i).set for i in os.listdir(d)]

    for key in all_sets:
        converted_list.append(all_sets[key])

    converted_list.append(eye_list)
    total = list(itertools.product(*converted_list))
    picked = []
    hahaha = []

    while len(picked) < num:
        randomNum = random.randint(0, len(total) - 1)
        randomized = total[randomNum]
        del total[randomNum]
        picked.append(randomized)
    eye_colors = []
    for i in picked:
        for j in i:
            if 'eye' in j:
                eye_colors.append(j)

    def get_file_from_set(st):

        picked_files = []
        # for i in full_files_list:
        #     for f in i:
        #         if 'eye' in f:
        #             break
        #         if Asset(f).set in st:
        #             picked_files.append(f)
        #             break
        # print(picked_files)
        for path in full_files:
            if any(item in path for item in st):
                picked_files.append(path)
        return picked_files
    
    for i in range(len(picked)):
        print(i + 1)
        hahaha.append(get_file_from_set(picked[i]))

    return hahaha, picked, eye_colors


def getbodytype(lst):
    for i in lst:
        if Asset(i).type in body_types:
            return Asset(i).type


def imgmerge(lst, name, eye):

    cur_body_type = getbodytype(lst)
    mask_name = None
    cr_eye = []

    for img in eye_img:
        if cur_body_type in img and eye in img:
            cr_eye.append(img)
    
    for e in cr_eye:
        if 'default' in e:
            default_eye = e

    file_1 = bg_f_files[random.randint(0,len(bg_f_files) - 1)]
    file_2 = bg_b_files[random.randint(0,len(bg_b_files) - 1)]
    
    img_1 = Image.open(Asset(file_1).path).convert('RGBA')
    img_2 = Image.open(Asset(file_2).path).convert('RGBA')
    bg = Image.alpha_composite(img_2, img_1)

    new_list = []
    for i in lst:
        if Asset(i).set in masks_list:
            mask_name = i
            continue
        new_list.append(i)
    new_list.reverse()

    data = {}
    for m in range(len(cr_eye)):
        bg_each = bg
        for k, i in enumerate(new_list):
            # in lan luot
            img = Image.open(Asset(i).path).convert('RGBA')
            bg_each = Image.alpha_composite(bg_each, img)

            # in mat
            if Asset(i).type == 'clothing':
                if Asset(i).pos == 'clothing_M':
                    img_f = Image.open(Asset(cr_eye[m]).path)
                    bg_each = Image.alpha_composite(bg_each, img_f)

        mouth_shape = Asset(cr_eye[m]).mouth_shape
        file_name = f'shiba_{str(name).zfill(6)}_{mouth_shape}.jpg'
        file_path = os.path.join(tdir, file_name)

        # resize to img_size
        bg_each.resize(img_size).convert('RGB').save(file_path,optimize=True, quality = 50)

        # add hash
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        data[f'{mouth_shape}_hash'] = sha256_hash.hexdigest()
        data[f'{mouth_shape}_img'] = file_name
        data[f'mask_hash'] = None
        data[f'mask_img'] = None

    list_w_mask = lst[:]
    list_w_mask.reverse()
    if mask_name != None:
        for i in list_w_mask:
            img = Image.open(Asset(i).path)
            bg = Image.alpha_composite(bg, img)
        
        file_name = f'shiba_{str(name).zfill(6)}_mask.jpg'
        file_path = os.path.join(tdir, file_name)

        bg.resize(img_size).convert('RGB').save(file_path,optimize=True, quality = 50)

        data[f'mask_hash'] = sha256_hash.hexdigest()
        data[f'mask_img'] = file_name

    data[f'background'] = [os.path.splitext(file_1)[0], os.path.splitext(file_2)[0]]

    return data


# def imgmergenoemo(lst, name):
#     cur_body_type = getbodytype(lst)
#     mouth_f = Asset(f'{cur_body_type}_mouth_default_F.png').path
#     mouth_b = Asset(f'{cur_body_type}_mouth_default_B.png').path
#     bg = Image.open(bg_url)
#     new_list = lst[:]
#     new_list.reverse()

#     data = {}

#     for i in new_list:
#         img = Image.open(Asset(i).path)

#         bg = Image.alpha_composite(bg, img)

#         if cur_body_type in i:
#             img_b = Image.open(mouth_b)
#             bg = Image.alpha_composite(bg, img_b)
#             img_f = Image.open(mouth_f)
#             bg = Image.alpha_composite(bg, img_f)

#         file_name = f'shiba_{str(name).zfill(6)}.png'
#         file_path = os.path.join(tdir, file_name)

#         # resize to img_size
#         bg1 = bg.resize(img_size)
#         bg1.save(file_path)

#         # add hash
#         sha256_hash = hashlib.sha256()
#         with open(file_path, "rb") as f:
#             # Read and update hash string value in blocks of 4K
#             for byte_block in iter(lambda: f.read(4096), b""):
#                 sha256_hash.update(byte_block)

#         data[f'hash'] = sha256_hash.hexdigest()
#         data[f'img'] = file_name

#     return data


def mainapp(num):
    generated = getvalidlist(num)
    asset_set = generated[1]
    results = generated[0]
    eyes_list = generated[2]

    data = {'tokens': [], 'profile': {'name': 'Token2021'}}

    def printimg(i):
        info = imgmerge(results[i], i + 1, eyes_list[i])
        return {
            'id': i + 1,
            'title': f'Sipherian #{i + 1}',
            'description:': '',
            'name': f'Sipherian #{i + 1}',
            'attributes': list(asset_set[i]),
            'image': info['default_img'],
            'imageHash': info['default_hash'],
            'emotions': {
                "DEFAULT": {
                    'image': info['default_img'],
                    'imageHash': info['default_hash']
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
                "EVIL": {
                    'image': info['evil_img'],
                    'imageHash': info['evil_hash']
                },
                "MASK": {
                    'image': info['mask_img'],
                    'imageHash': info['mask_hash']
                }
            },
            'background': info['background']
        }

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        result_data = executor.map(printimg, [_ for _ in range(len(results))])

    for _ in result_data:
        data['tokens'].append(_)

    with open(os.path.join(tdir, 'data.json'), 'w') as f:
        json.dump(data, f, indent=2)


# def testapp(num):
#     generated = getvalidlist(num)
#     asset_set = generated[1]
#     results = generated[0]
#
#     data = {'tokens': [], 'profile': {'name': 'Token2021'}}
#
#     def printimg(i):
#         info = imgmergenoemo(results[i], i + 1)
#         return {
#             'id': i + 1,
#             'title': f'Sipherian #{i + 1}',
#             'description:': '',
#             'name': f'Sipherian #{i + 1}',
#             'attributes': list(asset_set[i]),
#             'image': info['img'],
#             'imageHash': info['hash'],
#         }
#
#     with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
#         result_data = executor.map(printimg, [_ for _ in range(len(results))])
#
#     for _ in result_data:
#         data['tokens'].append(_)
#
#     with open(os.path.join(tdir, 'data.json'), 'w') as f:
#         json.dump(data, f, indent=2)


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
        # testapp(user_in)
    else:
        print(f'Dang generate {user_in} pet co 5 cam xuc...')
        mainapp(user_in)


initapp()
