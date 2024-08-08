# Ask How CLI

A CLI that converts natural language to shell commands using AWS BedRock.


## Installation 

Requires:
- Python3.4+
- Ollama

Step 1 - clone this repo
```bash
git clone https://github.com/j2nullify/ai-git-commit.git
cd ai-git-commit
pip install .
```

## Using Ask AI CLI

To generate automated commit messages: 
```
# Add your files like normal
git add -u
# Ai-generate commit messages
how-commit
```
![image](./images/image.png)


Then, you can push your changes and use AI to auto-generate you a description

```
how-pr
```

See example PR: https://github.com/j2nullify/ai-git-commit/pull/2

### Design Considerations

Why not a "# List all files"? 
- Often with CLI programs or instructions, many programs use "#" for commenting so I didn't end up choosing.

Why Ollama?
- Your CLI shouldn't be fed into into non-local models where possible. Ollama's development team is also fairly impressive in their delivery
speed and quality of shipping making them a great tool choice.

Why not use instructor?
- Instructor did not really fit this use case as LLMs tend to be able to reliably produce bash code snippets
with backticks.

Why not use online LLMs?
- There are alternative solutions that do this already.

Why not use LiteLLM?
- I liked the project but unfortunately it seemed a bit too unstable for this.
