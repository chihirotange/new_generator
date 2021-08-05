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
as_variations = assets_data.as_variations
bg_data = assets_data.bg_data
race_types = assets_data.as_data['all_races']
non_cosmic = assets_data.non_cosmic
as_num = assets_data.as_num
total_pets = assets_data.total_pets

# lay thong tin path tu cwd
efx_dir = os.path.join(bg_dir,'bg')
solid_dir = os.path.join(bg_dir,'solid')
as_paths = [os.path.join(root,f) for root,dirs,files in os.walk(as_dir) for f in files if 'eye' not in f]
bg_paths = [os.path.join(root,f) for root,dirs,files in os.walk(bg_dir) for f in files]
eye_paths = [os.path.join(root,f) for root,dirs,files in os.walk(as_dir) for f in files if 'eye' in f]

# so luong tung race
race_num = assets_data.race_num
print(race_num)

# tao list hands, clothings, hats
hats_list = []
clothings_list = []
hands_list = []

for i in as_num.keys():
    set_num = as_num[i]
    if set_num != 0:
        for n in range(set_num):
            hands_list.append('hand_' + i)
            hats_list.append('hat_' + i)
            clothings_list.append('clothing_' + i)

as_dict = {
    'hands': hands_list,
    'hats': hats_list,
    'clothings': clothings_list,
}

# tao list races
races_list = []
for race, n in race_num.items():
    if n != 0:
        for i in range(n):
            races_list.append(race)
            
# generate random shiba
def shiba_dna(lst = 'random'):
    if lst == 'random':
        data = {}
        full_dna = []
        picked_race = races_list.pop(random.randint(0, len(races_list) - 1))
        data['race'] = picked_race
        if picked_race in non_cosmic:
            picked_race = picked_race + random.choice(as_variations['body_colors'])

        full_dna.append(picked_race)
        for a in as_dict.values():
            picked_part = a.pop(random.randint(0,len(a) -1))
            full_dna.append(picked_part)

        data['dna'] = full_dna
        return data


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
    one_emo = False

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

    races_counter = {
        'infected': 0,
        'cyborg': 0,
        'canis': 0,
        'cosmic': 0
    }


    generated_shibas = []
    ids = [n + 1 for n in range(total_pets)]
    generated_bg = [random_bg() for bg in range(total_pets)]

    # tien hanh generate unique random shiba + background
    while len(races_list) > 0:
        shiba = shiba_dna()
        dna = shiba['dna']
        race = shiba['race']

        generated_shibas.append(shiba)
        races_counter[race] += 1


    # in shiba tu dna
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        results = list(executor.map(shiba_printer, generated_shibas,ids,generated_bg))
    

    # generate datas
    final_datas = []

    for i,id in enumerate(ids):
        indi_data = {
            'id': id,
            'attributes': list(generated_shibas[i]['dna']),
            # 'image': results[i].get('default_img', None),
            # 'emotions': {
            #     "DEFAULT": {
            #         'image': results[i].get('default_img', None),
            #     },
            #     "SAD": {
            #         'image': results[i].get('sad_img', None),
            #     },
            #     "NERVOUS": {
            #         'image': results[i].get('nervous_img', None),
            #     },
            #     "ANGRY": {
            #         'image': results[i].get('angry_img', None),
            #     },
            #     "EVIL": {
            #         'image': results[i].get('evil_img', None),
            #     },
            #     "MASK": {
            #         'image': results[i].get('mask_img', None),
            #     }
            # }
        }

        final_datas.append(indi_data)

    with open(os.path.join(t_dir, 'data.json'), 'w') as f:
        json.dump(final_datas, f, indent=2)

    print(races_counter)

set_total = 0
for i in as_num.values():
    set_total += i

# if set_total == total_pets:
mainapp()
# else:
    # print('kiem tra lai gia tri cac set va race')
