import csv

with open('xgdata.csv', 'r', encoding='UTF8', newline='') as xg_data_file:
    xg_data_reader = csv.reader(xg_data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for event in xg_data_reader:
        print(event)