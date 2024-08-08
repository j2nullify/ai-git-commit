import subprocess
from query_ollama import query_ollama
from extract_bash import extract_bash_commands_no_line_split

def make_pull_request():
    # Push the branch to remote
    subprocess.run(["git", "push"])

    # Generate PR description using Ollama
    # Generate PR title and description using Ollama
    prompt_title = "Generate a concise and informative pull request title for a feature branch."
    pr_title = query_ollama(prompt_title)
    pr_title = extract_bash_commands_no_line_split(pr_title)[0]

    prompt_body = "Generate a concise and informative pull request description for a feature branch. Include key changes and their impact."
    pr_description = query_ollama(prompt_body)
    pr_description = extract_bash_commands_no_line_split(pr_description)[0]

    # Create pull request using GitHub CLI
    # Check if GitHub CLI (gh) is installed
    try:
        subprocess.run(["gh", "--version"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("GitHub CLI (gh) is not installed. Please install it to create pull requests.")
        print("Visit https://cli.github.com/ for installation instructions.")
        return
    except FileNotFoundError:
        print("GitHub CLI (gh) is not found. Please install it to create pull requests.")
        print("Visit https://cli.github.com/ for installation instructions.")
        return

    # If gh is installed, proceed with creating the pull request
    subprocess.run(["gh", "pr", "create", "--title", pr_title, "--body", pr_description])

if __name__ == "__main__":
    make_pull_request()
