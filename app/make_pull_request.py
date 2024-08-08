import subprocess
from app.query_bedrock import query_bedrock
from app.extract_bash import extract_bash_commands_no_line_split

def get_pr_diff():
    try:
        diff = subprocess.check_output(["git", "diff", "origin/main...HEAD"]).decode()
        return diff
    except subprocess.CalledProcessError:
        print("Error: Unable to get the diff. Make sure you're in a git repository.")
        return None

def main():
    # Push the branch to remote
    # Get the current branch name
    current_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
    
    # Set the upstream to origin and push the current branch
    subprocess.run(["git", "push", "--set-upstream", "origin", current_branch])

    pr_diff = get_pr_diff()
    if not pr_diff:
        return    

    # Generate PR title and description using Bedrock
    prompt_title = f"Generate a concise and informative pull request title based on the following diff:\n\n{pr_diff}"
    pr_title = query_bedrock(prompt_title)
    pr_title = extract_bash_commands_no_line_split(pr_title)[0]

    prompt_body = f"Generate a concise and informative pull request description based on the following diff. Include key changes and their impact:\n\n{pr_diff}"
    pr_description = query_bedrock(prompt_body)
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
    
    result = subprocess.run(["gh", "pr", "create", "--title", pr_title, "--body", pr_description])
    if result.returncode != 0:
        result = subprocess.run(["gh", "pr", "edit", "--title", pr_title, "--body", pr_description])

    if result.returncode == 0:
        print("✅ Pull request created successfully!")
    else:
        print("❌ Failed to create pull request. Please try again.")
    return result 


if __name__ == "__main__":
    main()
