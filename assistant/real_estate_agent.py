import json
import os
from prompts.real_estate_agent import real_estate_agent_instructions


# Create or load assistant
def create_assistant(client):
    assistant_file_path = "assistant.json"

    # If there is an assistant.json file already, then load that assistant
    if os.path.exists(assistant_file_path):
        with open(assistant_file_path, "r") as file:
            assistant_data = json.load(file)
            assistant_id = assistant_data["assistant_id"]
            print("Loaded existing assistant ID.")
    else:
        # If no assistant.json is present, create a new assistant using the below specifications
        assistant = client.beta.assistants.create(
            name="real_estate_agent_assistant",
            instructions=real_estate_agent_instructions,
            model="gpt-4-1106-preview",
            tools=[
                {"type": "code_interpreter"},
                {
                    "type": "function",
                    "function": {
                        "name": "get_houses",
                        "description": "It is the function to obtain the information of all the houses that are stored in the database, like id, direction, name, price, state and status. But no show the id.",
                        "parameters": {
                            "type": "object",
                            "properties": {},
                            "required": [],
                        },
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_house",
                        "description": "It is the function to obtain the information of a specific house with the id, which is stored in the database.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "string",
                                    "description": "Is the id identification of the house in the database.",
                                },
                            },
                            "required": ["id"],
                        },
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "add_house",
                        "description": "It is the function to add a new house to the database, but it needs name, location and price.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "Is the name of the new house. Example Beach house",
                                },
                                "house_number": {
                                    "type": "string",
                                    "description": "Is the house number of the new house. Example B102",
                                },
                                "floor": {
                                    "type": "integer",
                                    "description": "It is the number of floors in the new house. Example 2",
                                },
                                "room": {
                                    "type": "integer",
                                    "description": "It is the number of rooms in the new house. Example 4",
                                },
                                "bathroom": {
                                    "type": "integer",
                                    "description": "It is the number of bathrooms in the new house. Example 2",
                                },
                                "kitchen": {
                                    "type": "integer",
                                    "description": "It is the number of kitchen in the new house. Example 1",
                                },
                                "garage": {
                                    "type": "integer",
                                    "description": "It is the number of garages in the new house. Example 2",
                                },
                                "country": {
                                    "type": "string",
                                    "description": "It is the country where the new house is located. Example Costa Rica",
                                },
                                "direction": {
                                    "type": "string",
                                    "description": "It is the direction where the new house is located. Example Playa Hermosa, Hermosa Palms Casa #10, Jacó 61101",
                                },
                                "state": {
                                    "type": "string",
                                    "description": "It is the state where the new house is located. Example Guanacaste",
                                },
                                "price": {
                                    "type": "integer",
                                    "description": "Is the price of the new house. Example 230000",
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Is the status of the new house. But it can only be For Sale, Pending, Under Contract, Contingent Sale, Withdrawn, Expired, Pre-sale, Sold. Example For Sale",
                                },
                            },
                            "required": [
                                "name",
                                "house_number",
                                "floor",
                                "room",
                                "bathroom",
                                "kitchen",
                                "garage",
                                "country",
                                "direction",
                                "state",
                                "price",
                                "status",
                            ],
                        },
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "update_house",
                        "description": "It is the function to update a house in the database, but it needs the new data.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "string",
                                    "description": "Is the id identification of the house to update.",
                                },
                                "name": {
                                    "type": "string",
                                    "description": "Is the new name of the new house. Example Beach house",
                                },
                                "house_number": {
                                    "type": "string",
                                    "description": "Is the new house number of the new house. Example B102",
                                },
                                "floor": {
                                    "type": "integer",
                                    "description": "It is the new number of floors in the new house. Example 2",
                                },
                                "room": {
                                    "type": "integer",
                                    "description": "It is the new number of rooms in the new house. Example 4",
                                },
                                "bathroom": {
                                    "type": "integer",
                                    "description": "It is the new number of bathrooms in the new house. Example 2",
                                },
                                "kitchen": {
                                    "type": "integer",
                                    "description": "It is the new number of kitchen in the new house. Example 1",
                                },
                                "garage": {
                                    "type": "integer",
                                    "description": "It is the new number of garages in the new house. Example 2",
                                },
                                "country": {
                                    "type": "string",
                                    "description": "It is the new country where the new house is located. Example Costa Rica",
                                },
                                "direction": {
                                    "type": "string",
                                    "description": "It is the new direction where the new house is located. Example Playa Hermosa, Hermosa Palms Casa #10, Jacó 61101",
                                },
                                "state": {
                                    "type": "string",
                                    "description": "It is the new state where the new house is located. Example Guanacaste",
                                },
                                "price": {
                                    "type": "integer",
                                    "description": "Is the new price of the new house. Example 230000",
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Is the new status of the new house. But it can only be For Sale, Pending, Under Contract, Contingent Sale, Withdrawn, Expired, Pre-sale, Sold. Example For Sale",
                                },
                            },
                            "required": ["id"],
                        },
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_agents",
                        "description": "It is the function to obtain the information of all the agents that are stored in the database, like id, name, email. But no show the id.",
                        "parameters": {
                            "type": "object",
                            "properties": {},
                            "required": [],
                        },
                    },
                },
            ],
        )

        # Create a new assistant.json file to load on future runs
        with open(assistant_file_path, "w") as file:
            json.dump({"assistant_id": assistant.id}, file)
            print("Created a new assistant and saved the ID.")

        assistant_id = assistant.id

    return assistant_id
