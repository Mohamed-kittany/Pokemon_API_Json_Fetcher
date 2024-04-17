#!/usr/bin/env python3
import requests
import random
import json
import os


# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))


''' <><><> Constants <><><> '''
# Create the full path for 'data.json' relative to the current script
FILENAME = os.path.join(current_directory, 'data.json')
POKEMON_API = "https://pokeapi.co/api/v2/pokemon"
LIMIT = 100000


def get_pokemon_count_and_results():
    # URL to the Pokémon API (using a high limit value in the url to get all Pokémon from db).
    url = f"{POKEMON_API}?limit={LIMIT}"

    # GET request.
    response = requests.get(url)
    data = response.json()

    # Extract count and results from the response.
    count_of_pokemons = data['count']
    results = data['results']

    return response.status_code, count_of_pokemons, results


def get_pokemon_from_api(pokemon_name):
    # URL to the Pokémon API (Get Pokémon by name)
    url = f"{POKEMON_API}/{pokemon_name}"

    # GET request.
    response = requests.get(url)
    pokemon = response.json()
    return response.status_code, pokemon


def extract_pokemon_details(pokemon_name):
    response_status_code, pokemon = get_pokemon_from_api(pokemon_name)
    if response_status_code != 200:
        print("Failed to retrieve data. Status code:", response_status_code)
        return None
    else:
        filtered_pokemon = {
            "id": pokemon["id"],
            "name": pokemon["name"],
            "weight": pokemon["weight"],
            "image": pokemon["sprites"]["front_default"]
        }
        return filtered_pokemon


def get_all_pokemons_from_json_file():
    try:
        # Open the file and read the JSON data
        with open(FILENAME, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return None
    except json.JSONDecodeError:
        print("Failed to decode JSON. Please check the file content.")
        return None


def write_pokemon_from_api_to_json_file(pokemon_name):
    pokemons_json = get_all_pokemons_from_json_file()

    if pokemons_json is None:
        return None
    else:
        # Getting the filtered Pokémon details by the Pokémon name.
        pokemon_filtered_details = extract_pokemon_details(pokemon_name)
        if pokemon_filtered_details is not None:
            # Append the new Pokémon to the list of Pokémon
            pokemons_json['pokemons'].append(pokemon_filtered_details)

            # Save Pokémon to data.json file
            # Write the updated data back to the file
            with open(FILENAME, 'w') as file:
                json.dump(pokemons_json, file, indent=4)


def check_if_pokemon_exist_in_db(pokemon_name):
    pokemons_json = get_all_pokemons_from_json_file()
    if pokemons_json is None:
        return None
    else:
        if len(pokemons_json['pokemons']) > 0:
            for pokemon in pokemons_json['pokemons']:
                if pokemon['name'] == pokemon_name:
                    print(f"Pokemon Details: ")
                    print(f"Pokemon ID: {pokemon['id']}")
                    print(f"Pokemon Name: {pokemon['name']}")
                    print(f"Pokemon Weight: {pokemon['weight']}")
                    print(f"Pokemon Image: {pokemon['image']}")
                    return True
        return False


def download_pokemon_list():
    response_status_code, pokemons_count, pokemon_results = get_pokemon_count_and_results()
    # Check if the request was successful.
    if response_status_code != 200:
        print("Failed to retrieve data. Status code:", response_status_code)
        return
    else:
        # List of random Pokémon (indexes). In this case we get 4 random indexes.
        random_pokemons_indexes = [random.randint(0, int(pokemons_count)) for _ in range(4)]
        # Choose random Pokémon (index) from the random Pokémon indexes.
        random_pokemon_index = random.choice(random_pokemons_indexes)
        # Get the name of the chosen Pokémon
        pokemon_name = pokemon_results[random_pokemon_index]["name"]

        # Check by name if the chosen Pokémon exist in data.json file
        # If chosen Pokémon exist in data.json file then print its details.
        # If chosen Pokémon doesn't exist in db then get its detail's from the api and write to the data.json file.
        is_pokemon_exist = check_if_pokemon_exist_in_db(pokemon_name)
        if not is_pokemon_exist and is_pokemon_exist is not None:
            write_pokemon_from_api_to_json_file(pokemon_name)


def main():
    while True:
        choice = input("Would like to draw a Pokémon? (Y/N) ")
        choice = choice.lower()

        if choice == "y":
            print("Start downloading pokemon list...")
            download_pokemon_list()
        elif choice == "n":
            print("See you around!")
            break
        else:
            print("Invalid choice option. Please try again.")


if __name__ == "__main__":
    main()
