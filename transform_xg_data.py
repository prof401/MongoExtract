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

final_list = list()
blank = 0
fk = 0
ck = 0
pk = 0


def add_shot(shot_event: list, kick_type: str):
    global blank
    global fk
    global ck
    global pk
    add_event = shot_event
    match kick_type:
        case "":
            add_event.append("")
            blank += 1
        case "free kick":
            add_event.append("fk")
            fk += 1
        case "corner kick":
            add_event.append("ck")
            ck += 1
        case "penalty kick":
            add_event.append("pk")
            pk += 1
        case _:
            print(kick_type)
    final_list.append(add_event)


def update_last_event(set_piece_type):
    global blank
    global fk
    global ck
    global pk
    code = ""
    match set_piece_type:
        case "":
            blank += 1
        case "free kick":
            code = "fk"
            fk += 1
        case "corner kick":
            code = "ck"
            ck += 1
        case "penalty kick":
            code = "pk"
            pk += 1
        case _:
            print(set_piece_type)
    final_list[len(final_list) - 1][7] = code


clear_last = False
with open('xgdata.csv', 'r', encoding='UTF8', newline='') as xg_data_file:
    xg_data_reader = csv.reader(xg_data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    last_event = list()
    for event in xg_data_reader:
        clear_last = False
        if len(event) >= 5:
            if event[EVENT_NAME] == EVENT_SHOT:
                if len(last_event) >= 5 and last_event[EVENT_NAME] == EVENT_SET_PIECE \
                        and last_event[GAME_ID] == event[GAME_ID] and last_event[PERIOD] == event[PERIOD]:
                    if int(event[TIME]) - int(last_event[TIME]) <= 5 or \
                            (last_event[SET_PIECE_TYPE] == "penalty kick"
                             and int(event[TIME]) - int(last_event[TIME]) <= 30):
                        add_shot(event, last_event[SET_PIECE_TYPE])
                    else:
                        add_shot(event, "")
                else:
                    add_shot(event, "")
            if len(last_event) >= 5 and event[EVENT_NAME] == EVENT_SET_PIECE and last_event[EVENT_NAME] == EVENT_SHOT:
                if last_event[GAME_ID] == event[GAME_ID] and last_event[PERIOD] == event[PERIOD] \
                        and int(event[TIME]) - int(last_event[TIME]) <= 1:
                    update_last_event(event[SET_PIECE_TYPE])
                    clear_last = True
        if clear_last:
            last_event = list()
        else:
            last_event = event
    print(len(final_list))
    print(blank)
    print(fk)
    print(ck)
    print(pk)
