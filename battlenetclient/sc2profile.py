class sc2profile:
    def __init__(self, character_id, realm, display_name):
        self.character_id = character_id
        self.realm = realm
        self.display_name = display_name

    def path(self):
        return str(self.character_id) + '/' + str(self.realm) + '/' + self.display_name
