import sqlite3
import sys

types = ["bug", "dark", "dragon", "electric", "fairy", "fight",
         "fire", "flying", "ghost", "grass", "ground", "ice", "normal",
         "poison", "psychic", "rock", "steel", "water"]

if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

for i, arg in enumerate(sys.argv):
    if i == 0:
        continue

    try:
        pokedex_num = int(arg)
    except ValueError:
        print(f"Error: Invalid pokedex number {arg}")
        sys.exit()

    conn = sqlite3.connect('../pokemon.sqlite')
    cursor = conn.cursor()

    name_and_types = ("SELECT p.name, pv.type1, pv.type2 FROM pokemon p JOIN pokemon_types_view AS pv ON p.name = pv.name WHERE p.id = " + arg + ";")
    cursor.execute(name_and_types)
    result = cursor.fetchone()
    pokemon_name = result[0]
    pokemon_types = (result[1], result[2])

    cursor.execute("SELECT * FROM pokemon_types_battle_view WHERE type1name = ? and type2name = ?",
              (pokemon_types[0], pokemon_types[1]))
    against_result = cursor.fetchone()

    new_against_result = against_result[2:]

    against_map = {}
    for against, nums in zip(types, new_against_result):
        against_map[against] = nums

    strengths = []
    weaknesses = []
    for against in against_map.keys():
        if against_map[against] > 1:
            strengths.append(against)
        elif against_map[against] < 1:
            weaknesses.append(against)

    print(f"Analyzing {arg}")
    print(f"{pokemon_name} ({pokemon_types[0]}{' ' + pokemon_types[1] if pokemon_types[1] else ''}) is strong against {strengths} but weak against {weaknesses}")
    conn.close()

answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")
