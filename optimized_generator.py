import random
import os
from PIL import Image
import assets_data
import concurrent.futures

# pretty print saves the day!
import pprint
pp = pprint.PrettyPrinter()


# lay folder theo dung hierachy de print (khai bao init)
as_dir = r'D:\Chii chan drive\shibe NFT\hires_assets\fixed_assets'
t_dir = r'D:\junks'
bg_dir = r'D:\Chii chan drive\shibe NFT\hires_assets\bg'
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


# in shiba (dna,bg, name)
def shiba_printer(dna,bg,name):
    
    # ugly codee===========================================================
    lowres = False
    one_emo = True

    # lay path eye dung theo race va mau mat
    cr_eyes = [i for i in eye_paths if f"{dna['race']}_{dna['eye']}" in i]

    # lay path tu shiba dna va bg
    sb_bg_paths = get_paths(bg,bg_paths)
    sb_paths = list(reversed(get_paths(dna['dna'],as_paths)))
    
    # lay bg tu efx va solid
    efx = Image.open(sb_bg_paths[0]).convert('RGBA')
    solid = Image.open(sb_bg_paths[1]).convert('RGBA')
    bg = Image.alpha_composite(solid,efx)

    # in them emotion mask
    if 'mask' in dna.keys():
        sb_paths_w_mask = sb_paths
        sb_paths = [i for i in sb_paths if dna['mask'] not in i]
        bg_mask = bg

        # tim cach rut gon code nay
        for e in cr_eyes:
            if 'default' in e:
                default_eye = e

        for _ in sb_paths_w_mask:
            img = Image.open(_)
            bg_mask = Image.alpha_composite(bg_mask, img)
            if all(check in os.path.basename(_) for check in ['clothing','M']):
                e_img = Image.open(default_eye)
                bg_mask = Image.alpha_composite(bg_mask, e_img)
        file_name = os.path.join(t_dir,f'shiba_{name}_mask.jpg')

        if lowres == True:
            bg_mask.resize((500,564)).convert('RGB').save(file_name, optimize = True, quality = 60)
        elif lowres == False:
            bg_mask.save(os.path.join(t_dir,f'shiba_{name}_mask.png')) 

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
        file_name = os.path.join(t_dir,f'shiba_{name}_{emo_name}.jpg')
        if lowres == True:
            sb_bg.resize((500,564)).convert('RGB').save(file_name, optimize = True, quality = 60)
        else:
            sb_bg.save(os.path.join(t_dir,f'shiba_{name}_{emo_name}.png'))
        if one_emo == True:
            break

    print(f'in xong con {name}')
  

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

    generated_shibas = []
    generated_bgs = []
    ids = [n for n in range(1, shiba_num+1)]

    # tien hanh generate unique random shiba + background
    while len(generated_shibas) < shiba_num:
        generated_bgs.append(random_bg())
        shiba = shiba_dna()
        dna = shiba['dna']
        race = shiba['race']
        ratio = race_ratios[race]
        if not is_duplicated(dna,generated_dnas) and random.uniform(0.0,100.0) < ratio:
            generated_shibas.append(shiba)
            generated_dnas.append(dna)
            races_counter[race] += 1
            print(len(generated_shibas))
    print(races_counter)
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        executor.map(shiba_printer, generated_shibas,generated_bgs,ids)


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

shiba = ['hat_brainiacPurple','hand_brainiac','clothing_brainiac','eye_brown', 'normal_brown']

shiba_printer(shiba_dna(shiba),random_bg(),'brainiacPurple')