# so luong tung race
total_pets = 9
race_num = {
    'infected': 0,
    'cyborg': 0,
    'cosmic': 0,
}
race_num['canis'] = total_pets - race_num['infected'] - race_num['cyborg'] - race_num['cosmic']


# so luong tung bo do
as_num = {
    'noirCapone': 100,
    'airForceOne': 100,
    'madJaxWarrior': 100,
    'daredevil': 100,
    'drippingCool': 100,
    'graffie': 100,
    'indigenous': 100,
    'nekoSpace': 100,
    'captainRed': 100,
    'radioJack': 100,
    'papaSanta': 100,
    'jiangshi': 100,
    'wastelander': 100,
    'neonDJ': 100,
    'oniChan': 100,
    'dragonDancer': 100,
    'punkPink': 100,
    'miniMe': 100,
    'bigTime': 100,
    'catstronaut': 100,
    'nuMechWarrior': 100,
    'bombardier': 100,
    'spaceTrooper': 100,
    'gakusei': 100,
    'cyberFixer': 100,
    'guardianOfOcean': 100,
    'metroWarrior': 100,
    'fixer': 100,
    'patisseire': 100,
    'surgicalPrecision': 100,
    'metro2021': 100,
    'pharaoh': 100,
    'turnDownTheHeat': 100,
    'cowboy': 100,
    'dogInACat': 100,
    'wanderingSamurai': 100,
    'cosmicExplorer': 100,
    'shikigami': 100,
    'mayanNomad': 100,
    'sunRaver': 100,
    'yinYangMaster': 100
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


# variations cua cac asset thiet lap o day (khi them asset moi can bo sung)
as_variations = {
    # races
    'body_colors': ['_red', '_brown', '_black', '_blue'],
}

# data de tao cac unique combinations
as_data = {
    'all_races': ['cyborg','infected','canis','cosmic']
}