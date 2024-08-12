"""Make a pull request
"""
import subprocess
from app.query_bedrock import query_bedrock
from app.extract_bash import extract_bash_commands_no_line_split

def get_current_branch():
    return subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()

def get_pr_number():
    try:
        pr_info = subprocess.check_output(["gh", "pr", "view", "--json", "number"]).decode()
        return int(pr_info.split(":")[1].strip()[:-1])
    except subprocess.CalledProcessError:
        return None

def get_pr_diff(pr_number):
    try:
        diff = subprocess.check_output(["gh", "pr", "diff", str(pr_number)]).decode()
        return diff
    except subprocess.CalledProcessError:
        print(f"Error: Unable to get the diff for PR #{pr_number}.")
        return None

def review_pull_request(pr_number):
    pr_diff = get_pr_diff(pr_number)
    if not pr_diff:
        return
    prompt = f"""Review the following pull request diff and provide a concise review comment. 
    Focus on detecting any potential issues, bugs, or security vulnerabilities.
    Include suggestions for improvement, and an overall assessment of code quality and functionality.
    If you have any specific code change suggestions to address these concerns, please include them as well.
    
    Additionally, highlight any unintended consequences or potential side effects that the developer may not have realized. 
    Consider suggesting better approaches based on established frameworks or design patterns.
    
    Analyze the changes in the context of:
    1. Code maintainability and readability
    2. Performance implications
    3. Scalability considerations
    4. Adherence to best practices and coding standards
    5. Potential impact on other parts of the system
    
    If applicable, recommend using specific libraries, tools, or frameworks that could improve the implementation.

    {pr_diff}

    Respond with only the review comment, enclosed in triple backticks (```).

    For example:

    ```
    The changes look good overall. Consider adding more unit tests for the new functionality.
    
    Suggestion for improvement:
    In file.py, line 42, consider changing:
    if x == None:
    to:
    if x is None:
    
    This is more idiomatic Python and avoids potential issues with custom __eq__ methods.
    ```
    """

    review_comment = query_bedrock(prompt)
    review_comment = extract_bash_commands_no_line_split(review_comment)[0]

    try:
        result = subprocess.run([
            "gh", "pr", "review", str(pr_number),
            "--body", review_comment,
            "--comment"
        ])

        if result.returncode == 0:
            print(f"✅ Review submitted successfully for PR #{pr_number}!")
        else:
            print(f"❌ Failed to submit review for PR #{pr_number}. Please try again.")
    except subprocess.CalledProcessError:
        print(f"Error: Unable to submit review for PR #{pr_number}.")

def main():
    # Check if GitHub CLI (gh) is installed
    try:
        subprocess.run(["gh", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("GitHub CLI (gh) is not installed or not found. Please install it to review pull requests.")
        print("Visit https://cli.github.com/ for installation instructions.")
        return

    current_branch = get_current_branch()
    pr_number = get_pr_number()

    if pr_number is None:
        print(f"No pull request found for the current branch '{current_branch}'.")
        create_pr = input("Would you like to create a pull request? (y/n): ").lower()
        if create_pr == 'y':
            subprocess.run(["python", "app/make_pull_request.py"])
            pr_number = get_pr_number()
        else:
            print("Exiting without creating a pull request.")
            return

    if pr_number:
        review_pull_request(pr_number)
    else:
        print("Unable to find or create a pull request. Please check your branch and try again.")

if __name__ == "__main__":
    main()
