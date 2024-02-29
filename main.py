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
        cost_matrix = cost_matrix + ",".join(distance_single_row) + "\n"

    if (mode.upper() == "AIR"):
        file = open(f"land_{mode}_travel_time_matrix.csv", "w")
        file.write(time_matrix)
        file.close()

        file = open(f"land_{mode}_travel_distance_matrix.csv", "w")
        file.write(distance_matrix)
        file.close()

        file = open(f"land_{mode}_travel_cost_matrix.csv", "w")
        file.write(cost_matrix)
        file.close()
    else:
        file = open(f"land_{mode}_{pass_through}_travel_time_matrix.csv", "w")
        file.write(time_matrix)
        file.close()

        file = open(f"land_{mode}_{pass_through}_travel_distance_matrix.csv", "w")
        file.write(distance_matrix)
        file.close()

        file = open(f"land_{mode}_{pass_through}_travel_cost_matrix.csv", "w")
        file.write(cost_matrix)
        file.close()

if __name__ == "__main__":
    p1 = Process(target=create_travel_info_matrix, args=(("air", ""),))
    p2 = Process(target=create_travel_info_matrix, args=(("sea", "hil"),))
    p3 = Process(target=create_travel_info_matrix, args=(("sea", "orm"),))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

