"""Query Ollama model
"""

import os
import requests
import json
import subprocess
from app.config import DEFAULT_MODEL, DEFAULT_URL


def init_ollama():
    subprocess.Popen(
        ["ollama", "start"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    subprocess.Popen(
        ["ollama", "serve"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )


def query_ollama(prompt, stream: bool = True):
    init_ollama()
    url = os.getenv("HOW_DEFAULT_URL", DEFAULT_URL)
    model = os.getenv("HOW_DEFAULT_MODEL", DEFAULT_MODEL)
    history = subprocess.getoutput("history")

    data = {
        "model": model,
        "prompt": f"""Convert the following natural language command to a bash command: {prompt}
History of CLI commands if it helps:
<history>
{history}
</history>
""",
        "stream": stream,
    }

    if stream:
        full_response = ""
        with requests.post(url, json=data, stream=True) as response:
            for line in response.iter_lines():
                if line:
                    json_response = json.loads(line)
                    chunk = json_response.get("response", "")
                    full_response += chunk
                    print(chunk, end="", flush=True)
                if json_response.get("done", False):
                    print()  # Print a newline at the end
                    break
        return full_response.strip()
    else:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            response_text = response.json()["response"].strip()
            print(response_text)
            return response_text
        else:
            error_message = f"Error: Unable to get response from Ollama. Status code: {response.status_code}"
            print(error_message)
            return error_message


if __name__ == "__main__":
    user_input = "List files"
    if user_input.lower() == "exit":
        print("Exiting. Goodbye!")
    command = query_ollama(user_input, True)
    print(f"Generated command: {command}")
