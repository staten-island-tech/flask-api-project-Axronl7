import requests

response = requests.get("https://valorant-api.com/v1/agents")
data = response.json
agent_list = data.get('data', []) 
for agent in agent_list:
    print(agent_list)