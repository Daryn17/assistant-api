from dotenv import load_dotenv, find_dotenv

import requests
import os

_ = load_dotenv(find_dotenv())

DATA_BASE_API = os.environ["DATA_BASE_API"]


def get_agents():
    url = f"{DATA_BASE_API}/agents"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return f"Failed to retrieve data, status code: {response.status_code}"
    except requests.RequestException as e:
        return str(e)
