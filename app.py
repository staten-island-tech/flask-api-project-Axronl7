from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/")
def index():
    # Get the list of Valorant agents from the API
    response = requests.get("https://valorant-api.com/v1/agents?isPlayableCharacter=true")
    data = response.json()  # Parse JSON response from the API
    agent_list = data['data']  # Extract the list of agents from the response

    agents = []  # List to store the agents' basic information
    agents_by_role = {}  # Dictionary to group agents by their role

    # Loop through each agent in the list
    for agent in agent_list:
        role = agent['role']['displayName'] if agent['role'] else "No Role"
        agent_info = {
            'name': agent['displayName'],
            'id': agent['uuid'],  # Unique identifier for the agent
            'image': agent['displayIcon'],  # Icon image of the agent
            'role': role
        }
        agents.append(agent_info)

        # Group agents by their role
        if role not in agents_by_role:
            agents_by_role[role] = []
        agents_by_role[role].append(agent_info)

    return render_template("index.html", agents=agents, agents_by_role=agents_by_role)


@app.route("/agent/<uuid>")
def agent_detail(uuid):
    # Get detailed information for a specific agent using UUID
    response = requests.get(f"https://valorant-api.com/v1/agents/{uuid}")
    data = response.json()  # Parse JSON response
    agent = data['data']

    # Pass agent details to the template
    return render_template("agent.html", agent={
        'name': agent['displayName'],
        'description': agent['description'],
        'image': agent['fullPortrait'],  # Full portrait image for detailed view
        'role': agent['role']['displayName'] if agent['role'] else "No Role",
        'abilities': [
            {
                'name': ability['displayName'],
                'description': ability['description'],
                'icon': ability['displayIcon']
            } for ability in agent['abilities'] if ability['displayName']  # Skip empty abilities
        ]
    })

if __name__ == '__main__':
    app.run(debug=True)
