"""Generate AI-driven commits from diffs
"""

import subprocess
from app.query_ollama import query_ollama
from textwrap import dedent


def generate_commit_message():
    # Get the git diff output
    git_diff_output = subprocess.getoutput("git diff")

    if not git_diff_output:
        print("No changes to commit.")
        return None

    print(git_diff_output)
    # Generate a commit message using the Ollama model
    commit_message = query_ollama(
        dedent(
            f"""
        Please generate a git commit message off this. Be concise but cover all files and changes.
        Git diff:
        {git_diff_output}

        Example commit message: ``feat(app/cli.py, query_ollama.py): enhance CLI experience with history and bash command conversion`

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
        # subprocess.run(["git", "commit", "-am", commit_message])


if __name__ == "__main__":
    main()
