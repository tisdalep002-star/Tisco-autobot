# MYTHOS — The God Spider 🕷️

> *Weaving through code, networks, and the atoms of thought.*

**MYTHOS** is an autonomous AI-powered terminal agent that brings Claude's intelligence to your command line. It executes complex tasks through natural language, wielding powerful tools for system automation, code execution, API interactions, and token analysis.

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-proprietary-red)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## ✨ Features

### 🔧 Four Powerful Tools

1. **Bash Execution** (`⚙`)
   - Execute any shell command with full system access
   - Run scripts, compile code, inspect processes
   - Traverse and manipulate the filesystem
   - Real-time output capture with error handling

2. **File Operations** (`✍`)
   - Write and append to files in any format
   - Automatic directory creation
   - Safe path expansion with `~` support
   - UTF-8 encoding by default

3. **HTTP Requests** (`⬡`)
   - Make REST API calls (GET, POST, PUT, DELETE, PATCH, HEAD)
   - Custom headers and request bodies
   - Web scraping capabilities
   - Built-in timeout handling and error recovery

4. **Token Analysis** (`◈`)
   - Inspect how text is tokenized by Claude models
   - Count tokens with precision
   - Understand token density and distribution
   - Support for different model contexts

### 🎨 Rich Terminal UI

- **Styled Output**: Color-coded panels, tables, and formatted results
- **Streaming Responses**: Real-time text display as Claude thinks
- **Tool Tracking**: Visual feedback for tool execution and results
- **Token Metrics**: Running count of tokens used in the conversation
- **ASCII Art**: Beautiful splash screen and branding

### 🧠 AI-Powered Autonomy

- Uses Claude (Opus 4.5) for reasoning and decision-making
- Maintains conversation history across interactions
- Automatically selects appropriate tools for tasks
- Synthesizes results with precision and brevity

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- `ANTHROPIC_API_KEY` environment variable set

### Installation

```bash
# Clone the repository
git clone https://github.com/tisdalep002-star/Tisco-autobot.git
cd Tisco-autobot

# Install dependencies
make install
# or
pip install -r requirements.txt
```

### Usage

```bash
# Start MYTHOS
make run
# or
python mythos.py
```

You'll see the splash screen and be ready to interact:

```
⬡ › ask the god spider something
```

### Available Commands

| Command | Description |
|---------|-------------|
| `exit`, `quit`, `q`, `:q` | Leave MYTHOS |
| `clear` | Reset conversation history and token count |
| `/tokens <text>` | Quick token inspection for any text |
| `help` | Show command help |
| *anything else* | Send a natural language request to the spider |

---

## 📋 Examples

### Execute System Commands

```
⬡ › list all python files in the current directory
```

MYTHOS will execute the appropriate bash command and show you the results.

### Create and Manage Files

```
⬡ › create a new Python script that prints "Hello, World!"
```

MYTHOS will write the file to disk automatically.

### Analyze APIs

```
⬡ › fetch the latest commits from the GitHub API for this repo
```

MYTHOS will make HTTP requests and parse the responses.

### Inspect Tokens

```
⬡ › /tokens What is the meaning of life?
```

See how Claude tokenizes your text:

```
property          value
─────────────────────────
tokens            8
characters        38
words             7
chars/token       4.75
tokens/word       1.14
model             claude-opus-4-5
```

### Complex Multi-Step Tasks

```
⬡ › read the contents of my config file, parse the JSON, extract the API keys, and validate them against my environment
```

MYTHOS chains multiple tools together to complete the task.

---

## 🛠️ Development

### Available Make Commands

```bash
make help       # Show all available commands
make install    # Install dependencies
make run        # Run MYTHOS
make test       # Run syntax checks
make lint       # Lint the code with pylint
make format     # Format code with black and isort
make clean      # Remove cache files and artifacts
```

### Running Tests

```bash
make test
```

This performs syntax validation and checks for common issues.

### Code Style

The project uses:
- **Black** for code formatting
- **isort** for import organization
- **pylint** for linting

```bash
make format
make lint
```

### Project Structure

```
Tisco-autobot/
├── mythos.py              # Main application file
├── requirements.txt       # Python dependencies
├── Makefile              # Development tasks
├── README.md             # This file
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── examples/             # Usage examples and scripts
    ├── basic_usage.md
    ├── advanced_tasks.md
    └── integration_patterns.md
```

---

## 🔐 Security

This application requires the `ANTHROPIC_API_KEY` to function. Keep this safe:

```bash
# Set it in your environment
export ANTHROPIC_API_KEY=sk-ant-your-key-here

# Or use a .env file (not in version control)
# See .env.example for the template
```

### Best Practices

- ✅ Never commit API keys to version control
- ✅ Use `.env` files locally (add to `.gitignore`)
- ✅ Rotate API keys regularly
- ✅ Review tool outputs before relying on them
- ✅ Be cautious with bash execution on unfamiliar systems

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file (see `.env.example`):

```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
MYTHOS_MODEL=claude-opus-4-5
MYTHOS_MAX_TOKENS=8192
MYTHOS_TIMEOUT=30
```

### Customization

Edit `mythos.py` to customize:

- **Theme**: Colors and styling in the `THEME` dictionary
- **System Prompt**: AI behavior and instructions in `SYSTEM_PROMPT`
- **Tools**: Add new tools by extending the `TOOLS` list
- **Model**: Change the model in the `Mythos` class (default: `claude-opus-4-5`)

---

## 📚 Advanced Usage

### Custom Tools

Add new tools by:

1. Define the tool schema in `TOOLS`
2. Implement the handler function
3. Add dispatch logic in `dispatch_tool()`

Example:

```python
def run_custom_tool(param: str) -> dict:
    """Your custom tool implementation."""
    try:
        result = do_something(param)
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

### Integration

MYTHOS can be used as:

- **Standalone CLI tool** for interactive automation
- **Component** in larger automation frameworks
- **API server** (with minimal modification)

---

## 🐛 Troubleshooting

### "ANTHROPIC_API_KEY not set"

Set your API key:
```bash
export ANTHROPIC_API_KEY=sk-ant-your-key-here
python mythos.py
```

### "Connection error"

Check your internet connection and API key validity.

### Tools not executing

Ensure required system tools are installed:
- `bash` for shell commands
- Standard Unix utilities (curl, jq, etc.) for HTTP requests

### Import errors

Reinstall dependencies:
```bash
make clean
make install
```

---

## 📖 License

Copyright © 2025 Tisco. All Rights Reserved.

**PROPRIETARY & CONFIDENTIAL** — Trade Secret of Tisco

Unauthorized use, reproduction, or distribution is strictly prohibited. See [LICENSE](LICENSE) for full terms.

---

## 🤝 Contributing

This is a proprietary project. For issues or suggestions, contact the maintainers.

---

## 📞 Support

For help:

1. Check the [examples/](examples/) directory
2. Review the [Troubleshooting](#-troubleshooting) section
3. Inspect the code comments in `mythos.py`

---

**MYTHOS** — *The web spans all. What threads shall we pull today?* 🕸️