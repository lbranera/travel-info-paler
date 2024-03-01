from travel import get_travel_info
from data_retriever import get_localities, get_rtc
from multiprocessing  import Process

rtc_list = get_rtc()
municipal_list = get_localities()

def create_travel_info_matrix(params):
    mode, pass_through = params

    first_line = '"' + '","'.join([''] + rtc_list) + '"'
    time_matrix = distance_matrix = cost_matrix = first_line + "\n"

    for municipal in municipal_list:
        single_row = [ f'"{municipal}"' ]

        time_single_row = single_row.copy()
        distance_single_row = single_row.copy()
        cost_single_row = single_row.copy()

        for rtc in rtc_list:
            try:
                # -- Console logs
                print("SOURCE:", municipal)
                print("DESTINATION:", rtc)
                # -- Console logs

                if (mode.upper() == "AIR"):
                    travel_info = get_travel_info(municipal, rtc, mode)
                else:
                    travel_info = get_travel_info(municipal, rtc, mode, pass_through)

                formatted_travel_time = str(travel_info["time"])
                formatted_travel_distance = str(travel_info["distance"])
                formatted_travel_cost = str(travel_info["cost"])

                # -- Console logs
                print(f"LAND-{mode} TRAVEL TIME:", formatted_travel_time)
                print(f"LAND-{mode} TRAVEL DISTANCE:", formatted_travel_distance)
                print(f"LAND-{mode} TRAVEL COST:", formatted_travel_cost, end="\n\n")
                # -- Console logs

                time_single_row.append(formatted_travel_time)
                distance_single_row.append(formatted_travel_distance)
                cost_single_row.append(formatted_travel_cost)

            except:
                time_single_row.append("_")
                distance_single_row.append("_")
                cost_single_row.append("_")

                # -- Console logs
                print(f"LAND-{mode} TRAVEL TIME: _")
                print(f"LAND-{mode} TRAVEL DISTANCE: _")
                print(f"LAND-{mode} TRAVEL COST: _", end="\n\n")
                # -- Console logs

        time_matrix = time_matrix + ",".join(time_single_row) + "\n"
        distance_matrix = distance_matrix + ",".join(distance_single_row) + "\n"
        cost_matrix = cost_matrix + ",".join(cost_single_row) + "\n"

    if (mode.upper() == "AIR"):
        filenames = [
            "./result/land_air_travel_time_matrix.csv",
            "./result/land_air_travel_distance_matrix.csv",
            "./result/land_air_travel_cost_matrix.csv"
        ]
    else:
        filenames = [
            f"./result/land_sea_{pass_through}_travel_time_matrix.csv",
            f"./result/land_sea_{pass_through}_travel_distance_matrix.csv",
            f"./result/land_sea_{pass_through}_travel_cost_matrix.csv"
        ]

    file_content = [
        time_matrix,
        distance_matrix,
        cost_matrix,
    ]

    for index, filename in enumerate(filenames):
        target_file_content = file_content[index]

        file = open(filename, "w")
        file.write(target_file_content)
        file.close()


def create_travel_info_row(source):        
    
    travel_modes = [
        ("air", None),
        ("sea", "hil"),
        ("sea", "orm"),
    ]

    for mode, pass_through in travel_modes:
        travel_time_list = []
        travel_distance_list = []
        travel_cost_list = []

        for rtc_destination in rtc_list:
            travel_info = get_travel_info(source, rtc_destination, mode, pass_through)

            formatted_travel_time = str(travel_info["time"])
            formatted_travel_distance = str(travel_info["distance"])
            formatted_travel_cost = str(travel_info["cost"])

            travel_time_list.append(formatted_travel_time)
            travel_distance_list.append(formatted_travel_distance)
            travel_cost_list.append(formatted_travel_cost)

            print("SOURCE:", source)
            print("DESTINATION:", rtc_destination)

        # Done travel info computation

        if (mode == "air"):
            filenames = [
                ("./result/land_air_travel_time_matrix.csv"),
                ("./result/land_air_travel_distance_matrix.csv"),
                ("./result/land_air_travel_cost_matrix.csv"),
            ]
        else:
            filenames = [
                f"./result/land_sea_{pass_through}_travel_time_matrix.csv",
                f"./result/land_sea_{pass_through}_travel_distance_matrix.csv",
                f"./result/land_sea_{pass_through}_travel_cost_matrix.csv",
            ]


            travel_info_list = [
                travel_time_list,
                travel_distance_list,
                travel_cost_list,
            ]

            for index, filename in enumerate(filenames):
                file = open(filename)
                row_entries = [entry for entry in file.readlines()]
                file.close()

                target_row_index = 0
                for row_index, row_entry in enumerate(row_entries):
                    if (source.upper() in row_entry.upper()):
                        target_row_index = row_index
                        break

                target_travel_info_list = travel_info_list[index]

                updated_row = f'"{source}",' + ",".join(target_travel_info_list) + "\n"
                row_entries[target_row_index] = updated_row

                updated_content = "".join(row_entries)

                file = open(filename, "w")
                file.write(updated_content)
                file.close()


if __name__ == "__main__":
    #p1 = Process(target=create_travel_info_matrix, args=(("air", None),))
    #p2 = Process(target=create_travel_info_matrix, args=(("sea", "hil"),))
    #p3 = Process(target=create_travel_info_matrix, args=(("sea", "orm"),))

    #p1.start()
    #p2.start()
    #p3.start()

    #p1.join()
    #p2.join()
    #p3.join()
    
    create_travel_info_row(source = "Allen,Northern Samar")

