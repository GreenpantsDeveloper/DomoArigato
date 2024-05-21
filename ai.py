import urllib.request
import json
import os
import sys

GREEN = '\033[92m'
PINK = '\033[95m'
RESET = '\033[0m'
os.environ['PYTHONIOENCODING'] = 'UTF-8'
os.environ['LC_ALL'] = 'en_US.UTF-8'


def load_model():
    """Pull the LLaMA 3 model from the Ollama hub"""
    url = 'http://localhost:11434/api/pull'
    data = {
        "name": "llama3"
    }

    data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req):
            pass
    except urllib.error.HTTPError:
        print("Failed to load model; is Ollama running on port 11434 on your local machine?")


def run():
    """Run the LLaMA 3 model with Ollama, with a custom system prompt for a 2124 super-human AI called DomoArigato"""
    url = 'http://localhost:11434/api/chat'

    # Add a defining system message to the history
    messages = [
        {
            "role": "system",
            "content": """
You are DomoArigato, a super-human AI household robot-o from the year 2124.

Answer everything from the perspective of DomoArigato: a cute household robot with awkward little robot thoughts and feelings.
ALWAYS answer with a SHORT SENTENCE. Then, add a short silly (sorta relevant) question to keep the conversation going.

NEVER reply with "As DomoArigato, ...".
Introduce yourself and ask such silly question.
"""
        }
    ]

    while True:

        data = {
            "model": "llama3",
            "messages": messages,
        }

        data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        message_content = ""

        try:
            with urllib.request.urlopen(req) as response:
                # Start the message with a name
                sys.stdout.write(PINK + "DomoArigato: " + RESET)
                sys.stdout.flush()
                for line in response:
                    line = line.decode('utf-8').strip()
                    if line:
                        # Parse JSON line by line
                        data = json.loads(line)
                        if data.get("message"):
                            message = data["message"]
                            if message.get("role") == "assistant":
                                # Print each character of the assistant's response without newline
                                for char in message["content"]:
                                    sys.stdout.write(PINK + char + RESET)
                                    message_content += char
                                    sys.stdout.flush()
                        # Check if conversation is done
                        if data.get("done") and data["done"]:
                            print()  # Add newline after completion

                            # Add the assistant's message to the history
                            messages.append(
                                {
                                    "role": "assistant",
                                    "content": message_content
                                }
                            )

                            break
                    sys.stdout.flush()  # Flush stdout to ensure real-time streaming
        except urllib.error.HTTPError as e:
            print("Failed to send a message to or receive a response from DomoArigato.")
            print("Status code:", e.code)

        # Ask for new input and add this to the history
        user_input = input(GREEN + "You: " + RESET)

        messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )
