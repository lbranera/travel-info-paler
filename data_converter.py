# Converts seconds to string hour-and-minutes format

def seconds_to_hours_minutes(seconds):
    seconds = float(seconds)
    if seconds < 0:
        return "Invalid input, please provide a non-negative number of seconds."

    hours, remainder = divmod(seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    return (f"{int(hours)} hours and {int(minutes)} minutes")

# Converts meters to kilometers format

def meters_to_kilometers(meters):
    kilometers = float(meters) / 1000
    return kilometers