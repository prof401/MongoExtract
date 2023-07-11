import csv

GAME_ID = 0
PERIOD = 1
TIME = 2
EVENT_NAME = 3
SHOT_RESULT = 4
SHOT_X = 5
SHOT_Y = 6
SET_PIECE_TYPE = 4

EVENT_SHOT = 'shot'
EVENT_SET_PIECE = 'set_piece'

shot_list = list()


def add_shot(shot_event: list, kick_type: str):
    add_event = shot_event
    match kick_type:
        case "":
            add_event.append("")
        case "free kick":
            add_event.append("fk")
        case "corner kick":
            add_event.append("ck")
        case "penalty kick":
            add_event.append("pk")
        case _:
            print(kick_type)
    shot_list.append(add_event)


def update_last_event(set_piece_type):
    code = ""
    match set_piece_type:
        case "":
            code = ""
        case "free kick":
            code = "fk"
        case "corner kick":
            code = "ck"
        case "penalty kick":
            code = "pk"
        case _:
            print(set_piece_type)
    shot_list[len(shot_list) - 1][len(shot_list[0]) - 1] = code


clear_last = False
with open('xgdata.csv', 'r', encoding='UTF8', newline='') as xg_data_file:
    xg_data_reader = csv.reader(xg_data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    last_event = list()
    for event in xg_data_reader:
        clear_last = False
        if len(event) >= 5:
            if event[EVENT_NAME] == EVENT_SHOT:
                if len(last_event) >= 5 and last_event[EVENT_NAME] == EVENT_SET_PIECE and last_event[GAME_ID] == event[
                    GAME_ID] and last_event[PERIOD] == event[PERIOD]:
                    if int(event[TIME]) - int(last_event[TIME]) <= 5 or (
                            last_event[SET_PIECE_TYPE] == "penalty kick" and int(event[TIME]) - int(
                        last_event[TIME]) <= 30):
                        add_shot(event, last_event[SET_PIECE_TYPE])
                    else:
                        add_shot(event, "")
                else:
                    add_shot(event, "")
            if len(last_event) >= 5 and event[EVENT_NAME] == EVENT_SET_PIECE and last_event[EVENT_NAME] == EVENT_SHOT:
                if last_event[GAME_ID] == event[GAME_ID] and last_event[PERIOD] == event[PERIOD] and int(
                    event[TIME]) - int(last_event[TIME]) <= 1:
                    update_last_event(event[SET_PIECE_TYPE])
                    clear_last = True
        if clear_last:
            last_event = list()
        else:
            last_event = event

with open('shot_data.csv', 'w', encoding='UTF8', newline='') as xg_data_file:
    xg_data_writer = csv.writer(xg_data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for shot in shot_list:
        xg_data_writer.writerow(shot)
