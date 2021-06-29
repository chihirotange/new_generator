import os

tdir = r'E:\chiichan\my drive\shibe NFT\assets\fixed_assets'

for root, ds, fs in os.walk(tdir):
    for f in fs:
        f_wo_ext = os.path.splitext(f)[0]
        part_to_add = root.split('_')[-1]
        os.rename(os.path.join(root,f), os.path.join(root,f'{f_wo_ext}_{part_to_add}.png'))