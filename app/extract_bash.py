"""Given an LLM response, extract bash commands.
"""

import re


def extract_bash_commands(llm_response: str) -> list:
    """
    Extracts a list of bash commands from a given LLM response.

    Args:
    llm_response (str): The response from the LLM containing the bash commands.

    Returns:
    list: A list of the extracted bash commands.
    """
    # Start of the bash script in the response

    commands = []
    pattern = re.compile(r"```(?:bash)?(.*?)```", re.DOTALL)
    matches = pattern.findall(llm_response)
    for match in matches:
        com = match.strip().split("\n")
        if com == "":
            continue
        commands.extend(com)

    return commands


if __name__ == "__main__":
    from query_ollama import query_ollama

    user_input = "List files"
    if user_input.lower() == "exit":
        print("Exiting. Goodbye!")
    command = query_ollama(user_input)
    print(f"Generated command: {command}")
    commands = extract_bash_commands(command)
    print("Commands:")
    print(commands)
