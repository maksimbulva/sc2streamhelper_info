BNET_REGIONS = {
    'eu': 'https://eu.api.battle.net',
    'us': 'https://us.api.battle.net',
    'sea': 'https://sea.api.battle.net',
    'kr': 'https://kr.api.battle.net',
    'cn': 'https://battlenet.com.cn'
}

BNET_REGION_CODES = {
    'eu':  1,
    'us':  2,
    'sea': 3,
    'kr':  4,
    'cn':  5,
}


def get_server_by_region(region):
    try:
        return BNET_REGIONS[region.lower()]
    except:
        return None


def get_region_code(region):
    try:
        return BNET_REGION_CODES[region.lower()]
    except:
        return None
