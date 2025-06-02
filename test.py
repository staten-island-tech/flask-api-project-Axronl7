import requests

response = requests.get("https://raw.githubusercontent.com/WhalenSITHS/Pokedex-Python-Starter/main/pokedex.json")
data = response.json()  


for pokemon in data:
    if 'Bug' in pokemon['type'] and 'Fire' in pokemon['type']:
        print(pokemon['name']['japanese']) 

for pokemon in data:
    if pokemon['base']['HP'] > 65:
        print(pokemon['name']['english'])