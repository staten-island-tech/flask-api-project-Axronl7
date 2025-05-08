from flask import Flask, render_template, abort
import requests

app = Flask(__name__)

# The base URL for the Valorant API
BASE_URL = "https://valorant-api.com/v1/agents"

@app.route("/")
def index():
    # Get the list of Valorant agents from the API
    try:
        response = requests.get(f"{BASE_URL}?isPlayableCharacter=true")
        response.raise_for_status()  # Will raise an error for bad status codes
        data = response.json()  # Parse JSON response from the API

        agent_list = data.get('data', [])  # Safely get agents' data

        agents = []  # List to store the agents' basic information
        agents_by_role = {}  # Dictionary to group agents by their role

        # Loop through each agent in the list and organize their information
        for agent in agent_list:
            role = agent.get('role', {}).get('displayName', "No Role")
            agent_info = {
                'name': agent.get('displayName'),
                'id': agent.get('uuid'),  # Unique identifier for the agent
                'image': agent.get('displayIcon'),  # Icon image of the agent
                'role': role
            }
            agents.append(agent_info)

            # Group agents by their role
            if role not in agents_by_role:
                agents_by_role[role] = []
            agents_by_role[role].append(agent_info)

        return render_template("index.html", agents=agents, agents_by_role=agents_by_role)

    except requests.exceptions.RequestException as e:
        # Handle the exception if API call fails
        print(f"Error fetching agents: {e}")
        abort(500, description="Error fetching agent data from the API")

@app.route("/agent/<uuid>")
def agent_detail(uuid):
    try:
        response = requests.get(f"{BASE_URL}/{uuid}")
        response.raise_for_status()  # Will raise an error for bad status codes
        data = response.json()

        agent = data.get('data')

        if not agent:
            abort(404, description="Agent not found")

        agent_details = {
            'name': agent.get('displayName'),
            'description': agent.get('description'),
            'image': agent.get('fullPortrait'),
            'role': agent.get('role', {}).get('displayName', "No Role"),
            'abilities': [
                {
                    'name': ability.get('displayName'),
                    'description': ability.get('description'),
                    'icon': ability.get('displayIcon')
                } for ability in agent.get('abilities', []) if ability.get('displayName')
            ]
        }

        return render_template("agent.html", agent=agent_details)

    except requests.exceptions.RequestException as e:
        # Handle the exception if API call fails
        print(f"Error fetching agent details: {e}")
        abort(500, description="Error fetching agent details from the API")

    except Exception as e:
        # Handle any other unforeseen errors
        print(f"Unexpected error: {e}")
        abort(500, description="An unexpected error occurred")

if __name__ == '__main__':
    app.run(debug=True)
