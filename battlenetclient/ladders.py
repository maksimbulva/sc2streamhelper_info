from .exceprions import FetchFailedException
from sc2streamhelper.settings import ACCESS_TOKEN
import requests


def fetch_ladder(server, ladder_id):
    url = server + '/data/sc2/ladder/' + str(ladder_id) + '?access_token=' + ACCESS_TOKEN
    r = requests.get(url)

    if r.status_code != requests.codes.ok:
        # TODO
        raise FetchFailedException

    return r.json()


def fetch_ladders(player_profile_json, match_making_queue: str) -> object:
    result = []

    for ladder_entry in player_profile_json['currentSeason']:
        ladders = ladder_entry['ladder']
        if len(ladders) == 0:
            continue
        ladder = ladders[0]
        if ladder['matchMakingQueue'] == match_making_queue:
            result.append(int(ladder['ladderId']))
    return result
