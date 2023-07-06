# Get the database using the method we defined in pymongo_test_insert file
import csv

from pymongo_get_database import get_database

X_LEFT_18 = 144.8
X_RIGHT_18 = 885.2
X_YARD = (X_RIGHT_18 - X_LEFT_18) / 44.0
X_CENTER = (X_RIGHT_18 + X_LEFT_18) / 2.0

Y_GOAL_LINE = 887.2428977
Y_TOP_18 = 642.842879
Y_YARD = (Y_TOP_18 - Y_GOAL_LINE) / 18.0


def shots(event: dict):
    attr: list = event['tagAttributes']
    result = ""
    x = 0.0
    y = 0.0
    for item in attr:
        match item['name']:
            case 'Result':
                result = item['value']
            case 'Field Location':
                x = (item['value']['x'] - X_CENTER) / X_YARD
                y = (item['value']['y'] - Y_GOAL_LINE) / Y_YARD
    return ["shot", result, x, y]


dbname = get_database()

# Retrieve a collection named "user_1_items" from database
collection_name = dbname["vidswap"]

extract_dict = {'Shot': shots}

games = collection_name.find()

with open('xgdata.csv', 'w', encoding='UTF8', newline='') as xg_data_file:
    xg_data_writer = csv.writer(xg_data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for game in games:
        playlist = game['playlist']
        game_id = playlist['id']
        # This does not give a very readable output
        print(playlist['name'] + ' on ' + playlist['date'])
        for event in game['tagEvents']:
            event_name = event['tagResource']['name']
            if (event_name in extract_dict.keys()):
                event_data = [game_id]
                event_data.extend(extract_dict[event_name](event))
                xg_data_writer.writerow(event_data)
