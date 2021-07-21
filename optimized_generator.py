import random
import os
from PIL import Image
import assets_data
import concurrent.futures
import hashlib
import json

# pretty print saves the day!
import pprint
pp = pprint.PrettyPrinter()


# lay folder theo dung hierachy de print (khai bao init)
as_dir = r'E:\chiichan\my drive\shibe NFT\hires_assets\fixed_assets'
t_dir = r'E:\junks'
bg_dir = r'E:\chiichan\my drive\shibe NFT\hires_assets\bg'
not_alien = ['normal','anatomicanis', 'android']

# tim cach deal with dong data nay hay hon :(
as_data = assets_data.as_data
as_variations = assets_data.as_variations
bg_data = assets_data.bg_data
masks_list = assets_data.masks_list
race_ratios = assets_data.race_ratios

# lay thong tin path tu cwd
efx_dir = os.path.join(bg_dir,'bg')
solid_dir = os.path.join(bg_dir,'solid')
as_paths = [os.path.join(root,f) for root,dirs,files in os.walk(as_dir) for f in files if 'eye' not in f]
bg_paths = [os.path.join(root,f) for root,dirs,files in os.walk(bg_dir) for f in files]
eye_paths = [os.path.join(root,f) for root,dirs,files in os.walk(as_dir) for f in files if 'eye' in f]

# generate random shiba
def shiba_dna(lst = 'random'):
    if lst == 'random':
        data = {}
        full_dna = set()
        for a in as_data.keys():
            as_part = as_data[a]
            asset = random.choice(as_part)
            if asset in masks_list:
                if asset in as_variations.keys():
                    random_variation = random.choice(as_variations[asset])
                    picked = asset + random_variation
                else:
                    picked = asset
                data['mask'] = picked
            elif asset in as_variations.keys():
                random_variation = random.choice(as_variations[asset])
                picked = asset + random_variation
            elif asset in not_alien:
                random_variation = random.choice(as_variations['body_colors'])
                picked = asset + random_variation
                data['race'] = asset
            else:
                picked = asset
                if 'eye' in asset:
                    data['eye'] = asset
                elif 'alien' in asset:
                    data['race'] = 'alien'
            full_dna.add(picked)

        data['dna'] = full_dna
        return data
    else:
        data = {'dna' : set(lst)}
        for l in lst:
            if 'eye' in l:
                data['eye'] = l
            elif 'alien' in l:
                data['race'] = 'alien'
            elif any(r in l for r in not_alien):
                # coi viet cho code nay cho bot thu cong va ngu hoc duoc ko
                data['race'] = l.split('_')[0]
            elif any(m in l for m in masks_list):
                data['mask'] = l
        return data


# kiem tra xem shiba vua tao co bi trung voi list da generate hay ko
def is_duplicated(sb,lst):
    if sb in lst:
        print('Duplicated!')
        return True
    else:
        return False


# tao bg random
def random_bg():
    efx = random.choice(bg_data['bg'])
    solid = random.choice(bg_data['solid'])
    return [efx,solid]


# lay list file tu folder
def get_paths(lst,d_path):
    paths = [i for i in d_path if any(a in i for a in lst)]
    return paths


# tao hash
def hash_generation(f_path):
    sha256_hash = hashlib.sha256()
    with open(f_path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# in shiba (dna,bg, name)
def shiba_printer(dna,bg,name):
   
    if isinstance(name,int):
        name = str(name).zfill(6)

    # khai bao dict cho hash
    shiba_data = {}
    
    # ugly codee===========================================================
    lowres = True
    one_emo = True

    # lay path eye dung theo race va mau mat
    cr_eyes = [i for i in eye_paths if f"{dna['race']}_{dna['eye']}" in i]

    # lay path tu shiba dna va bg
    sb_bg_paths = get_paths(bg,bg_paths)
    sb_paths = list(reversed(get_paths(dna['dna'],as_paths)))
    
    # lay bg tu efx va solid
    if bg == 'transparent':
        bg = Image.open(os.path.join(efx_dir,'bg_none.png'))

    else:
        efx = Image.open(sb_bg_paths[0]).convert('RGBA')
        solid = Image.open(sb_bg_paths[1]).convert('RGBA')
        bg = Image.alpha_composite(solid,efx)

    # in them emotion mask
    if 'mask' in dna.keys():
        sb_paths_w_mask = sb_paths
        sb_paths = [i for i in sb_paths if dna['mask'] not in i]
        bg_mask = bg

        #lay path default eye (tim cach rut gon code nay)
        for e in cr_eyes:
            if 'default' in e:
                default_eye = e


        for _ in sb_paths_w_mask:
            img = Image.open(_)
            bg_mask = Image.alpha_composite(bg_mask, img)
            if all(check in os.path.basename(_) for check in ['clothing','M']):
                e_img = Image.open(default_eye)
                bg_mask = Image.alpha_composite(bg_mask, e_img)
        file_name = f'shiba_{name}_mask'


        # save file duoi dang highres hay lowres
        if lowres == True:
            file_path = os.path.join(t_dir,file_name + '.jpg')
            bg_mask.resize((500,564)).convert('RGB').save(file_path, optimize = True, quality = 60)
        else:
            file_path = os.path.join(t_dir,file_name + '.png')
            bg_mask.save(os.path.join(t_dir,file_path))

        shiba_data['mask_img'] = file_name
        shiba_data['mask_hash'] = hash_generation(file_path)
    else:
        shiba_data['mask_img'] = None
        shiba_data['mask_hash'] = None
    # in emotions co ban
    while len(cr_eyes) > 0:
        e = random.choice(cr_eyes)
        cr_eyes.remove(e)
        sb_bg = bg
        for _ in sb_paths:
            img = Image.open(_)
            sb_bg = Image.alpha_composite(sb_bg, img)
            if all(check in os.path.basename(_) for check in ['clothing','M']):
                e_img = Image.open(e)
                sb_bg = Image.alpha_composite(sb_bg, e_img)
        emo_name = os.path.splitext(os.path.basename(e))[0].split('_')[-2]
        file_name = f'shiba_{name}_{emo_name}'

        # save duoi dang highres hay alow res
        if lowres == True:
            file_path = os.path.join(t_dir,file_name + '.jpg')
            sb_bg.resize((500,564)).convert('RGB').save(file_path, optimize = True, quality = 60)
        else:
            file_path = os.path.join(t_dir,file_name + '.png')
            sb_bg.save(os.path.join(t_dir,file_path))

        shiba_data[f'{emo_name}_img'] = file_name
        shiba_data[f'{emo_name}_hash'] = hash_generation(file_path)

        if one_emo == True:
            break

    print(f'in xong con {name}')
    return shiba_data
  

def mainapp():

    shiba_num = int(input('Nhap so pet can tao: '))

    races_counter = {
        'anatomicanis': 0,
        'android': 0,
        'normal': 0,
        'alien': 0
    }


    # import data dna json vao cho nay
    generated_dnas = []


    # tao data dna
    saved_dnas = {'dnas' : []}

    with open('saved_dnas.json') as f:
        loaded_dnas = json.load(f)
        if loaded_dnas:
            for dna in loaded_dnas['dnas']:
                saved_dnas['dnas'].append(dna)
                generated_dnas.append(set(dna['dna']))

    generated_shibas = []
    generated_bgs = []
    ids = [n for n in range(1, shiba_num+1)]


    # tien hanh generate unique random shiba + background
    while len(generated_shibas) < shiba_num:
        generated_bg = random_bg()
        generated_bgs.append(generated_bg)
        shiba = shiba_dna()
        dna = shiba['dna']
        race = shiba['race']
        ratio = race_ratios[race]
        if not is_duplicated(dna,generated_dnas) and random.uniform(0.0,100.0) < ratio:
            generated_shibas.append(shiba)
            generated_dnas.append(dna) #tiep tuc them dna da generate vao dna pool
            races_counter[race] += 1

            dna_info = {
                'dna' : list(dna),
                'bg' : generated_bg
            }
            saved_dnas['dnas'].append(dna_info)

            print(len(generated_shibas))
    with open('saved_dnas.json', 'w') as f:
        json.dump(saved_dnas,f,indent = 1)

    print(generated_dnas, len(generated_dnas))


    # in shiba tu dna
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        results = list(executor.map(shiba_printer, generated_shibas,generated_bgs,ids))
    

    # generate datas
    final_datas = {'tokens': [], 'profile': {'name': 'Token2021'}}

    for i,id in enumerate(ids):
        indi_data = {
            'id': id,
            'title': f'Sipherian #{id}',
            'description:': '',
            'name': f'Sipherian #{id}',
            'attributes': list(generated_shibas[i]['dna']),
            'image': results[i].get('default_img', None),
            'imageHash': results[i].get('default_hash', None),
            'emotions': {
                "DEFAULT": {
                    'image': results[i].get('default_img', None),
                    'imageHash': results[i].get('default_hash', None)
                },
                "SAD": {
                    'image': results[i].get('sad_img', None),
                    'imageHash': results[i].get('sad_hash', None)
                },
                "NERVOUS": {
                    'image': results[i].get('nervous_img', None),
                    'imageHash': results[i].get('nervous_hash', None)
                },
                "ANGRY": {
                    'image': results[i].get('angry_img', None),
                    'imageHash': results[i].get('angry_hash', None)
                },
                "EVIL": {
                    'image': results[i].get('evil_img', None),
                    'imageHash': results[i].get('evil_hash', None)
                },
                "MASK": {
                    'image': results[i].get('mask_img', None),
                    'imageHash': results[i].get('mask_hash', None)
                }
            },
            'background': generated_bgs[i]
        }

        final_datas['tokens'].append(indi_data)

    with open(os.path.join(t_dir, 'data.json'), 'w') as f:
        json.dump(final_datas, f, indent=2)

    print(races_counter)



# mainapp()


# IN ORIGINALS
# as_set = assets_data.as_sets


# hats = ['hat_' + i for i in as_set]
# clothings = ['clothing_' + i for i in as_set]
# hands = ['hand_' + i for i in as_set]

# original_pets = []
# generated_bgs = []
# generated_names = []
# for i in range(len(as_set)):
#     generated_name = as_set[i]
#     pet_dna = [hats[i],clothings[i],hands[i], 'normal_brown', 'eye_brown']
#     pet = shiba_dna(pet_dna)
#     original_pets.append(pet)
#     generated_bgs.append(random_bg())
#     generated_names.append(generated_name)
#     print(i+1)

# with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
#         executor.map(shiba_printer, original_pets,generated_bgs,generated_names)


# thong so in rieng tung con
son_thung = ['hat_sipherionTrainer','hand_graffitiArtist','clothing_drip','eye_brown', 'normal_brown']

shiba_printer(shiba_dna(son_thung),random_bg(),'caSiSonThung')

# print(hash_generation(f'E:\junks\shiba_1_angry.jpg'))

# for i in range(10):
#     shiba_printer(shiba_dna(),'transparent', f'shiba_{str(i + 1).zfill(3)}')
