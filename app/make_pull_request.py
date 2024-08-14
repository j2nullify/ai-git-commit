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
    prompt_title = f"""Generate a concise and informative pull request title based on the following diff:

{pr_diff}

Respond with only the title, enclosed in triple backticks (```). For example:
```
feat(user-auth): Implement JWT-based authentication
```
"""
    pr_title = query_bedrock(prompt_title)
    pr_title = extract_bash_commands_no_line_split(pr_title)[0]

    prompt_body = f"Generate a concise and informative pull request description based on the following diff. Include key changes and their impact:\n\n{pr_diff}"
    pr_description = query_bedrock(prompt_body)
    pr_description = extract_bash_commands_no_line_split(pr_description)[0]
    prompt_label = f"""Based on the following diff, suggest the most appropriate label for this pull request based on SemVer2.
    Choose only one of: "minor", "patch", or "major". Respond with only the label.

    <example>minor</example>
    <example>patch</example>
    <example>major</example>
    Diff:
    {pr_diff}
    """
    pr_label = query_bedrock(prompt_label).strip()

    for labels in pr_label: 
        if "minor" in labels: 
            pr_label = "minor"
        elif "patch" in labels: 
            pr_label = "patch"
        elif "major" in labels: 
            pr_label = "major"

    # Validate the label
    if pr_label not in ["minor", "patch", "major"]:
        print(f"Warning: Invalid label '{pr_label}' generated. Defaulting to 'minor'.")
        pr_label = "minor"

    # Create pull request using GitHub CLI with label
    result = subprocess.run([
        "gh", "pr", "create", "--title", pr_title, "--body", pr_description, 
        "--label", pr_label])
    if result.returncode != 0:
        result = subprocess.run([
            "gh", "pr", "edit", "--title", pr_title, "--body", pr_description, 
        "--label", pr_label])


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

if __name__ == "__main__":
    main()
