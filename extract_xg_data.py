# Get the database using the method we defined in pymongo_test_insert file
from pymongo_get_database import get_database
dbname = get_database()


# Retrieve a collection named "user_1_items" from database
collection_name = dbname["vidswap"]

games = collection_name.find()
for game in games:
    playlist = game['playlist']
    game_id = playlist['id']
    # This does not give a very readable output
    print(playlist['name'] + ' on ' + playlist['date'])
    for event in game['tagEvents']:
        event_id = event['id']
        print(event['tagResource']['name'])
        attr = event['tagAttributes']