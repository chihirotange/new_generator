from PIL import Image
import os
import random

companions_dir = r'E:\chiichan\my drive\shibe NFT\hires_assets\companions'
bg_dir = r'E:\chiichan\my drive\shibe NFT\hires_assets\bg'
target_dir = 'E:\junks\companions'
img_size = (728,728)

effects_dir = os.path.join(bg_dir,'bg')
solid_dir = os.path.join(bg_dir,'solid')
companions_names = list(map(lambda x: os.path.splitext(x)[0], os.listdir(companions_dir)))
companions_paths = list(map(lambda x: os.path.join(companions_dir,x), os.listdir(companions_dir)))
effects_paths = list(map(lambda x: os.path.join(effects_dir,x), os.listdir(effects_dir)))
solid_paths = list(map(lambda x: os.path.join(solid_dir,x), os.listdir(solid_dir)))


for i in range(1,11):
    picked_efx = effects_paths[random.randint(0, len(effects_paths) - 1)]
    picked_solid = solid_paths[random.randint(0, len(solid_paths) - 1)]

    img_efx = Image.open(picked_efx).convert('RGBA')
    img_solid = Image.open(picked_solid).convert('RGBA')

    bg = Image.alpha_composite(img_solid, img_efx)
    bg = bg.resize(img_size)

    for cp in range(len(companions_paths)):
        img_companion = Image.open(companions_paths[cp]).convert('RGBA')
        img_final = Image.alpha_composite(bg,img_companion)

        file_name = fr'set_{i}_{companions_names[cp]}.png'
        file_path = os.path.join(target_dir,file_name)
        img_final.save(file_path)