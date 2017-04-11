def get_race(team_member):
    played_race_count = team_member['played_race_count']
    if played_race_count:
        return played_race_count[0]['race']['en_US']
    return None


def is_same_race(race1, race2):
    return race1[0].lower() == race2[0].lower()

