# Get the database using the method we defined in pymongo_test_insert file
import csv
import time

from pymongo_get_database import get_database

X_LEFT_18 = 144.8
X_RIGHT_18 = 885.2
X_YARD = (X_RIGHT_18 - X_LEFT_18) / 44.0
X_CENTER = (X_RIGHT_18 + X_LEFT_18) / 2.0

Y_GOAL_LINE = 887.2428977
Y_TOP_18 = 642.842879
Y_YARD = (Y_TOP_18 - Y_GOAL_LINE) / 18.0


def shot(shot_event: dict):
    attr: list = shot_event['tagAttributes']
    result = ""
    x = -1
    y = -1
    for item in attr:
        match item['name']:
            case 'Result':
                result = item['value']
            case 'Field Location':
                x = (item['value']['x'] - X_CENTER) / X_YARD
                y = (item['value']['y'] - Y_GOAL_LINE) / Y_YARD
    if not result or x == -1 or y == -1:
        return []
    return ["shot", result, x, y]


def set_piece(set_piece_event: dict):
    type_set = {'free kick', 'penalty kick', 'corner kick'}
    set_piece_type = ""
    for attribute in set_piece_event['tagAttributes']:
        if attribute["name"] == "Type":
            if attribute["value"] in type_set:
                set_piece_type = attribute["value"]
            else:
                return []
    return ["set_piece", set_piece_type]


extract_dict = {'Shot': shot,
                'Set Piece': set_piece}

games = get_database()["vidswap"].find()

with open('xgdata.csv', 'w', encoding='UTF8', newline='') as xg_data_file:
    xg_data_writer = csv.writer(xg_data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for game in games:
        playlist = game['playlist']
        game_id = playlist['id']
        period = 0
        periodStart = 0
        oldPeriodStart = -1

        print(playlist['name'] + ' on ' + playlist['date'] + " - " + str(game_id))
        e_tot = 0;
        shot_total = 0;
        shot_rec = 0;
        set_total = 0;
        set_rec = 0;
        for event in game['tagEvents']:
            e_tot += 1
            event_name = event['tagResource']['name']
            if event_name in extract_dict.keys():
                match event_name:
                    case "Shot":
                        shot_total += 1
                    case "Set Piece":
                        set_total += 1
                extract_data = extract_dict[event_name](event)
                if extract_data:
                    startEvent = int(time.mktime(time.strptime(event['startOffset'], "%H:%M:%S.%f")))
                    offset = startEvent - periodStart
                    match event_name:
                        case "Shot":
                            shot_rec += 1
                            offset += 3
                        case "Set Piece":
                            set_rec += 1
                            offset += 2
                    event_data = [game_id, period, offset]
                    event_data.extend(extract_dict[event_name](event))
                    xg_data_writer.writerow(event_data)
            else:
                if event_name == 'Period':
                    periodStart = int(time.mktime(time.strptime(event['startOffset'], "%H:%M:%S.%f")))
                    if periodStart != oldPeriodStart:
                        # only change period if start time changed
                        period += 1
                        oldPeriodStart = periodStart
        print(str(period) + " e: " + str(e_tot) + " shot: " + str(shot_rec) + "/" + str(shot_total) + " set: " + str(set_rec) + "/" + str(set_total) )
