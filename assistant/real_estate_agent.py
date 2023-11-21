import json
import os
from prompt.real_estate_agent import real_estate_agent_instructions


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
                        "name": "get_current_date_and_time",
                        "description": "This function is designed to return the current date and time.",
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
                        "name": "send_email",
                        "description": "This function is designed to send an email when the customer or agent adds or updates an appointment.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "client_email": {
                                    "type": "string",
                                    "description": "It is the email of the client at the appointment.",
                                },
                                "agent_email": {
                                    "type": "string",
                                    "description": "It is the email of the agent at the appointment.",
                                },
                                "subject": {
                                    "type": "string",
                                    "description": "Is the subject of the email about appointment, write something appropriate and polite.",
                                },
                                "body": {
                                    "type": "string",
                                    "description": "Is the body of the email about appointment, mention in the body the exact date and time of the appointment, write something appropriate and polite.",
                                },
                            },
                            "required": [
                                "client_email",
                                "agent_email",
                                "subject",
                                "body",
                            ],
                        },
                    },
                },
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
                                    "description": "Is the new name of the house. Example Beach house",
                                },
                                "house_number": {
                                    "type": "string",
                                    "description": "Is the new house number of the house. Example B102",
                                },
                                "floor": {
                                    "type": "integer",
                                    "description": "It is the new number of floors in the house. Example 2",
                                },
                                "room": {
                                    "type": "integer",
                                    "description": "It is the new number of rooms in the house. Example 4",
                                },
                                "bathroom": {
                                    "type": "integer",
                                    "description": "It is the new number of bathrooms in the house. Example 2",
                                },
                                "kitchen": {
                                    "type": "integer",
                                    "description": "It is the new number of kitchen in the house. Example 1",
                                },
                                "garage": {
                                    "type": "integer",
                                    "description": "It is the new number of garages in the house. Example 2",
                                },
                                "country": {
                                    "type": "string",
                                    "description": "It is the new country where the house is located. Example Costa Rica",
                                },
                                "direction": {
                                    "type": "string",
                                    "description": "It is the new direction where the house is located. Example Playa Hermosa, Hermosa Palms Casa #10, Jacó 61101",
                                },
                                "state": {
                                    "type": "string",
                                    "description": "It is the new state where the house is located. Example Guanacaste",
                                },
                                "price": {
                                    "type": "integer",
                                    "description": "Is the new price of the house. Example 230000",
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Is the new status of the house. But it can only be For Sale, Pending, Under Contract, Contingent Sale, Withdrawn, Expired, Pre-sale, Sold. Example For Sale",
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
                {
                    "type": "function",
                    "function": {
                        "name": "get_agent",
                        "description": "It is the function to obtain the information of a specific agent with the id, which is stored in the database.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "string",
                                    "description": "Is the id identification of the agent in the database.",
                                },
                            },
                            "required": ["id"],
                        },
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "add_agent",
                        "description": "It is the function to add a new agent to the database, but it needs name and other data.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "Is the name of the new agent. Example Daryn Soto",
                                },
                                "email": {
                                    "type": "string",
                                    "description": "Is the email of the new agent. Example Beach darynsoto@gmail.com",
                                },
                                "phone": {
                                    "type": "string",
                                    "description": "Is the phone of the new agent. Example +50686733343",
                                },
                            },
                            "required": ["name", "email", "phone"],
                        },
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "update_agent",
                        "description": "It is the function to update a agent in the database, but it needs the new data.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "string",
                                    "description": "Is the id identification of the agent to update.",
                                },
                                "name": {
                                    "type": "string",
                                    "description": "Is the new name of the agent. Example Gerardo Soto",
                                },
                                "email": {
                                    "type": "string",
                                    "description": "Is the new email of the agent. Example darynsoto@hotmail.com",
                                },
                                "phone": {
                                    "type": "string",
                                    "description": "Is the new phone of the agent. Example +50686733342",
                                },
                            },
                            "required": ["id"],
                        },
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_appointments",
                        "description": "It is the function to obtain the information of all the appointments that are stored in the database, like id, client_name, client_email, appointment_time. But no show the id.",
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
                        "name": "get_appointment",
                        "description": "It is the function to obtain the information of a specific appointment with the id, which is stored in the database.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "string",
                                    "description": "Is the id identification of the appointment in the database.",
                                },
                            },
                            "required": ["id"],
                        },
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "add_appointment",
                        "description": "It is the function to add a new appointment to the database, but it needs name and other data.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "appointment_time": {
                                    "type": "string",
                                    "description": "Is the appointment time of the new appointment. Example 21/11/2023 13:45:30 in timestamp format",
                                },
                                "client_name": {
                                    "type": "string",
                                    "description": "Is the client name of the new appointment, Ask the client her name. Example Juan Miguel",
                                },
                                "client_email": {
                                    "type": "string",
                                    "description": "Is the client email of the new appointment, Ask the client her email. Example juanarce@gmail.com",
                                },
                                "client_phone": {
                                    "type": "string",
                                    "description": "Is the client phone of the new appointment, Ask the client her phone. Example +50686722343",
                                },
                                "notes": {
                                    "type": "string",
                                    "description": "Is the notes of the new appointment. Example I need to see the house quickly",
                                },
                                "house_id": {
                                    "type": "string",
                                    "description": "It is the identification of the house that the client will come to see at the new appointment. Example 17",
                                },
                                "agent_id": {
                                    "type": "string",
                                    "description": "It is the identification of the agent who will show the house to the client at the new appointment. Example 7",
                                },
                            },
                            "required": [
                                "appointment_time",
                                "client_name",
                                "client_email",
                                "client_phone",
                                "notes",
                                "agent_id",
                                "house_id",
                            ],
                        },
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "update_appointment",
                        "description": "It is the function to update a appointment in the database, but it needs the new data.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "appointment_time": {
                                    "type": "string",
                                    "description": "Is the new appointment time of the appointment. Example 21/11/2023 13:45:30 in timestamp format",
                                },
                                "client_name": {
                                    "type": "string",
                                    "description": "Is the new client name of the appointment. Example Juan Miguel",
                                },
                                "client_email": {
                                    "type": "string",
                                    "description": "Is the new client email of the appointment. Example juanarce@gmail.com",
                                },
                                "client_phone": {
                                    "type": "string",
                                    "description": "Is the new client phone of the appointment. Example +50686722343",
                                },
                                "notes": {
                                    "type": "string",
                                    "description": "Is the new notes of the appointment. Example I need to see the house quickly",
                                },
                                "house_id": {
                                    "type": "string",
                                    "description": "It is the new identification of the house that the client will come to see at the appointment. Example 17",
                                },
                                "agent_id": {
                                    "type": "string",
                                    "description": "It is the new identification of the agent who will show the house to the client at the appointment. Example 7",
                                },
                            },
                            "required": [
                                "appointment_time",
                                "client_name",
                                "client_email",
                                "client_phone",
                                "notes",
                                "agent_id",
                                "house_id",
                            ],
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
