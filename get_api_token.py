from subprocess import call
from sc2streamhelper.passwords import *

call([
    "curl",
    "--user " + SC2STREAMHELPER_APIKEY + ":" + SC2STREAMHELPER_APISECRET,
    "--data-urlencode ""grant_type=client_credentials"" ""http://us.battle.net/oauth/token"""
    ])
