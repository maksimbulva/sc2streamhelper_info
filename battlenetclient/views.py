from django.http import HttpResponseNotFound, HttpResponseBadRequest, JsonResponse
from django.utils.html import escape
from sc2streamhelper.settings import ACCESS_TOKEN, API_KEY
from .converter import to_int
from .ladder_parser import get_race, is_same_race
from .regions import get_server_by_region
from .sc2profile import sc2profile

import requests


# Create your views here.

def mmr(_, region, character_id, realm, character_name, race):
    server = get_server_by_region(region)
    if not server:
        return make_mmr_bad_request_response('region', region)

    profile = sc2profile(to_int(character_id), to_int(realm),
                         character_name)

    url = server + '/sc2/profile/' + profile.path() + '/ladders?apikey=' + API_KEY
    r = requests.get(url)

    if r.status_code != requests.codes.ok:
        return HttpResponseBadRequest('Request to battle.net failed with status code ' + r.status_code)

    solo_ladders = []

    data = r.json()
    for ladder_entry in data['currentSeason']:
        ladders = ladder_entry['ladder']
        if len(ladders) == 0:
            continue
        ladder = ladders[0]
        if ladder['matchMakingQueue'] == 'LOTV_SOLO':
            solo_ladders.append(int(ladder['ladderId']))

    for ladder_id in solo_ladders:
        url = server + '/data/sc2/ladder/' + str(ladder_id) + '?access_token=' + ACCESS_TOKEN
        r = requests.get(url)

        if r.status_code != requests.codes.ok:
            return HttpResponseBadRequest('Request to battle.net failed with status code ' + r.status_code)

        ladder_data = r.json()
        for team_info in ladder_data['team']:
            for m in team_info['member']:
                m_profile = m['legacy_link']
                if m_profile['path'] == '/profile/' + profile.path():
                    if is_same_race(get_race(m), race):
                        result = {
                            'rating': team_info['rating'],
                            'wins':   team_info['wins'],
                            'losses': team_info['losses'],
                            'points': team_info['points'],
                        }
                        return JsonResponse(result)

    return HttpResponseNotFound()


def make_mmr_bad_request_response(param_name, param_value):
    return HttpResponseBadRequest(escape(
        'Bad ' + param_name + ' value ' + param_value + '\n'))
