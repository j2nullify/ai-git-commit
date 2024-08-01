"""Generate AI-driven commits from diffs
"""

import subprocess
from app.query_bedrock import query_bedrock
from textwrap import dedent
from rich.prompt import Prompt
from app.extract_bash import extract_bash_commands_no_line_split


def generate_commit_message():
    # Get the git diff output
    git_diff_output = subprocess.getoutput("git diff --cached")

    if not git_diff_output:
        print("No changes to commit.")
        return None

    print(git_diff_output)
    # Generate a commit message using the Ollama model
    commit_message = query_bedrock(
        dedent(
            f"""
        Please generate a git commit message off this. Be concise but cover all files and changes.
        Git diff:
        {git_diff_output}

        Example commit message: 

        ```bash
        feat(app/cli.py, query_ollama.py): enhance CLI experience with history and bash command conversion
        ```

        Commit message:
        """
        )
    )

    if not commit_message:
        print("Failed to generate a commit message.")
        return None

    return commit_message.strip()


def main():
    commit_message = generate_commit_message()
    if commit_message:
        print("Generated commit message:")
        print(commit_message)
        # Here you could add code to automatically commit using this message
        # For example:
        bash_commands = extract_bash_commands_no_line_split(commit_message)
        if len(bash_commands) == 0:
            bash_commands = [commit_message]
        value = Prompt.ask("Commit message", default=bash_commands[0])
        return subprocess.run(["git", "commit", "-m", value])


if __name__ == "__main__":
    main()
