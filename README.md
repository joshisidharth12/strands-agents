# my-agent

Local [Strands Agents](https://strandsagents.com/docs/) experiments using LiteLLM (Groq). Includes a weather demo agent and an interactive file-manager agent with sandboxed tools and delete approval.

## Requirements

- Python `>=3.12`
- [uv](https://docs.astral.sh/uv/) (recommended)
- A Groq API key set in a local `.env` file (never commit this file)

```env
GROQ_API_KEY=your_key_here
```

## Setup

```bash
uv sync
```

## Project structure

```
my-agent/
├── src/
│   ├── agents/                 # Agent entrypoints
│   │   ├── weather_agent.py
│   │   └── file_manager_agent.py
│   ├── config/                 # Shared LLM model config (LiteLLM → Groq)
│   ├── harness/                # Hooks / interrupt handlers
│   │   └── delete_interrupt_hook.py
│   └── tools/
│       ├── get_weather.py
│       └── file_manager_tools/
│           └── operations.py   # Sandboxed list / create / delete
├── workspace/                  # Sandbox root for file-manager tools
├── pyproject.toml
└── study-plan.md               # Learning notes (Strands → AgentCore)
```

## Agents

### Weather agent

Simple one-shot agent that calls a weather tool.

| Tool | Description |
|------|-------------|
| `get_weather` | Returns a mock weather string for a location |

Run:

```bash
uv run python -m agents.weather_agent
```

### File manager agent

Interactive CLI agent that lists, creates, and deletes files under `workspace/`. Paths are constrained to that sandbox. Deletes require explicit user approval via a before-tool-call interrupt hook.

| Tool | Description |
|------|-------------|
| `list_dir` | List files/dirs under `workspace/` (relative path) |
| `create_file` | Create a new text file (fails if it already exists) |
| `delete_file` | Delete a file; prompts for `y/N` before running |

Harness:

| Hook | Behavior |
|------|----------|
| `DeleteApprovalHook` | Interrupts `delete_file` and cancels unless the user approves with `y` |

Run:

```bash
uv run file-manager
```

Type `quit`, `exit`, or `q` to leave the REPL.

## Model

Shared model is configured in `src/config/llm_model.py` via LiteLLM → Groq (`groq/openai/gpt-oss-20b`). Credentials come from environment variables only.

## Dependencies

- `strands-agents` — agent loop, tools, hooks
- `litellm` — model provider routing
- `python-dotenv` — load `.env` for local secrets
