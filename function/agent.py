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


def get_agent(id):
    url = f"{DATA_BASE_API}/agent/{id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return f"Failed to retrieve data, status code: {response.status_code}"
    except requests.RequestException as e:
        return str(e)


def add_agent(data):
    url = f"{DATA_BASE_API}/agent"
    try:
        response = requests.post(url, json=data)
        if response.status_code == 201:
            return response.json()
        return f"Failed to retrieve data, status code: {response.status_code}"
    except requests.RequestException as e:
        return str(e)


def update_agent(id, data):
    url = f"{DATA_BASE_API}/agent/{id}"
    try:
        response = requests.put(url, json=data)
        response.raise_for_status()
        return response.status_code, response.json()
    except requests.HTTPError as http_err:
        return response.status_code, str(http_err)
    except Exception as err:
        return None, str(err)
