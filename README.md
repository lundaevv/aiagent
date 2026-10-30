# AI Agent in Python

A coding AI agent built as part of the [Boot.dev "Build an AI Agent in Python"](https://www.boot.dev/courses/build-ai-agent-python) course.

The agent runs an agentic loop — it takes a user prompt, calls tools as needed, and keeps iterating until it produces a final answer (up to 20 iterations). It can inspect, modify, and run code in any working directory.

## How it works

1. User provides a prompt via CLI
2. The agent sends the prompt + system context to an LLM (via [OpenRouter](https://openrouter.ai))
3. If the model calls a tool, the agent executes it and feeds the result back
4. The loop repeats until the model gives a final text response

## Tools available

| Tool | Description |
|------|-------------|
| `get_files_info` | List files in a directory with sizes |
| `get_file_content` | Read the contents of a file |
| `run_python_file` | Execute a Python file and capture output |
| `write_file` | Write or overwrite a file |

All paths are resolved relative to the working directory, which is configurable in `call_function.py`. By default it points to `calculator/`.

## Target codebase

`calculator/` is the example codebase included with this project — a simple Python calculator that evaluates infix expressions with operator precedence. It's what the agent reads, debugs, and fixes out of the box.

## Setup

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

Create a `.env` file:

```
OPENROUTER_API_KEY=your_key_here
```

## Usage

```bash
uv run main.py "your prompt here"
uv run main.py "your prompt here" --verbose
```

**Example:**

```bash
uv run main.py "Fix the operator precedence bug in the calculator"
uv run main.py "Run the tests and tell me what fails" --verbose
```

## Project structure

```
├── main.py               # Entry point, agentic loop
├── call_function.py      # Tool dispatcher
├── prompts.py            # System prompt
├── config.py             # Constants (MAX_CHARS)
├── functions/            # Tool implementations
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── run_python_file.py
│   └── write_file.py
└── calculator/           # Target codebase the agent operates on
    ├── main.py
    ├── tests.py
    └── pkg/
        └── calculator.py
```

> **Warning:** Do not give this program to others to use. It does not have the security and safety features that a production AI agent would have. This is for learning purposes only.
