from django.http import HttpResponseNotFound, HttpResponseBadRequest, JsonResponse
from django.utils.html import escape
from sc2streamhelper.settings import ACCESS_TOKEN, API_KEY
from .converter import to_int
from .exceprions import BadParameter, BnetRequestFailed
from .ladder_parser import get_race, is_same_race, validate_race
from .ladders import fetch_ladder
from .models import Players
from .regions import get_region_code, get_server_by_region
from .sc2profile import sc2profile

import requests


# Create your views here.

def mmr(_, region, character_id, realm, character_name, race):
    try:
        server = get_server_by_region(region)
        race = validate_race(race)
        profile = sc2profile(to_int(character_id), to_int(realm),
                             character_name)
        result_dict = get_mmr(server, profile.path(), race)
        if result_dict:
            return JsonResponse(result_dict)

    except BadParameter as e:
        return make_bad_request_response(e.parameter_name,
                                         e.parameter_value)
    except BnetRequestFailed as e:
        return make_bnet_request_failed_response(e.request_status_code)

    return HttpResponseNotFound()


def lookup_mmr(_, region, character_name, race):
    results = []
    try:
        server = get_server_by_region(region)
        region_code = get_region_code(region)
        race = validate_race(race)

        if (not character_name) or (not isinstance(character_name, str)):
            raise BadParameter('character_name', character_name)

        # Fetch at most 5 players with this name
        query = Players.objects.filter(region_code=region_code) \
                               .filter(display_name=character_name)[:5]
        for player in query:
            try:
                result_dict = get_mmr(server, player.profile_path, race)
                if (result_dict is not None) and len(result_dict) > 0:
                    results.append(result_dict)
            except:
                pass

    except BadParameter as e:
        return make_bad_request_response(e.parameter_name,
                                         e.parameter_value)

    return JsonResponse({'results': results})


def update(_, region, ladder_id):
    server = get_server_by_region(region)
    region_code = get_region_code(region)
    if (not server) or (region_code is None):
        return make_bad_request_response('region', region)

    # Counters to be sent back in JSON
    players_fetched_count = 0
    new_players_count = 0

    ladder_data = fetch_ladder(server, ladder_id)
    for team_info in ladder_data['team']:
        for m in team_info['member']:
            players_fetched_count += 1
            m_profile = m['legacy_link']
            key = m_profile['id']
            name, _, _ = m_profile['name'].partition('#')

            profile_path = m_profile['path']
            if profile_path.startswith('/profile/'):
                profile_path = profile_path[len('/profile/'):]

            player = Players.objects.filter(pk=key).first()
            if player is None:
                # Create the new player
                new_players_count += 1
                player = Players(
                    player_id=key,
                    region_code=region_code,
                    display_name=name,
                    profile_path=profile_path,
                )
            else:
                # Update the current player record
                player.region_code = region_code
                player.display_name = name
                player.profile_path = profile_path

            player.save()

    return JsonResponse({
        'players_fetched_count': players_fetched_count,
        'new_players_count': new_players_count,
    })


def stats(_, region):
    return JsonResponse({
        'players_count': Players.objects.count()
    })


def make_bad_request_response(param_name, param_value):
    return HttpResponseBadRequest(escape(
        'Bad "' + param_name + '" value "' + param_value + '"\n'))


def make_bnet_request_failed_response(error_code):
    return HttpResponseBadRequest('Request to battle.net failed with status code ' + str(error_code))


def get_mmr(server, profile_path, race):
    url = server + '/sc2/profile/' + profile_path + '/ladders?apikey=' + API_KEY
    r = requests.get(url)

    if r.status_code != requests.codes.ok:
        raise BnetRequestFailed(r.status_code)

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
        ladder_data = fetch_ladder(server, ladder_id)
        for team_info in ladder_data['team']:
            for m in team_info['member']:
                m_profile = m['legacy_link']
                if m_profile['path'] == '/profile/' + profile_path:
                    if is_same_race(get_race(m), race):
                        return {
                            'profile_path': profile_path,
                            'race': race,
                            'rating': team_info['rating'],
                            'wins': team_info['wins'],
                            'losses': team_info['losses'],
                            'points': team_info['points'],
                        }
    return None
