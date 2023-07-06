# Get the database using the method we defined in pymongo_test_insert file
from pymongo_get_database import get_database


def shots(event: dict):
    attr: list = event['tagAttributes']
    result = ""
    x = 0
    y = 0
    for item in attr:
        match item['name']:
            case 'Result':
                result = item['value']
            case 'Field Location':
                x = item['value']['x']
                y = item['value']['y']
    ret_value = "Shot," + result + "," + str(x) + "," + str(y)
    return ret_value


dbname = get_database()

# Retrieve a collection named "user_1_items" from database
collection_name = dbname["vidswap"]

extract_dict = {'Shot': shots}

games = collection_name.find()
for game in games:
    playlist = game['playlist']
    game_id = playlist['id']
    # This does not give a very readable output
    print(playlist['name'] + ' on ' + playlist['date'])
    for event in game['tagEvents']:
        event_name = event['tagResource']['name']
        if (event_name in extract_dict.keys()):
            print(str(game_id) + "," + extract_dict[event_name](event))
