import itertools

races_types = ['normal','android', 'anatomicanis', 'alien']
asset_types = ['clothing', 'hand', 'hat']
asset_sets = [
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
    
]

all_assets =  list(itertools.product(*[asset_types,races]))

print(all_assets)