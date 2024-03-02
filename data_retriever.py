# Reads and retrieves eastern_visayas.csv

def get_localities():

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

# Reads and retrieves rtc.csv

def get_rtc():
    file = open("./data/rtc.csv")
    entries = [",".join(entry.strip().split(",")[1:]) for entry  in file.readlines()]
    entries = entries[1:]
    file.close()

    return entries


rtc_list = get_rtc()
municipal_list = get_localities()
