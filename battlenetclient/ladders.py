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
