import os
import csv
import requests
from dotenv import load_dotenv
from data_converter import meters_to_kilometers

load_dotenv()

# Replace 'YOUR_API_KEY' with your actual Google Maps API key

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# List of airports

air_ports = {
    "MNL": "NAIA,Pasay City,Metro Manila",
    "TAC": "Daniel Romualdez Airport,Tacloban City,Leyte",
    "CEB": "Mactan-Cebu International Airport,Lapu-Lapu City,Cebu",
}

# List of seaports

sea_ports = {
    "HIL": "Hilongos,Leyte",
    "ORM": "Ormoc City,Leyte",
    "MAT": "Matnog,Sorsogon",
    "ALL": "Allen,Northern Samar",
    "CEB": "Cebu City,Cebu",
}

# Determines land travel cost using bus-fare formula 

def get_land_travel_cost(distance):
    distance_km = meters_to_kilometers(distance)
    starting_cost = 13

    if (distance_km <= 5):
        return starting_cost
    else:
        additional_cost = (distance_km - 5) * 2.25
        return (starting_cost + additional_cost)

# Determines (travel time, distance, cost) from one locality to another locality '''

def get_land_travel_info(source, destination, mode='driving'):
    if source == destination:
        return 0
    else:
        base_url = "https://maps.googleapis.com/maps/api/directions/json"
        
        params = {
            'origin': source,
            'destination': destination,
            'mode': mode,
            'key': GOOGLE_API_KEY,
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        #print(data)

        if data['status'] == 'OK':
            routes = data['routes']

            travel_times = []
            travel_distances = []

            for route in routes:
                distance = min([ float(leg['distance']['value']) for leg in route['legs']])
                time = min([ float(leg['duration']['value']) for leg in route['legs']])

                travel_times.append(time)
                travel_distances.append(distance)
            
            travel_time = min(travel_times)
            travel_distance = min(travel_distances)
            travel_cost = get_land_travel_cost(travel_distance)

            return {
                "time": travel_time,
                "distance": travel_distance,
                "cost": travel_cost
            }

# Determines (travel time, distance, cost) from Tacloban Airport to MNL or CEB '''

def get_flight_info(destination):

    file = open("./data/flights.csv")
    csv_reader = csv.reader(file, quotechar='"')

    for (_, flight_dest, time, distance, cost) in csv_reader:
        if (destination == flight_dest):

            travel_info = {
                "time": float(time),
                "distance": float(distance),
                "cost": float(cost),
            }


            return travel_info

# Determines (travel time, distance, cost) from one seaport to another seaport '''

def get_ship_info(source, destination):
    
    file = open("./data/ships.csv")
    csv_reader = csv.reader(file, quotechar='"')

    for (ship_source, ship_dest, time, distance, cost) in csv_reader:
        if ((source == ship_source) and (destination == ship_dest)):

            travel_info = {
                "time": float(time),
                "distance": float(distance),
                "cost": float(cost),
            }

            return travel_info

# Determines if the RTC place is located in Metro Manila '''

def is_rtc_metro_manila(place):
    return ("METRO MANILA" in place.upper())

# Determines (travel time, distance, cost, path) from source to destination '''

def get_travel_info(source, destination, mode, pass_through = None):
    try:
        if (mode.upper() == "AIR"):
            if (is_rtc_metro_manila(destination)):
                AIRPORT_KEY_INDEX = "MNL"
            else:
                AIRPORT_KEY_INDEX = "CEB"

            origin_to_airport = get_land_travel_info(source, air_ports["TAC"])
            airport_to_airport = get_flight_info(air_ports[AIRPORT_KEY_INDEX])
            airport_to_RTC = get_land_travel_info(air_ports[AIRPORT_KEY_INDEX], destination)
            
            travel_info_array = [
                origin_to_airport,
                airport_to_airport,
                airport_to_RTC,
            ]

            travel_time = sum([info["time"] for info in travel_info_array])
            travel_distance = sum([info["distance"] for info in travel_info_array])
            travel_cost = sum([info["cost"] for info in travel_info_array])

            travel_path = [source, air_ports["TAC"], air_ports[AIRPORT_KEY_INDEX], destination]
            
            return {
                "time": travel_time,
                "distance": travel_distance,
                "cost": travel_cost,
                "path": travel_path,
            }

        elif (mode.upper() == "SEA"):

            if (is_rtc_metro_manila(destination)):           
                origin_to_seaport = get_land_travel_info(source, sea_ports["ALL"])
                seaport_to_seaport = get_ship_info(sea_ports["ALL"], sea_ports["MAT"])
                seaport_to_RTC = get_land_travel_info(sea_ports["MAT"], destination)
                
                travel_info_array = [
                    origin_to_seaport,
                    seaport_to_seaport,
                    seaport_to_RTC,
                ]

                travel_time = sum([info["time"] for info in travel_info_array])
                travel_distance = sum([info["distance"] for info in travel_info_array])
                travel_cost = sum([info["cost"] for info in travel_info_array])

                travel_path = [source, sea_ports["ALL"], sea_ports["MAT"], destination]

                return {
                    "time": travel_time,
                    "distance": travel_distance,
                    "cost": travel_cost,
                    "path": travel_path,
                }

            else:

                if (pass_through.upper() == "HIL"):
                    SEAPORT_KEY_INDEX = "HIL"
                elif (pass_through.upper() == "ORM"):
                    SEAPORT_KEY_INDEX = "ORM"
                
                origin_to_seaport = get_land_travel_info(source, sea_ports[SEAPORT_KEY_INDEX])
                seaport_to_seaport = get_ship_info(sea_ports[SEAPORT_KEY_INDEX], sea_ports["CEB"])
                seaport_to_RTC = get_land_travel_info(sea_ports["CEB"], destination)

                travel_info_array = [
                    origin_to_seaport,
                    seaport_to_seaport,
                    seaport_to_RTC,
                ]

                travel_time = sum([info["time"] for info in travel_info_array])
                travel_distance = sum([info["distance"] for info in travel_info_array])
                travel_cost = sum([info["cost"] for info in travel_info_array])

                travel_path = [source, sea_ports[SEAPORT_KEY_INDEX], sea_ports["CEB"], destination]

                return {
                    "time": travel_time,
                    "distance": travel_distance,
                    "cost": travel_cost,
                    "path": travel_path,
                }

        else:
            raise Exception

    except Exception as error:
        print("Error in getting travel route and travel time.")
        print(error)



if __name__ == "__main__":

    travel_info = get_travel_info(
        source = "Abuyog,Leyte",
        destination = "Cebu Doctors University Hospital,Cebu City,Cebu",
        mode = "air"
    )

    print(travel_info)

    #travel_info = get_land_travel_info("Abuyog,Leyte", air_ports["TAC"])
    #print(travel_info)