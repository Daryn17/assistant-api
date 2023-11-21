import json
import requests
import os
from openai import OpenAI
from prompts.real_estate_agent import real_estate_agent_instructions

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
DATA_BASE_API = os.environ["DATA_BASE_API"]

# Init OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)


def get_houses():
    # The endpoint URL
    url = f"{DATA_BASE_API}/houses"
    try:
        # Perform the GET request
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            # The request was successful, return the response data as a JSON object
            return response.json()
        # The request failed, return the status code
        return f"Failed to retrieve data, status code: {response.status_code}"
    except requests.RequestException as e:
        # Handle any requests exceptions that may occur
        return str(e)


def get_houses_by_id(id):
    # The endpoint URL
    url = f"{DATA_BASE_API}/house/{id}"
    try:
        # Perform the GET request
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            # The request was successful, return the response data as a JSON object
            return response.json()
        else:
            # The request failed, return the status code
            return f"Failed to retrieve data, status code: {response.status_code}"
    except requests.RequestException as e:
        # Handle any requests exceptions that may occur
        return str(e)


def add_house(data):
    # The endpoint URL
    url = f"{DATA_BASE_API}/house"
    try:
        response = requests.post(url, json=data)
        # Check if the request was successful
        if response.status_code == 201:
            # The request was successful, return the response data as a JSON object
            return response.json()
        else:
            # The request failed, return the status code
            return f"Failed to retrieve data, status code: {response.status_code}"
    except requests.RequestException as e:
        # Handle any requests exceptions that may occur
        return str(e)


def update_house(id, data):
    # The endpoint URL
    url = f"{DATA_BASE_API}/house/{id}"
    try:
        # Send the PUT request
        response = requests.put(url, json=data)
        # If the response code is 200-299, it was successful
        response.raise_for_status()
        # Return the status code and the response content
        return response.status_code, response.json()
    except requests.HTTPError as http_err:
        # Return the status code and HTTP error message
        return response.status_code, str(http_err)
    except Exception as err:
        # For other exceptions, return None and the error message
        return None, str(err)


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
            # Getting assistant prompt from "prompts.py" file, edit on left panel if you want to change the prompt
            instructions=real_estate_agent_instructions,
            model="gpt-4-1106-preview",
            tools=[
                {"type": "code_interpreter"},
                {
                    "type": "function",  # This adds the lead capture as a tool
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
                        "name": "get_houses_by_id",
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
            ],
        )

        # Create a new assistant.json file to load on future runs
        with open(assistant_file_path, "w") as file:
            json.dump({"assistant_id": assistant.id}, file)
            print("Created a new assistant and saved the ID.")

        assistant_id = assistant.id

    return assistant_id
