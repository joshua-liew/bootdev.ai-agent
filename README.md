# bootdev.ai-agent
'Build an AI Agent in Python' project as part of the boot.dev Back-End Dev Path.

This is a toy version of an agentic cooding tool such as Claude.


## Installation

- Clone this repository
```
git clone https://github.com/joshua-liew/bootdev.ai-agent.git
```
- Install `uv`, the fast new package manager for Python. \([https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)\)
    - On macOS and Linux.
    ```
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
    - On Windows.
    ```
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
- Install dependencies with `uv sync`.
```
uv sync
```
- Activate the virtual environment.
```
source .venv/bin/activate
```
- Test the program with `uv run main.py`. (Expected output below)
```
AI Code Assistant
=================
Usage: main.py <PROMPT> [--verbose]
Error: expected 1 arguments; received 0 - exiting with code 1
```


## Usage
> For security reasons, all actions are performed in the following directory by default:
> `./calculator`.  
> You can change this behaviour by tweaking the constant `WORKING_DIR` in `config.py`.
>
> WARNING: Change this at your own risk.

This agent can do the following actions:
- List files and directories
- Read file content
- Execute Python files with optional arguments
- Write or overwrite files

Pass a prompt to the program to try it out.
```
# Example
uv run main.py "make a file that says 'hello world'."

# Output
 - Calling function: write_file
Final response:
I have created a file named `hello.txt` with the content 'hello world'.

# Example
uv run main.py "look for the file that says 'hello world'. where is it? i do not know where it is."

# Output
 - Calling function: get_files_info
 - Calling function: get_file_content
Final response:
The file `hello.txt` contains the text "hello world".
```
