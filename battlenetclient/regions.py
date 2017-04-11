BNET_REGIONS = {
    'eu': 'https://eu.api.battle.net',
    'us': 'https://us.api.battle.net',
    'sea': 'https://sea.api.battle.net',
    'kr': 'https://kr.api.battle.net',
    'cn': 'https://battlenet.com.cn'
}


def get_server_by_region(region):
    try:
        return BNET_REGIONS[region.lower()]
    except:
        return None
