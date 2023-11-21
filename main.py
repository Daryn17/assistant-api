from flask import Flask, request, jsonify
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from packaging import version
from assistant.real_estate_agent import create_assistant
from function.house import get_houses, get_house, add_house, update_house
from function.agent import get_agents, get_agent, add_agent, update_agent
from function.appointment import (
    get_appointments,
    get_appointment,
    add_appointment,
    update_appointment,
)
from function.utils import get_current_date_and_time

import json
import os
import time
import openai

_ = load_dotenv(find_dotenv())

required_version = version.parse("1.1.1")
current_version = version.parse(openai.__version__)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if current_version < required_version:
    raise ValueError(
        f"Error: OpenAI version {openai.__version__} is less than the required version 1.1.1"
    )

print("OpenAI version is compatible.")

app = Flask(__name__)

client = OpenAI(api_key=OPENAI_API_KEY)

# Create or load assistant
assistant_id = create_assistant(client)


# Start conversation thread
@app.route("/start", methods=["GET"])
def start_conversation():
    print("Starting a new conversation...")
    thread = client.beta.threads.create()
    print(f"New thread created with ID: {thread.id}")
    return jsonify({"thread_id": thread.id})


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    thread_id = data.get("thread_id")
    user_input = data.get("message", "")

    if not thread_id:
        print("Error: Missing thread_id")
        return jsonify({"error": "Missing thread_id"}), 400

    print(f"Received message: {user_input} for thread ID: {thread_id}")

    # Add the user's message to the thread
    client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=user_input
    )

    # Run the Assistant
    run = client.beta.threads.runs.create(
        thread_id=thread_id, assistant_id=assistant_id
    )

    # Check if the Run requires action (function call)
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread_id, run_id=run.id
        )
        # print(f"Run status: {run_status.status}")
        if run_status.status == "completed":
            break
        if run_status.status == "requires_action":
            # Handle the function call
            for tool_call in run_status.required_action.submit_tool_outputs.tool_calls:
                if tool_call.function.name == "get_current_date_and_time":
                    output = get_current_date_and_time()
                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread_id,
                        run_id=run.id,
                        tool_outputs=[
                            {"tool_call_id": tool_call.id, "output": json.dumps(output)}
                        ],
                    )
                if tool_call.function.name == "get_houses":
                    output = get_houses()
                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread_id,
                        run_id=run.id,
                        tool_outputs=[
                            {"tool_call_id": tool_call.id, "output": json.dumps(output)}
                        ],
                    )
                if tool_call.function.name == "get_house":
                    arguments = json.loads(tool_call.function.arguments)
                    output = get_house(arguments["id"])
                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread_id,
                        run_id=run.id,
                        tool_outputs=[
                            {"tool_call_id": tool_call.id, "output": json.dumps(output)}
                        ],
                    )
                if tool_call.function.name == "add_house":
                    arguments = json.loads(tool_call.function.arguments)
                    output = add_house(
                        {
                            "name": arguments["name"],
                            "house_number": arguments["house_number"],
                            "floor": arguments["floor"],
                            "room": arguments["room"],
                            "bathroom": arguments["bathroom"],
                            "kitchen": arguments["kitchen"],
                            "garage": arguments["garage"],
                            "country": arguments["country"],
                            "direction": arguments["direction"],
                            "state": arguments["state"],
                            "price": arguments["price"],
                            "status": arguments["status"],
                        }
                    )
                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread_id,
                        run_id=run.id,
                        tool_outputs=[
                            {"tool_call_id": tool_call.id, "output": json.dumps(output)}
                        ],
                    )
                if tool_call.function.name == "update_house":
                    arguments = json.loads(tool_call.function.arguments)
                    data = {}
                    if "name" in arguments:
                        data["name"] = arguments["name"]
                    if "house_number" in arguments:
                        data["house_number"] = arguments["house_number"]
                    if "floor" in arguments:
                        data["floor"] = arguments["floor"]
                    if "room" in arguments:
                        data["room"] = arguments["room"]
                    if "bathroom" in arguments:
                        data["bathroom"] = arguments["bathroom"]
                    if "kitchen" in arguments:
                        data["kitchen"] = arguments["kitchen"]
                    if "garage" in arguments:
                        data["garage"] = arguments["garage"]
                    if "country" in arguments:
                        data["country"] = arguments["country"]
                    if "direction" in arguments:
                        data["direction"] = arguments["direction"]
                    if "state" in arguments:
                        data["state"] = arguments["state"]
                    if "price" in arguments:
                        data["price"] = arguments["price"]
                    if "status" in arguments:
                        data["status"] = arguments["status"]

                    output = update_house(
                        arguments["id"],
                        data,
                    )
                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread_id,
                        run_id=run.id,
                        tool_outputs=[
                            {"tool_call_id": tool_call.id, "output": json.dumps(output)}
                        ],
                    )

                if tool_call.function.name == "get_agents":
                    output = get_agents()
                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread_id,
                        run_id=run.id,
                        tool_outputs=[
                            {"tool_call_id": tool_call.id, "output": json.dumps(output)}
                        ],
                    )

                if tool_call.function.name == "get_agent":
                    arguments = json.loads(tool_call.function.arguments)
                    output = get_agent(arguments["id"])
                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread_id,
                        run_id=run.id,
                        tool_outputs=[
                            {"tool_call_id": tool_call.id, "output": json.dumps(output)}
                        ],
                    )

                if tool_call.function.name == "add_agent":
                    arguments = json.loads(tool_call.function.arguments)
                    output = add_agent(
                        {
                            "name": arguments["name"],
                            "email": arguments["email"],
                            "phone": arguments["phone"],
                        }
                    )
                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread_id,
                        run_id=run.id,
                        tool_outputs=[
                            {"tool_call_id": tool_call.id, "output": json.dumps(output)}
                        ],
                    )

                if tool_call.function.name == "update_agent":
                    arguments = json.loads(tool_call.function.arguments)
                    data = {}
                    if "name" in arguments:
                        data["name"] = arguments["name"]
                    if "email" in arguments:
                        data["email"] = arguments["email"]
                    if "phone" in arguments:
                        data["phone"] = arguments["phone"]

                    output = update_agent(
                        arguments["id"],
                        data,
                    )
                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread_id,
                        run_id=run.id,
                        tool_outputs=[
                            {"tool_call_id": tool_call.id, "output": json.dumps(output)}
                        ],
                    )

                if tool_call.function.name == "get_appointments":
                    output = get_appointments()
                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread_id,
                        run_id=run.id,
                        tool_outputs=[
                            {"tool_call_id": tool_call.id, "output": json.dumps(output)}
                        ],
                    )

                if tool_call.function.name == "get_appointment":
                    arguments = json.loads(tool_call.function.arguments)
                    output = get_appointment(arguments["id"])
                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread_id,
                        run_id=run.id,
                        tool_outputs=[
                            {"tool_call_id": tool_call.id, "output": json.dumps(output)}
                        ],
                    )

                if tool_call.function.name == "add_appointment":
                    arguments = json.loads(tool_call.function.arguments)
                    output = add_appointment(
                        {
                            "agent_id": arguments["agent_id"],
                            "appointment_time": arguments["appointment_time"],
                            "client_name": arguments["client_name"],
                            "client_email": arguments["client_email"],
                            "client_phone": arguments["client_phone"],
                            "house_id": arguments["house_id"],
                            "notes": arguments["notes"],
                        }
                    )
                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread_id,
                        run_id=run.id,
                        tool_outputs=[
                            {"tool_call_id": tool_call.id, "output": json.dumps(output)}
                        ],
                    )

                if tool_call.function.name == "update_appointment":
                    arguments = json.loads(tool_call.function.arguments)
                    data = {}
                    if "agent_id" in arguments:
                        data["agent_id"] = arguments["agent_id"]
                    if "appointment_time" in arguments:
                        data["appointment_time"] = arguments["appointment_time"]
                    if "client_name" in arguments:
                        data["client_name"] = arguments["client_name"]
                    if "client_email" in arguments:
                        data["client_email"] = arguments["client_email"]
                    if "client_phone" in arguments:
                        data["client_phone"] = arguments["client_phone"]
                    if "house_id" in arguments:
                        data["house_id"] = arguments["house_id"]
                    if "notes" in arguments:
                        data["notes"] = arguments["notes"]

                    output = update_appointment(
                        arguments["id"],
                        data,
                    )
                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread_id,
                        run_id=run.id,
                        tool_outputs=[
                            {"tool_call_id": tool_call.id, "output": json.dumps(output)}
                        ],
                    )

            time.sleep(1)  # Wait for a second before checking again

    # Retrieve and return the latest message from the assistant
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    response = messages.data[0].content[0].text.value

    print(f"Assistant response: {response}")
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
