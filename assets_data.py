# data generation
as_types = ['clothing', 'hand', 'hat']

# ti le rot
raw_ratios = {
    'anatomicanis': 10,
    'android': 10,
    'alien': 1,
}

# ti le normal con lai just kindergarten math
raw_ratios['normal'] = 100 - raw_ratios['anatomicanis'] - raw_ratios['android'] - raw_ratios['alien']

as_sets = [
    'AIDogbone',
    'airForceOne',
    'brawler',
    'daredevil',
    'drip',
    'graffitiArtist',
    'nativeAmerican',
    'nekoSpace',
    'pirateCaptain',
    'radiohead',
    'santaClaus',
    'jiangshi',
    'wastelander',
    'neonDJ',
    'oniForHire',
    'dragonDancer',
    'neonPunkPistoleer',
    'miniMe',
    'commando',
    'catstronaut',
    'mecha',
    'bombardier',
    'cloneTrooper',
    'gakusei',
    'streetNeonPunk',
    'subnautica',
    'sipherionTrainer',
    'plumber',
    'patissier',
    'brainiac',
    'metro',
    'pharoah',
    'fireFighter',
    'sheriff',
    'neonKitty',
    'samurai',
    'astronaut',
    'shikigami',
    'maya',
    'techSupport',
    'raver',
    'omyogi'
]

# tinh toan ratio
race_ratios = {
    'normal': 100 if raw_ratios['normal'] != 0 else 0,
    'anatomicanis' : raw_ratios['anatomicanis'] if raw_ratios['normal'] == 0 else int(raw_ratios['anatomicanis']/raw_ratios['normal']*100),
    'android' : raw_ratios['android'] if raw_ratios['normal'] == 0 else int(raw_ratios['android']/raw_ratios['normal']*100),
    'alien' : raw_ratios['alien'] if raw_ratios['normal'] == 0 else int(raw_ratios['alien']/raw_ratios['normal']*100)
}

print(race_ratios)

# cac thong tin bg
bg_data = {

    'bg' : [
        'bg_airForceOne', 
        'bg_brainiac', 
        'bg_brawler', 
        'bg_catstronaut', 
        'bg_daredevil', 
        'bg_drip', 
        'bg_fireFighter', 
        'bg_gakusei', 
        'bg_graffitiArtist', 
        'bg_metro', 
        'bg_miniMe', 
        'bg_nativeAmerican', 
        'bg_nekoSpace', 
        'bg_neonDJ', 
        'bg_neonPunkPistoleer', 
        'bg_none', 
        'bg_oniForHire', 
        'bg_patissier', 
        'bg_pharoah', 
        'bg_plumber', 
        'bg_samurai', 
        'bg_santaClaus', 
        'bg_sheriff', 
        'bg_sipherionTrainer', 
        'bg_subnautica', 
        'bg_wastelander'],

    'solid' : [
        'solid_01', 
        'solid_02', 
        'solid_03', 
        'solid_04', 
        'solid_05', 
        'solid_06', 
        'solid_07', 
        'solid_08', 
        'solid_09', 
        'solid_10'
        ]
}

# cac emotions
emo = ['happy', 'default', 'sad', 'nervous', 'evil']

masks_list = ('hat_neonKitty', 'hat_mecha', 'hat_cloneTrooper', 'hat_radiohead', 'hat_metro')

# variations cua cac asset thiet lap o day (khi them asset moi can bo sung)
as_variations = {
    # races
    'body_colors': ['_black', '_brown', '_green','_grey','_lightblue','_purple', '_red'],

    # sets
    'hat_AIDogbone': ['White','Black'],
    'clothing_AIDogbone': ['White','Black'],
    'hand_AIDogbone': ['White','Black'],
    'hat_brawler': ['Brown', 'Grey', 'Gold'],
    'hat_daredevil': ['Red','Purple'],
    'hat_pirateCaptain': ['GreenRed','BlueOrange'],
    'clothing_pirateCaptain': ['GreenRed','BlueOrange'],
    'hand_jiangshi': ['Blue','Yellow','Red','Purple'],
    'hat_neonPunkPistoleer': ['Yellow','Pink','Lightblue'],
    'hand_mecha': ['Sword','LightSword'],
    'hat_gakusei': ['Black', 'Yellow'],
    'hand_plumber': ['Orange', 'Blue'],
    'hat_brainiac': ['Yellow', 'Red', 'Purple'],
    'hat_metro': ['Pink','Lightblue','Yellow'],
    'hat_sheriff': ['Brown', 'Grey'],
    'hat_astronaut': ['White', 'Red'],
    'clothing_astronaut': ['White', 'Red'],
    'hand_astronaut': ['White', 'Red'],
    'hat_streetNeonPunk': ['Yellow', 'Lightblue']
}

# data de tao cac unique combinations
as_data = {
    'all_hats' : ['hat_' + i for i in as_sets],
    'all_hands' : ['hand_' + i for i in as_sets],
    'all_clothings' : ['clothing_' + i for i in as_sets],
    'all_eyes': ['eye_amber', 'eye_blue', 'eye_brown', 'eye_green', 'eye_grey', 'eye_heterochromia', 'eye_purple', 'eye_red'],
    'all_races': ['alien','android','anatomicanis','normal']
}