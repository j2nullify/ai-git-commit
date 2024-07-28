# Ask How CLI

A CLI that converts natural language to shell commands using Ollama.


## Installation 

Requires:
- Python3.4+
- Ollama

```bash
git clone https://github.com/ColabDog/how-ai-cli.git
cd how-ai-cli
pip install .
```

## Using Ask AI CLI

To use the AI CLI, ask "how" in front of the natural language query inside quotations.

```bash
how "List all files"
```

To generate automated commit messages: 
```
how-commit
```

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
