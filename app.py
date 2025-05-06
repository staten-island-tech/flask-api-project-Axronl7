from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/")
def index():
    # Get the first 150 Pokémon from the API
    response = requests.get("https://valorant-api.com/v1/agents?limit=150")
    data = response.json()
    agent_list = data['results']
    
    # Create a list to hold Pokémon details
    agents = []
    
    for agent in agents_list:
        # Each Pokémon URL looks like "https://pokeapi.co/api/v2/pokemon/1/"
        url = agent ['url']
        parts = url.strip("/").split("/")
        id = parts[-1]  # The last part is the Pokémon's ID
        
        # Create an image URL using the Pokémon's ID
        image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png"
        
        agents.append({
            'name': agent['name'].capitalize(),
            'id': id,
            'image': image_url
        })
    
    # Send the Pokémon list to the index.html page
    return render_template("index.html", agents=agents)

# New route: When a user clicks a Pokémon card, this page shows more details and a stats chart
@app.route("/pokemon/<int:id>")
def agent_detail(id):
    # Get detailed info for the Pokémon using its id
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{id}")
    data = response.json()
    
    # Extract extra details like types, height, and weight
    types = [t['type']['name'] for t in data['types']]
    ability = data.get('ability')
    weight = data.get('weight')
    name = data.get('name').capitalize()
    image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png"
    
    # Extract base stats for the chart (e.g., hp, attack, defense, etc.)
    stat_names = [stat['stat']['name'] for stat in data['stats']]
    stat_values = [stat['base_stat'] for stat in data['stats']]
    
    # Send all details to the pokemon.html template
    return render_template("agent.html", agent={
        'name': name,
        'id': id,
        'image': image_url,
        'types': types,
        'height': height,
        'weight': weight,
        'stat_names': stat_names,
        'stat_values': stat_values
    })

if __name__ == '__main__':
    app.run(debug=True)
