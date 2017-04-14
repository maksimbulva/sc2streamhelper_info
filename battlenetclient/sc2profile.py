from .exceprions import BadParameter


class sc2profile:
    def __init__(self, character_id, realm, display_name):
        if (character_id is None) or (not isinstance(character_id, int)) or character_id <= 0:
            raise BadParameter('character_id', character_id)
        self.character_id = character_id

        if (realm is None) or (not isinstance(realm, int)) or realm <= 0:
            raise BadParameter('realm', realm)
        self.realm = realm

        if (not display_name) or (not isinstance(display_name, str)):
            raise BadParameter('display_name', display_name)
        self.display_name = display_name

    def path(self):
        return str(self.character_id) + '/' + str(self.realm) + '/' + self.display_name
