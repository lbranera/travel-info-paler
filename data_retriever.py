import csv

# Retrieves ./data/eastern_visayas.csv

def get_municities():

    exemptions = [
        "Almagro,Samar",
        "Biri,Northern Samar",
        "Capul,Northern Samar",
        "Daram,Samar",
        "Jipapad,Eastern Samar",
        "Limasawa,Southern Leyte",
        "Maripipi,Biliran",
        "Matuguinao,Samar",
        "Maydolong,Eastern Samar",
        "Motiong,Northern Samar",
        "San Antonio,Northern Samar",
        "San Vicente,Northern Samar",
        "Santo Nino,Samar",
        "Silvino Lobos,Nothern Samar",
        "Tagapul-An,Samar",
        "Zumarraga,Samar",
    ]

    file = open("./data/eastern_visayas.csv")
    entries = [",".join(entry.strip().split(",")[1:]) for entry  in file.readlines()]
    entries = entries[1:]

    entries = list(set(entries).difference(set(exemptions)))
    entries.sort()
    file.close()

    return entries

# Retrieves ./data/rtc.csv

def get_radio_therapy_centers():
    file = open("./data/rtc.csv")
    entries = [",".join(entry.strip().split(",")[1:]) for entry  in file.readlines()]
    entries = entries[1:]
    file.close()

    return entries

# Retrieves ./data/flights.csv

def get_flights_info():
    file = open("./data/flights.csv")
    csv_reader = csv.reader(file, quotechar='"')
    flights_info = list(csv_reader)
    flights_info = flights_info[1: ]

    return flights_info

# Reetrieves ./data/ships.csv

def get_ships_info():
    file = open("./data/ships.csv")
    csv_reader = csv.reader(file, quotechar='"')
    ships_info = list(csv_reader)
    ships_info = ships_info[1: ]

    return ships_info


def get_airports():
    file = open("./data/airports.csv")
    csv_reader = csv.reader(file, quotechar='"')
    airports = list(csv_reader)
    airports = airports[1: ]

    airports_dict_list = []

    for key, airport in airports:
        airports_dict_list.append({ key: airport })
    
    return airports_dict_list


def get_seaports():
    file = open("./data/seaports.csv")
    csv_reader = csv.reader(file, quotechar='"')
    seaports = list(csv_reader)
    seaports = seaports[1: ]

    seaports_dict_list = []

    for key, seaport in seaports:
        seaports_dict_list.append({ key: seaport })
    
    return seaports_dict_list


radio_therapy_centers_list = get_radio_therapy_centers()
municities_list = get_municities()

flights_info = get_flights_info()
ships_info = get_ships_info()

airports = get_airports()
seaports = get_seaports()