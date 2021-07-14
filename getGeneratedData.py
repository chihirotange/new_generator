import json
import os
import itertools

# with open('data.json') as read_file:

#     data = json.load(read_file)
#     tokens = data['tokens']
#     attributes = [i['attributes'] for i in tokens]

with open('generated_data.json') as mod_file:
    generated_data = json.load(mod_file)

def getGeneratedSet():
    data = []
    for i in generated_data:
        data.append(set(i))
    
    return(data)


list_to_compare = getGeneratedSet()

print ({'hand_radiohead', 'clothing_fireFighter', 'hat_brawlerBrown', 'android_red', 'eye_red'} in list_to_compare)
# =================================================
# doi_ten = {
#     'clothing_AIDogbone' : 'clothing_AIDogboneBlack',
#     'hat_AIDogbone' : 'hat_AIDogboneBlack',
#     'hand_AIDogbone' : 'hand_AIDogboneBlack',
#     'clothing_pirateCaptain' : 'clothing_pirateCaptainBlueOrange',
#     'hat_pirateCaptain' : 'hat_pirateCaptainBlueOrange',
#     'hat_brawler' : 'hat_brawlerBrown',
#     'hat_daredevil' : 'hat_daredevilRed',
#     'hand_mecha' : 'hand_mechaSword',
#     'hat_gakusei' : 'hat_gakuseiBlack',
#     'hand_plumber' : 'hand_plumberOrange',
#     'hat_brainiac' : 'hat_brainiacYellowGreen',
#     'hand_jiangshi' : 'hand_jiangshiBlue',
#     'hat_neonDJ' : 'hat_neonDJTurquoise',
#     'hat_neonPunkPistoleer' : 'hat_neonPunkPistoleerPink',
#     'hand_brainiac' : 'hand_brainiacYellow',
#     'hat_metro' : 'hat_metroPink',
#     'hat_sheriff' : 'hat_sheriffBrown',
#     'clothing_astronaut' : 'clothing_astronautWhite',
#     'hand_astronaut' : 'hand_astronautWhite',
#     'hand_astronaut' : 'hand_astronautWhite',
#     'hat_neonPunk' : 'hat_streetNeonPunkLightblue',
#     'clothing_neonPunk' : 'clothing_streetNeonPunkLightblue',
#     'hand_neonPunk' : 'hand_streetNeonPunkLightblue',
# }

# doi_ten_keys = doi_ten.keys()
# new_attributes = []
# for i in attributes:
#     if any('cityzen' in a for a in i):
#         continue
#     new_attributes.append(i)


# for h, i in enumerate(new_attributes):
#     for x, a in enumerate(i):
#         if a in doi_ten_keys:
#             new_attributes[h][x] = doi_ten[a]


# with open('generated_data.json', 'w') as outfile:
#     json.dump(new_attributes, outfile)

# =================================================

# with open('list_500.json') as no_generation:
#     fixed_data = json.load(no_generation)

# fixed_list = []

# for i in fixed_data:
#     fixed_list.append(set(i))

# for i in fixed_list