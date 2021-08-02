# data generation
as_types = ['clothing', 'hand', 'hat']

# ti le rot
raw_ratios = {
    'infected': 0,
    'cyborg': 100,
    'cosmic': 0,
}

# ti le canis con lai just kindergarten math
raw_ratios['canis'] = 100 - raw_ratios['infected'] - raw_ratios['cyborg'] - raw_ratios['cosmic']

as_sets = [


    'noirCapone',
    'airForceOne',
    'madJaxWarrior',
    'daredevil',
    'drippingCool',
    'graffie',
    'indigenous',
    'nekoSpace',
    'captainRed',
    'radioJack',
    'papaSanta',
    'jiangshi',
    'wastelander',
    'neonDJ',
    'oniChan',
    'dragonDancer',
    'punkPink',
    'miniMe',
    'bigTime',
    'catstronaut',
    'nuMechWarrior',
    'bombardier',
    'spaceTrooper',
    'gakusei',
    'cyberFixer',
    'guardianOfOcean',
    'metroWarrior',
    'fixer',
    'patisseire',
    'surgicalPrecision',
    'metro2021',
    'pharaoh',
    'turnDownTheHeat',
    'cowboy',
    'dogInACat',
    'wanderingSamurai',
    'cosmicExplorer',
    'shikigami',
    'mayanNomad',
    'sunRaver',
    'yinYangMaster'
]

# tinh toan ratio
race_ratios = {
    'canis': 100 if raw_ratios['canis'] != 0 else 0,
    'infected' : raw_ratios['infected'] if raw_ratios['canis'] == 0 else int(raw_ratios['infected']/raw_ratios['canis']*100),
    'cyborg' : raw_ratios['cyborg'] if raw_ratios['canis'] == 0 else int(raw_ratios['cyborg']/raw_ratios['canis']*100),
    'cosmic' : raw_ratios['cosmic'] if raw_ratios['canis'] == 0 else int(raw_ratios['cosmic']/raw_ratios['canis']*100)
}

# cac thong tin bg
bg_data = {

    'bg' : [
        'bg_airForceOne', 
        'bg_surgicalPrecision', 
        'bg_madJaxWarrior', 
        'bg_catstronaut', 
        'bg_daredevil', 
        'bg_drip', 
        'bg_fireFighter', 
        'bg_gakusei', 
        'bg_graffitiArtist', 
        'bg_metro', 
        'bg_miniMe', 
        'bg_indigenous', 
        'bg_nekoSpace', 
        'bg_neonDJ', 
        'bg_punkPink', 
        'bg_none', 
        'bg_oniChan', 
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
        'solid_blue', 
        'solid_green', 
        'solid_pink', 
        'solid_red', 
        'solid_yellow', 
        ]
}

# cac emotions
emo = ['happy', 'default', 'sad', 'nervous', 'evil']

# non-cosmic
non_cosmic = ['infected','canis','cyborg']

# cac mask thao dc
masks_list = ('hat_dogInACat', 'hat_nuMechWarrior', 'hat_spaceTrooper', 'hat_radioJack', 'hat_metro2021')

# variations cua cac asset thiet lap o day (khi them asset moi can bo sung)
as_variations = {
    # races
    'body_colors': ['_red', '_brown', '_black', '_blue'],
}

# data de tao cac unique combinations
as_data = {
    'all_hats' : ['hat_' + i for i in as_sets],
    'all_hands' : ['hand_' + i for i in as_sets],
    'all_clothings' : ['clothing_' + i for i in as_sets],
    'all_races': ['cyborg','infected','canis','cosmic']
}