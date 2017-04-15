from subprocess import call
from time import sleep

def populate_database(region_str, ladder_id_min, ladder_id_max):
    for ladder_id in range(ladder_id_min, ladder_id_max + 1):
        print('Fetching ladder id ' + str(ladder_id))
        call([
            'curl',
            'http://127.0.0.1/data/' + region_str + '/update/' + str(ladder_id)
        ])
        # Respect battle net API requests per second limit
        sleep(0.020)


if __name__ == '__main__':
    print('Do not call this directly, use scripts with region names like eu_populate_database.py')
