import requests
response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1")
data = response.json()
pokemon_list = data['results']
for pokemon in pokemon_list:
    print(pokemon['name'])