import random
import os
from PIL import Image
import assets_data
import concurrent.futures
import json

# pretty print saves the day!
import pprint
pp = pprint.PrettyPrinter()


# lay folder theo dung hierachy de print (khai bao init)
as_dir = r'D:\Chii chan drive\shibe NFT\final\fixed_assets'
t_dir = r'D:\junks'
bg_dir = r'D:\Chii chan drive\shibe NFT\final\bg'

# tim cach deal with dong data nay hay hon :(
as_data = assets_data.as_data
as_variations = assets_data.as_variations
bg_data = assets_data.bg_data
# masks_list = assets_data.masks_list
race_ratios = assets_data.race_ratios
race_types = assets_data.as_data['all_races']
non_cosmic = assets_data.non_cosmic

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
            picked = asset
            if asset in non_cosmic:
                variations = random.choice(as_variations['body_colors'])
                picked = asset + variations
                data['race'] = asset
            elif asset == 'cosmic':
                data['race'] = asset
            # elif asset in masks_list:
                # data['mask'] = asset
            full_dna.add(picked)

        data['dna'] = full_dna
        return data
    else:
        data = {'dna' : set(lst)}
        for l in lst:
            # if any(m in l for m in masks_list):
                # data['mask'] = l
            race = l.split('_')[0]
            if race in race_types:
                data['race'] = race
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
    efx = 'bg_drip'
    solid = random.choice(bg_data['solid'])
    return [efx,solid]


# lay list file tu folder
def get_paths(lst,d_path):

    if isinstance(lst,(list,set)):
        paths = []

        for i in d_path:
            for a in lst:
                if a + '.png' == os.path.basename(i):
                    paths.append(i)
                    break
        return paths

    elif isinstance(lst, str):
        for i in d_path:
            if lst + ".png" == os.path.basename(i):
                return i


# in shiba (dna,bg, name)
def shiba_printer(dna,name,bg='transparent'):
   
    if isinstance(name,int):
        name = str(name).zfill(6)

    # khai bao dict cho hash
    shiba_data = {}
    
    # ugly codee===========================================================
    lowres = True
    one_emo = True

    # lay path eye dung theo race va mau mat
    cr_eyes = [i for i in eye_paths if f"{dna['race']}_eye" in i]

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


    #lay path default eye (tim cach rut gon code nay)
    for e in cr_eyes:
        if 'default' in e:
            default_eye = e
                
    # in them emotion mask
    sb_paths_w_mask = sb_paths
    sb_paths = [i for i in sb_paths if 'hat_' not in os.path.basename(i)]

    bg_mask = bg


    for _ in sb_paths_w_mask:
        img = Image.open(_)
        bg_mask = Image.alpha_composite(bg_mask, img)
        if 'body_F' in _:
            e_img = Image.open(default_eye)
            bg_mask = Image.alpha_composite(bg_mask, e_img)
    file_name = f'shiba_{name}_mask'


    # save file duoi dang highres hay lowres
    if lowres == True:
        file_path = os.path.join(t_dir,file_name + '.png')
        bg_mask.resize((700,790)).save(file_path, optimize = True)
    else:
        file_path = os.path.join(t_dir,file_name + '.png')
        bg_mask.save(os.path.join(t_dir,file_path))

    shiba_data['mask_img'] = file_name

    # in emotions co ban
    while len(cr_eyes) > 0:
        if default_eye in cr_eyes:
            e = default_eye
        else:
            e = random.choice(cr_eyes)
        cr_eyes.remove(e)
        sb_bg = bg
        for _ in sb_paths:
            img = Image.open(_)
            sb_bg = Image.alpha_composite(sb_bg, img)
            if 'body_F' in _:
                e_img = Image.open(e)
                sb_bg = Image.alpha_composite(sb_bg, e_img)
        emo_name = os.path.splitext(os.path.basename(e))[0].split('_')[-1]
        file_name = f'shiba_{name}_{emo_name}'

        # save duoi dang highres hay alow res
        if lowres == True:
            file_path = os.path.join(t_dir,file_name + '.png')
            sb_bg.resize((700,790)).save(file_path, optimize = True)
        else:
            file_path = os.path.join(t_dir,file_name + '.png')
            sb_bg.save(os.path.join(t_dir,file_path))

        shiba_data[f'{emo_name}_img'] = file_name

        if one_emo == True:
            break

    print(f'in xong con {name}')
    return shiba_data
  

def mainapp():

    shiba_num = int(input('Nhap so pet can tao: '))
    shiba_batch = int(input('Bat dau tu: '))

    races_counter = {
        'infected': 0,
        'cyborg': 0,
        'canis': 0,
        'cosmic': 0
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
    ids = [n for n in range(shiba_batch, shiba_num+shiba_batch)]
    generated_bg = [random_bg() for bg in range(shiba_num)]

    # tien hanh generate unique random shiba + background
    while len(generated_shibas) < shiba_num:
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
            }
            saved_dnas['dnas'].append(dna_info)

            print(len(generated_shibas))
    with open('saved_dnas.json', 'w') as f:
        json.dump(saved_dnas,f,indent = 1)

    print(generated_dnas, len(generated_dnas))


    # in shiba tu dna
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        results = list(executor.map(shiba_printer, generated_shibas,ids,generated_bg))
    

    # generate datas
    final_datas = {'tokens': [], 'profile': {'name': 'Token2021'}}

    for i,id in enumerate(ids):
        indi_data = {
            'id': id,
            'attributes': list(generated_shibas[i]['dna']),
            'image': results[i].get('default_img', None),
            'emotions': {
                "DEFAULT": {
                    'image': results[i].get('default_img', None),
                },
                "SAD": {
                    'image': results[i].get('sad_img', None),
                },
                "NERVOUS": {
                    'image': results[i].get('nervous_img', None),
                },
                "ANGRY": {
                    'image': results[i].get('angry_img', None),
                },
                "EVIL": {
                    'image': results[i].get('evil_img', None),
                },
                "MASK": {
                    'image': results[i].get('mask_img', None),
                }
            }
        }

        final_datas['tokens'].append(indi_data)

    with open(os.path.join(t_dir, 'data.json'), 'w') as f:
        json.dump(final_datas, f, indent=2)

    print(races_counter)



mainapp()

# test_shiba = ['hand_metro2021', 'infected_brown', 'hat_metro2021','clothing_metro2021']

# shiba_printer(shiba_dna(test_shiba), 'shiba_infected',['bg_drip','solid_blue'])