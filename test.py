import json

def print_states_cities_and_areacodes_from_json():
    # Load JSON data with explicit encoding
    with open('raw.json', encoding='utf-8') as f:
        data = json.load(f)

    # Create a dictionary to store cities and their associated area codes by state
    states_cities_areacodes = {}

    # Extract and store cities and their associated area codes by state
    for entry in data:
        state = entry["state"]
        city = entry["city"]
        areacode = entry["area-code"]
        if state in states_cities_areacodes:
            if city in states_cities_areacodes[state]:
                states_cities_areacodes[state][city].append(areacode)
            else:
                states_cities_areacodes[state][city] = [areacode]
        else:
            states_cities_areacodes[state] = {city: [areacode]}

    # Print states, cities, and associated area codes
    print("States, Cities, and Associated Area Codes:")
    for state, cities_areacodes in sorted(states_cities_areacodes.items()):
        print(state + ":")
        for city, areacodes in cities_areacodes.items():
            print(" -", city + ":")
            for areacode in areacodes:
                print("   -", areacode)

if __name__ == "__main__":
    print_states_cities_and_areacodes_from_json()
