import subprocess
import sys
from app.query_ollama import query_ollama
from app.extract_bash import extract_bash_commands
from app.menu import row_based_rich_menu
from app.config import EXIT_COMMAND


def process_query(query: str):
    response = query_ollama(query)
    bash_commands = extract_bash_commands(response)
    if len(bash_commands) == 0:
        print("No command could be produced")
        return 0
    selected_bash_command = row_based_rich_menu(bash_commands)
    if selected_bash_command == EXIT_COMMAND:
        return 0
    try:
        result = subprocess.run(selected_bash_command, check=True, shell=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing the command: {e}")
        return 1


def main():
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        return process_query(query)
    else:
        print("Please provide a query.")
        sys.exit(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    args = parser.parse_args()
    main(args.query)
