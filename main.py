import json
import os
import time
from flask import Flask, request, jsonify
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
import openai
from openai import OpenAI
import assistant.real_estate_agent as real_estate_agent

# Check OpenAI version compatibility
from packaging import version

required_version = version.parse("1.1.1")
current_version = version.parse(openai.__version__)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if current_version < required_version:
    raise ValueError(
        f"Error: OpenAI version {openai.__version__} is less than the required version 1.1.1"
    )

print("OpenAI version is compatible.")

# Create Flask app
app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Create or load assistant
assistant_id = real_estate_agent.create_assistant(
    client
)  # this function comes from "functions.py"


# Start conversation thread
@app.route("/start", methods=["GET"])
def start_conversation():
    print("Starting a new conversation...")
    thread = client.beta.threads.create()
    print(f"New thread created with ID: {thread.id}")
    return jsonify({"thread_id": thread.id})


# Generate response
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
                if tool_call.function.name == "get_houses":
                    # Process lead get_houses
                    output = real_estate_agent.get_houses()
                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread_id,
                        run_id=run.id,
                        tool_outputs=[
                            {"tool_call_id": tool_call.id, "output": json.dumps(output)}
                        ],
                    )
                if tool_call.function.name == "get_houses_by_id":
                    # Process lead get_houses_by_id
                    arguments = json.loads(tool_call.function.arguments)
                    output = real_estate_agent.get_houses_by_id(arguments["id"])
                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread_id,
                        run_id=run.id,
                        tool_outputs=[
                            {"tool_call_id": tool_call.id, "output": json.dumps(output)}
                        ],
                    )
                if tool_call.function.name == "add_house":
                    # Process lead add_house
                    arguments = json.loads(tool_call.function.arguments)
                    output = real_estate_agent.add_house(
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
                    # Process lead update_house
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

                    output = real_estate_agent.update_house(
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